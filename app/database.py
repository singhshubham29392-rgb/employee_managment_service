import sqlite3
from pathlib import Path
from app.config import DB_PATH

DEFAULT_DEPARTMENTS = [("IT", "Information Technology"), ("Human Resources", "People and recruitment"), ("Finance", "Finance and accounting"), ("Marketing", "Marketing and communications"), ("Operations", "Business operations")]

class Database:
    def __init__(self, path=None):
        self.path = str(path or DB_PATH)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        class ClosingConnection(sqlite3.Connection):
            def __exit__(self, exc_type, exc, tb):
                try:
                    return super().__exit__(exc_type, exc, tb)
                finally:
                    self.close()
        con = sqlite3.connect(self.path, factory=ClosingConnection)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys=ON")
        return con

    def initialize(self):
        with self.connect() as c:
            c.executescript('''
            CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, salt BLOB NOT NULL, password_hash BLOB NOT NULL, iterations INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS departments(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE COLLATE NOCASE, description TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY AUTOINCREMENT, employee_code TEXT NOT NULL UNIQUE, full_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE COLLATE NOCASE, phone TEXT NOT NULL, gender TEXT, date_of_birth TEXT, address TEXT NOT NULL DEFAULT '', department_id INTEGER NOT NULL REFERENCES departments(id) ON DELETE RESTRICT, designation TEXT NOT NULL, joining_date TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('Active','On Leave','Resigned')), salary REAL NOT NULL DEFAULT 0 CHECK(salary>=0), emergency_contact TEXT, notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE INDEX IF NOT EXISTS idx_employee_name ON employees(full_name COLLATE NOCASE);
            CREATE INDEX IF NOT EXISTS idx_employee_phone ON employees(phone);
            CREATE INDEX IF NOT EXISTS idx_employee_department ON employees(department_id);
            CREATE INDEX IF NOT EXISTS idx_employee_status ON employees(status);
            ''')
            if not c.execute("SELECT 1 FROM departments LIMIT 1").fetchone():
                c.executemany("INSERT INTO departments(name,description) VALUES(?,?)", DEFAULT_DEPARTMENTS)

    def has_admin(self):
        with self.connect() as c: return c.execute("SELECT 1 FROM admins LIMIT 1").fetchone() is not None
