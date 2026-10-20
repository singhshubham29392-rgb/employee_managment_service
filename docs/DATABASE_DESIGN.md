# Database design

SQLite database initialized automatically on application start. Each connection enables `PRAGMA foreign_keys=ON`.

| Table | Main fields | Constraints and relationships |
|---|---|---|
| admins | id, username, salt, password_hash, iterations, created_at | Unique username; password material only as salted PBKDF2 hash |
| departments | id, name, description, created_at | Case-insensitive unique name |
| employees | id, employee_code, full_name, email, phone, optional demographics/contact, department_id, designation, joining_date, status, salary, notes, timestamps | Unique employee code and case-insensitive email; required department foreign key with RESTRICT; status and nonnegative salary checks |

Indexes cover employee name, phone, department and status. Lookups and writes use parameterized SQL. Employee changes are committed by SQLite transactions. Database file: `%USERPROFILE%\.employee_management_system\employees.sqlite3` by default; `EMPLOYEE_MGMT_DATA` overrides its containing directory.

Back up and restore only while the application is closed by copying the database file. The five inserted department names are sample defaults used on a newly initialized database.
