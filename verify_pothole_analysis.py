import sys
import os
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from ai_engine.advanced_severity import AdvancedSeverityAssessor
from ai_engine.repair_verification import RepairVerificationAI

def verify_pothole_analysis():
    """Verify AI Analysis on test image"""
    image_path = 'test_pothole.jpg'
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Did you run setup_test_data.py?")
        return

    print(f"\nAnalyzing {image_path}...")
    
    # Test Severity Assessment
    print("\n--- Testing Advanced Severity Assessment ---")
    assessor = AdvancedSeverityAssessor()
    try:
        severity, area_sqm, pothole_count, deterioration, analysis = assessor.assess_damage(image_path)
        print(f"Severity: {severity}")
        print(f"Damage Area: {area_sqm:.2f} sqm")
        print(f"Pothole Count: {pothole_count}")
        print(f"Deterioration: {deterioration:.2f}%")
        print("Analysis Details:", analysis)
    except Exception as e:
        print(f"Severity Assessment Error: {e}")

    # Test Repair Verification (using same image as 'after' just to test function)
    print("\n--- Testing Repair Verification (Simulated) ---")
    verifier = RepairVerificationAI()
    try:
        # Simulate verification (using same image for both just to test execution flow)
        is_verified, confidence, quality_score, repair_analysis = verifier.verify_repair(image_path, image_path)
        print(f"Is Verified: {is_verified}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Quality Score: {quality_score:.2f}")
        print("Repair Analysis:", repair_analysis)
    except Exception as e:
        print(f"Repair Verification Error: {e}")

if __name__ == "__main__":
    verify_pothole_analysis()
