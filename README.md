# Employee Management System

A local, offline desktop HR application built with Python, Tkinter/ttk and SQLite. It supports administrator setup and login, employee and department CRUD, live workforce summaries, CSV export, and printable HTML profiles. Matplotlib adds a live department chart when installed.

## Abstract and problem statement

Small organizations and student demonstrations often need a simple way to maintain employee information without a hosted service. This project provides a local desktop interface and a relational database for employee records, departments, search, reporting and administrator authentication.

## Objectives and scope

The application demonstrates desktop UI design, validation, password hashing, relational data, CRUD operations, reporting, logging and automated tests. It is intended for educational and small local deployments. It is not an enterprise HR, payroll, multi-user or network security system.

## Requirements and technology

- Python 3.11 or newer, Tkinter (usually included with Windows Python), SQLite (included with Python).
- Matplotlib 3.8+ is optional and enables charts. No network service is required at runtime.
- Suggested hardware: any supported Windows computer with 4 GB RAM and about 100 MB free disk space.

## Features

- First-run administrator creation; PBKDF2-HMAC-SHA256 with a random salt and 600,000 iterations.
- Employee registration, listing, search by ID/name/email/phone, department and status filters, sort, edit, profile, and confirmed delete.
- Department creation/editing; duplicate names are rejected and in-use departments cannot be deleted.
- Database-derived status and department counts, recent additions and optional chart.
- CSV employee directory export and print-friendly HTML employee profiles.
- SQLite foreign-key enforcement, indexes, local error log and input validation.

## Project structure

`main.py` contains Tkinter presentation and application flow. `app/database.py` owns schema and connections; `app/auth.py` handles administrator credentials; `app/validators.py` validates employee input; `app/services/` contains employee, department and export logic. `tests/` uses isolated temporary databases. `docs/` contains design and student report materials.

## Installation and run (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Matplotlib is optional. If package installation is unavailable, run `python main.py`; charts show an installation note and the rest of the application works. On first launch, create an administrator username and a password of at least 10 characters. No default account or password exists. Later launches show the login screen.

## Use

Choose Employees to add records, search and filter, edit or delete (with confirmation), or save an individual printable profile. Choose Departments to manage department names. Reports exports the employee directory as UTF-8 CSV to a path chosen in the save dialog. The export contains work contact, department, designation, dates, status and salary; review it before sharing. Dashboard figures derive from the current local database.

## Database schema

`admins` stores unique usernames, random salts and PBKDF2 hashes. `departments` stores unique names and descriptions. `employees` stores employee profile and work fields, a unique generated employee code, a unique email, timestamps and a required foreign key to departments. See [Database design](docs/DATABASE_DESIGN.md).

## Data location, backup and restore

By default the database is `%USERPROFILE%\.employee_management_system\employees.sqlite3`; logs are stored alongside it. Set `EMPLOYEE_MGMT_DATA` before launch to choose another writable data directory. To back up or restore, close the app first, then copy `employees.sqlite3` to or from a secure location. The shipped default department names are sample seed data, not organization-specific claims.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests create and remove a temporary database and do not touch the live user database. Actual outcomes are recorded in [Test cases](docs/TEST_CASES.md) after execution.

## Limitations and future work

This single-user local tool does not implement role management, payroll, encrypted database storage, automated backup, or multi-device synchronization. Future work could add pagination, finer-grained report filters, a dedicated status chart, PDF generation, configurable organizations and database encryption with a managed key.

## Screenshots

Capture genuine screens by launching `python main.py` on a desktop with Tk support. Use a fresh data directory (`$env:EMPLOYEE_MGMT_DATA = Join-Path $PWD 'demo-data'`) for setup and demo records. Capture setup, login, dashboard, employee form/list/search/edit, departments, CSV save dialog, and an opened HTML profile. Do not place real personal data in report screenshots; use clearly fictional demonstration entries and remove demo data when finished.
