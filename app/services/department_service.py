class DepartmentService:
    def __init__(self, db): self.db=db
    def list(self):
        with self.db.connect() as c: return c.execute("SELECT d.*,COUNT(e.id) employee_count FROM departments d LEFT JOIN employees e ON e.department_id=d.id GROUP BY d.id ORDER BY d.name").fetchall()
    def save(self,name,description="",department_id=None):
        if not name.strip(): raise ValueError("Department name is required.")
        try:
            with self.db.connect() as c:
                if department_id: c.execute("UPDATE departments SET name=?,description=? WHERE id=?",(name.strip(),description.strip(),department_id))
                else: c.execute("INSERT INTO departments(name,description) VALUES(?,?)",(name.strip(),description.strip()))
        except Exception as e:
            if "UNIQUE" in str(e): raise ValueError("A department with that name already exists.")
            raise
    def delete(self,department_id):
        with self.db.connect() as c:
            try: c.execute("DELETE FROM departments WHERE id=?",(department_id,))
            except Exception as e:
                if "FOREIGN KEY" in str(e): raise ValueError("Reassign or remove employees before deleting this department.")
                raise
