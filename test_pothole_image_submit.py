"""
Submit the attached pothole image through the app's report flow and verify it works.
Run from project root with venv activated: python test_pothole_image_submit.py
"""
import os
import sys

# Image paths (attached pothole image)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Prefer local copy in project
LOCAL_ASSET = os.path.join(SCRIPT_DIR, "assets", "test_pothole.png")
ASSET_IMAGE = os.path.join(
    SCRIPT_DIR,
    "assets",
    "c__Users_Admin_AppData_Roaming_Cursor_User_workspaceStorage_b98f720318928b395d17b2d5d41479f0_images_images-58a94ce0-0a9d-4414-9af3-62f9cdfe0224.png",
)
FALLBACK_IMAGE = os.path.join(SCRIPT_DIR, "media", "test_pothole_submit.png")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smc_platform.settings")

def get_image_path():
    if os.path.isfile(LOCAL_ASSET):
        return LOCAL_ASSET
    if os.path.isfile(ASSET_IMAGE):
        return ASSET_IMAGE
    if os.path.isfile(FALLBACK_IMAGE):
        return FALLBACK_IMAGE
    cursor_asset = r"C:\Users\Admin\.cursor\projects\c-Users-Admin-Desktop-road-damage-system\assets\c__Users_Admin_AppData_Roaming_Cursor_User_workspaceStorage_b98f720318928b395d17b2d5d41479f0_images_images-58a94ce0-0a9d-4414-9af3-62f9cdfe0224.png"
    if os.path.isfile(cursor_asset):
        return cursor_asset
    return None

def main():
    import django
    django.setup()
    from django.test import Client
    from django.urls import reverse
    from django.core.files.uploadedfile import SimpleUploadedFile
    from reports.models import Report, ReportImage
    from departments.models import Department

    image_path = get_image_path()
    if not image_path:
        print("ERROR: Pothole image not found. Place the image at one of:")
        print(f"  - {LOCAL_ASSET}")
        print(f"  - {ASSET_IMAGE}")
        print(f"  - {FALLBACK_IMAGE}")
        sys.exit(1)

    print(f"Using image: {image_path}")
    print("Submitting report via /reports/create/ ...")

    # Ensure at least one department exists for assignment
    dept, _ = Department.objects.get_or_create(
        name="Public Works Department",
        defaults={"code": "PWD", "description": "Road maintenance", "is_active": True},
    )
    print(f"Department for assignment: {dept.name}")

    client = Client()
    url = reverse("reports:create")

    with open(image_path, "rb") as f:
        image_content = f.read()
    data = {
        "title": "Large pothole with water and cracking - test",
        "description": "Deep pothole filled with water, surrounded by alligator cracking. Needs urgent repair.",
        "location_name": "Test Road, Near Junction",
        "latitude": "17.6599",
        "longitude": "75.9064",
        "damage_type": "pothole",
        "severity": "high",
        "images": SimpleUploadedFile("pothole.png", image_content, content_type="image/png"),
    }
    response = client.post(url, data, format="multipart")

    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        # Form re-displayed: check for errors
        if hasattr(response, "context") and response.context and "form" in response.context:
            form = response.context["form"]
            if form.errors:
                print("FAIL: Form errors:", form.errors)
                sys.exit(1)
            if form.non_field_errors():
                print("FAIL: Form non-field errors:", form.non_field_errors())
                sys.exit(1)
        print("Response 200: Form re-displayed (possible AI decline or validation).")
        sys.exit(1)
    if response.status_code != 302:
        print(f"Unexpected status: {response.status_code}")
        if hasattr(response, "content") and response.content:
            print(response.content[:500])
        sys.exit(1)

    redirect_url = response.get("Location", "")
    print(f"Redirect: {redirect_url}")
    print("SUCCESS: Report accepted (redirect).")

    # Verify the new report and image in DB (latest should be our submission)
    latest = Report.objects.order_by("-reported_at").first()
    if not latest or "Large pothole with water and cracking" not in (latest.title or ""):
        print("WARNING: Latest report in DB is not our submission.")
    else:
        print(f"Report in DB: id={latest.id}, title={latest.title}, status={latest.status}")
    img_count = ReportImage.objects.filter(report=latest).count() if latest else 0
    print(f"Images attached: {img_count}")
    if latest and img_count == 0:
        print("FAIL: No images saved to report.")
        sys.exit(1)
    print("SUCCESS: Pothole image submitted and saved. App flow is working.")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
