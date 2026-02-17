# TEST PLAN: Real-Time Dashboard Updates

## Prerequisites
1. Ensure the server is running (`python manage.py runserver`).
2. You have created an **Admin** user and a **Citizen** user (or use temporary ones).

## Steps

1. **Open the Admin Dashboard**
   - Log in as an Admin.
   - Go to `http://127.0.0.1:8000/dashboard/admin/`.
   - Keep this tab open and visible.

2. **Open the Department Dashboard (Optional)**
   - If you have an Official account, log in as Official in a separate browser (or Incognito window).
   - Go to `http://127.0.0.1:8000/dashboard/department/`.
   - Keep this tab visible.

3. **Submit a New Report**
   - Open a NEW browser window (or Incognito).
   - Log in as a **Citizen**.
   - Go to `http://127.0.0.1:8000/reports/create/`.
   - Fill in the form and submit.

4. **Observe Real-Time Updates**
   - Watch the **Admin Dashboard** tab.
   - **Expected Behavior:**
     - The **"Total Submissions"** and **"Awaiting Verification"** counters should **increment immediately** (+1).
     - A **new row** should appear at the top of the "Citizen Reports Queue" table (highlighted in yellow temporarily).
     - A notification may appear in the "Performance Logs".
   
   - Watch the **Department Dashboard** tab (if open).
     - **Expected Behavior:**
       - Counters update.
       - A **new marker** drops onto the map at the report location.
       - The table updates with the new report.

## Debugging
- If updates don't appear, check the browser console (F12) for WebSocket connection errors.
- Ensure you are connected to `ws://127.0.0.1:8000/ws/dashboard/`.
