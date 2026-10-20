# Employee Management System (Python + SQLite)

This project is an offline desktop application for managing employee and department records. Its graphical interface uses Python Tkinter/ttk, and it stores persistent data in an SQLite database. Matplotlib is optional and adds dashboard charts.

## Project purpose

Instead of keeping employee details in separate manual files, this application provides one place to create, view, search, update, and delete records; filter employees by department or status; and export reports. It is an educational and internship project, not an enterprise payroll or multi-user HR security system.

## How the application works

1. `main.py` runs the application window and Tkinter screens.
2. `app/config.py` defines the database and log file locations. The default database location is `%USERPROFILE%\\.employee_management_system\\employees.sqlite3`.
3. `app/database.py` creates the SQLite database and its `admins`, `departments`, and `employees` tables on first launch. SQLite foreign-key enforcement is enabled for every connection. A new database is seeded with sample departments: IT, Human Resources, Finance, Marketing, and Operations.
4. `app/auth.py` handles first-run administrator setup and later logins. Passwords are never stored as plain text: the app stores a PBKDF2-HMAC-SHA256 hash with a random salt.
5. `main.py` collects form input. `app/validators.py` checks employee fields, while modules in `app/services/` perform CRUD operations, calculate statistics, and export reports using parameterized SQLite queries.
6. The SQLite file preserves records after the application closes. The same database is opened the next time the application starts.

### Database tables

- `admins`: unique username, password salt/hash, and iteration count.
- `departments`: unique department name and description.
- `employees`: generated employee code, name, email, phone, optional personal details, department foreign key, designation, joining date, status, salary, notes, and timestamps.

Employee emails and generated codes must be unique. A department cannot be deleted while employees are assigned to it. Indexes support common searches and filters. See [Database design](docs/DATABASE_DESIGN.md) for details.

## Features

- Create an administrator account on first launch; sign in and log out on later launches.
- Add, list, search, filter, sort, edit, and delete employee records. Deletion requires confirmation.
- The application generates employee IDs automatically, for example `EMP-00001`.
- Search by employee ID, name, email, or phone. Filter by department and employment status.
- Add and edit departments; duplicate department names are rejected.
- Dashboard totals for all employees, active employees, employees on leave, resigned employees, and departments are calculated from the database. Recent additions are also shown.
- A department bar chart appears on the dashboard when Matplotlib is installed.
- Export filtered reports as CSV. Save an individual employee profile as printable HTML.
- Technical errors are written to a local log. User-facing validation errors do not reveal passwords or stored credentials.

## Requirements

- Python 3.11 or newer. Tests in this workspace were run with Python 3.14.
- On Windows, the Python installation must include Tcl/Tk for the desktop interface.
- SQLite is included with Python; you do not need to install a separate SQLite server.
- Matplotlib is optional for charts. The rest of the application uses the Python standard library.

## Install and run on Windows

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell's execution policy prevents activation, run this in the current terminal and try activation again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

The application can still run if Matplotlib installation fails; the dashboard will display a message where the chart would appear.

## First-run administrator setup

On the first `python main.py` launch, the setup screen asks you to create an administrator account. Choose a username of at least 3 characters and a password of at least 10 characters, then confirm the password. There is no default or production password in this project. After the account is created, the application opens the dashboard. Use the same credentials to sign in on later launches. Protect access to the Windows account that holds the local data; local password hashing does not make this an enterprise-grade security system.

## Using the application

### Add an employee

1. After signing in, select **Employees** from the sidebar.
2. Select **Add employee**.
3. Enter the full name, email, phone, department, designation, and joining date. Employment status defaults to **Active**.
4. Enter dates in `YYYY-MM-DD` format. The joining date cannot be in the future. Date of birth is optional and must be in the past. Salary is optional, but if provided it must be a non-negative number.
5. Select **Save employee**. The application validates the fields and checks for duplicate email addresses before saving the record to SQLite. The table refreshes and displays the generated employee code.

Gender, date of birth, address, emergency contact, and notes are optional. Email addresses must be unique. Phone numbers may contain digits, spaces, and common phone symbols.

### View, search, edit, or delete employees

Select a record in the Employees table. The search field matches employee ID, name, email, or phone. Use the dropdowns to filter by department or employment status; **Refresh** reloads the table. Select a column heading to sort. Select a record and choose **View profile** to save and open a printable HTML profile, **Edit** to update it, or **Delete** to remove it. The delete confirmation identifies the employee by name and ID. Deletion cannot be undone.

### Manage departments

Select **Departments** in the sidebar to add or edit departments. Duplicate names are not allowed. Before deleting a department that has employees, edit those employees to reassign them or delete their records.

### Dashboard and report exports

Dashboard values are calculated from the database each time the dashboard is displayed. If there are no employees, the dashboard displays an empty-state message. In **Reports**, search, department, and status filters are optional. Leave all filters blank to export the full directory. Applying filters exports only matching records. Choose a destination in the save dialog. CSV files contain employee ID, name, work email and phone, department, designation, joining date, status, and salary. Review exported data before sharing it.

To create an individual profile, select a record in Employees and choose **View profile**. The HTML file opens in a browser and can be printed using the browser's Print command.

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

Tests create a database in a temporary directory and do not modify the live user database. They cover database initialization, administrator password verification, employee CRUD/search/validation, duplicate email rejection, department deletion restrictions, CSV export, and dashboard statistics. All 6 test methods passed in the Python 3.14 run in this workspace. See [Test cases](docs/TEST_CASES.md) for details. GUI workflows are not covered by the automated test suite.

## Database location, backup, and restore

Default database: `%USERPROFILE%\\.employee_management_system\\employees.sqlite3`. The application log, `application.log`, is stored in the same folder. To choose a different data folder, set the `EMPLOYEE_MGMT_DATA` environment variable before starting the application:

```powershell
$env:EMPLOYEE_MGMT_DATA = Join-Path $PWD 'employee-data'
python main.py
```

To back up the database, close the application and copy `employees.sqlite3` to a secure backup location. To restore it, close the app and copy the backup file back into the data folder, replacing the existing file. The database contains employee personal data; do not share it with untrusted people or add it to a public repository. No real employee database is included in the project source.

## Project files

```text
main.py                            Tkinter interface and screen navigation
app/config.py                      Application name and writable local data paths
app/database.py                    SQLite schema, initialization, and connections
app/auth.py                         Administrator setup and login verification
app/validators.py                   Employee input validation
app/services/employee_service.py   Employee CRUD, search, and statistics
app/services/department_service.py Department CRUD
app/services/report_service.py     CSV and HTML profile generation
tests/                             unittest automated tests
docs/                              Database, user, test, and report documentation
requirements.txt                   Optional Matplotlib dependency
```

## Screenshots and internship report

To capture genuine screenshots, launch the app on a desktop computer. To keep demo data separate from live records, set a separate `EMPLOYEE_MGMT_DATA` folder first. You can capture the setup, login, dashboard, employee add/list/search/edit, department screen, CSV save workflow, and HTML profile. Use fictional demo details only. The [Internship report outline](docs/INTERNSHIP_REPORT_OUTLINE.md) and [User manual](docs/USER_MANUAL.md) provide additional guidance. Students must fill in their own verified organization, training dates, supervisor, results, and learning outcomes; this README does not invent them.

## Limitations and possible future improvements

This is a single-administrator, local desktop application. The database file is not encrypted at rest. Multi-user access control, payroll, automatic backups, and cloud/device synchronization are not implemented. Employee listings do not provide pagination for large datasets. Matplotlib is optional for charts. Possible future improvements include PDF reports, pagination, configurable organization titles, additional report/date filters, and a managed encryption key.
