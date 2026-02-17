# PROJECT WALKTHROUGH

This document guides you through testing the real-time features of the Road Damage Management System.

## 1. Preparation

### A. Ensure Server is Running
The server should already be running. If not, run:
```bash
start_server.bat
```
Wait until you see `Listening on TCP address 127.0.0.1:8000`.

### B. Create Test Users
We have prepared a script to create the necessary users (Admin, Official, Citizen):
```bash
python create_demo_users.py
```
This creates:
- **Admin**: `admin` / `adminpass`
- **Official**: `official` / `officialpass` (Department: Road Maintenance)
- **Citizen**: `citizen` / `citizenpass`

---

## 2. Verify Real-Time Updates

### Step 1: Open Official Dashboard (Receiver)
1. Open a browser window (e.g., Chrome).
2. Go to: [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
3. Log in as **Official**:
   - Username: `official`
   - Password: `officialpass`
4. Navigate to **"Dept. Map"** in the top navigation bar.
5. Keep this window open and visible. Note the "Pending" count.

### Step 2: Open Admin Dashboard (Receiver)
1. Open a new tab in the same browser.
2. Go to: [http://127.0.0.1:8000/admin/logout/](http://127.0.0.1:8000/admin/logout/) (logout first) or use Incognito.
   - *Tip: Better to use a different browser or Incognito window for the next step.*
3. Log in as **Admin**:
   - Username: `admin`
   - Password: `adminpass`
4. Access the **Admin Dashboard**:
   - Go to [http://127.0.0.1:8000/dashboard/admin/](http://127.0.0.1:8000/dashboard/admin/)
5. Keep this window visible alongside the Official Dashboard.

### Step 3: Create a Report (Sender)
1. Open a **New Private/Incognito Window** (if not already used).
2. Log in as **Citizen**:
   - Username: `citizen`
   - Password: `citizenpass`
3. Go to **"Report Damage"**: [http://127.0.0.1:8000/reports/create/](http://127.0.0.1:8000/reports/create/)
4. **Fill the form**:
   - Click **"Get Location"** (Allow permissions) -> Coordinates appear.
   - Title: "Deep Pothole on Main St"
   - Description: "Large pothole causing traffic issues."
   - Click **"Open Camera"** -> Take a photo.
   - Submit the report.

### Step 4: Witness the Update
- Immediately look at the **Official Dashboard** and **Admin Dashboard**.
- **WITHOUT REFRESHING**, you should see:
  - The **"Pending"** counter increment (+1).
  - A **New Row** appear in the "Recent Reports" list.
  - A **New Marker** drop onto the map (Official Dashboard).
  - A notification toast (if enabled).

## 3. Explore Features

- **Map Interaction**: Click the new marker on the Official Dashboard to see the photo you just took.
- **Status Update**: As Admin/Official, open the report details and change status to "In Progress". Go back to the dashboard -> Status updates instantly.

---

**Troubleshooting**:
- If updates don't appear, refresh the page once to ensure WebSocket connection.
- Check browser console (F12) for "WebSocket connected" message.
