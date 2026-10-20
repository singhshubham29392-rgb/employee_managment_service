# User manual

1. Install Python 3.11+ and launch `python main.py` from the project directory.
2. On first run, create an administrator username and password (10+ characters). Later launches require this login.
3. Dashboard shows live counts; it is empty until records are entered. The department chart appears with Matplotlib installed.
4. In Departments, add/edit departments. A department containing employees cannot be deleted until its employees are reassigned or removed.
5. In Employees, choose Add employee. Required fields are name, email, phone, department, designation, joining date and status. Dates use YYYY-MM-DD. Select a row to view a profile, edit, or delete it. Search supports code/name/email/phone; dropdowns filter department and status.
6. In Reports, choose CSV export and select a destination. In Employees, select View profile to save a printable HTML report.
7. Close the application before copying the database for backup or restore. Use Logout to return to the login screen.

The application stores local records and a technical error log under `%USERPROFILE%\.employee_management_system` unless overridden with `EMPLOYEE_MGMT_DATA`. Keep access to that folder restricted and avoid using real personal data in demonstrations.
