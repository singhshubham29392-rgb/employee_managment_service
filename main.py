import logging, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from app.config import APP_NAME, LOG_PATH
from app.database import Database
from app.auth import create_admin, authenticate
from app.services.employee_service import EmployeeService
from app.services.department_service import DepartmentService
from app.services.report_service import export_csv, employee_html

class App:
    def __init__(self, root):
        self.root=root; self.root.title(APP_NAME); self.root.geometry("1200x760"); self.root.minsize(900,600)
        self.db=Database(); self.employees=EmployeeService(self.db); self.departments=DepartmentService(self.db)
        self.style=ttk.Style(); self.style.theme_use("clam"); self.style.configure("Treeview",rowheight=30,background="white",fieldbackground="white",font=("Segoe UI",10)); self.style.configure("Treeview.Heading",font=("Segoe UI",10,"bold"))
        self.root.configure(bg="#f2f5f9"); self.login()
    def clear(self):
        for w in self.root.winfo_children(): w.destroy()
    def field(self,parent,label,initial="",width=32):
        box=ttk.Frame(parent); ttk.Label(box,text=label).pack(anchor="w"); v=tk.StringVar(value=initial); ttk.Entry(box,textvariable=v,width=width).pack(fill="x",pady=(4,12)); return box,v
    def login(self):
        self.clear(); frame=ttk.Frame(self.root,padding=40); frame.place(relx=.5,rely=.5,anchor="center"); setup=not self.db.has_admin()
        ttk.Label(frame,text=APP_NAME,font=("Segoe UI",22,"bold")).pack(pady=(0,8)); ttk.Label(frame,text="Create your administrator account" if setup else "Administrator sign in").pack(pady=(0,20))
        _,user=self.field(frame,"Username"); _.pack(fill="x"); _,pw=self.field(frame,"Password"); _.pack(fill="x"); pw_entry=frame.winfo_children()[-1].winfo_children()[-1]; pw_entry.configure(show="•")
        if setup:
            _,confirm=self.field(frame,"Confirm password"); _.pack(fill="x"); frame.winfo_children()[-1].winfo_children()[-1].configure(show="•")
        def submit():
            try:
                if setup:
                    if pw.get()!=confirm.get(): raise ValueError("Passwords do not match.")
                    create_admin(self.db,user.get(),pw.get())
                elif not authenticate(self.db,user.get(),pw.get()): raise ValueError("Username or password is incorrect.")
                self.home()
            except ValueError as e: messagebox.showerror("Sign in",str(e),parent=self.root)
            except Exception: logging.exception("Authentication failure"); messagebox.showerror("Error","Unable to complete sign in. See the local application log.",parent=self.root)
        ttk.Button(frame,text="Create administrator" if setup else "Sign in",command=submit).pack(fill="x",pady=10)
    def home(self):
        self.clear(); self.shell=ttk.Frame(self.root); self.shell.pack(fill="both",expand=True)
        nav=tk.Frame(self.shell,bg="#142b4a",width=220); nav.pack(side="left",fill="y"); nav.pack_propagate(False)
        tk.Label(nav,text="PEOPLE\nMANAGEMENT",bg="#142b4a",fg="white",font=("Segoe UI",17,"bold"),justify="left").pack(anchor="w",padx=22,pady=28)
        for label,fn in [("Dashboard",self.dashboard),("Employees",self.employee_page),("Departments",self.department_page),("Reports",self.report_page),("Settings",self.settings_page),("Logout",self.login)]:
            tk.Button(nav,text=label,command=fn,anchor="w",bg="#142b4a",fg="white",activebackground="#25476f",activeforeground="white",relief="flat",font=("Segoe UI",11),padx=22,pady=12).pack(fill="x")
        self.content=ttk.Frame(self.shell,padding=26); self.content.pack(side="left",fill="both",expand=True); self.dashboard()
    def page(self,title,subtitle=""):
        for w in self.content.winfo_children(): w.destroy()
        ttk.Label(self.content,text=title,font=("Segoe UI",23,"bold"),foreground="#172b49").pack(anchor="w")
        if subtitle: ttk.Label(self.content,text=subtitle,foreground="#627086").pack(anchor="w",pady=(4,18))
        body=ttk.Frame(self.content); body.pack(fill="both",expand=True,pady=(12,0)); return body
    def dashboard(self):
        b=self.page("Dashboard","Live workforce overview")
        s=self.employees.stats(); cards=ttk.Frame(b); cards.pack(fill="x")
        for label,key in [("Total employees","total"),("Active","active"),("On leave","leave"),("Resigned","resigned"),("Departments","departments")]:
            card=ttk.LabelFrame(cards,text=label,padding=18); card.pack(side="left",fill="both",expand=True,padx=(0,8)); ttk.Label(card,text=str(s[key]),font=("Segoe UI",24,"bold")).pack(anchor="w")
        lower=ttk.Frame(b); lower.pack(fill="both",expand=True,pady=20); recent=ttk.LabelFrame(lower,text="Recent additions",padding=12); recent.pack(side="left",fill="both",expand=True,padx=(0,12))
        if s["recent"]:
            for r in s["recent"]: ttk.Label(recent,text=f"{r['employee_code']}   {r['full_name']}   {r['joining_date']}").pack(anchor="w",pady=7)
        else: ttk.Label(recent,text="No employee records yet. Add an employee to see dashboard data.").pack(anchor="w")
        charts=ttk.LabelFrame(lower,text="Employees by department",padding=12); charts.pack(side="left",fill="both",expand=True)
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig=Figure(figsize=(4.8,3.2),dpi=90); ax=fig.add_subplot(111); labels=[r["name"] for r in s["by_department"] if r["n"]]; vals=[r["n"] for r in s["by_department"] if r["n"]]
            if vals: ax.bar(labels,vals,color="#3c78b5"); ax.tick_params(axis="x",rotation=25); fig.tight_layout(); canvas=FigureCanvasTkAgg(fig,master=charts); canvas.draw(); canvas.get_tk_widget().pack(fill="both",expand=True)
            else: ttk.Label(charts,text="Charts appear when employees are added.").pack()
        except ImportError: ttk.Label(charts,text="Install Matplotlib to enable dashboard charts.").pack()
    def employee_page(self):
        b=self.page("Employees","Search, filter and manage employee records")
        bar=ttk.Frame(b); bar.pack(fill="x",pady=(0,12)); q=tk.StringVar(); dep=tk.StringVar(); stat=tk.StringVar()
        ttk.Entry(bar,textvariable=q,width=30).pack(side="left"); ttk.Label(bar,text=" Search ID, name, email or phone").pack(side="left")
        dnames=[r["name"] for r in self.departments.list()]; ttk.Combobox(bar,textvariable=dep,values=[""]+dnames,state="readonly",width=20).pack(side="left",padx=8); ttk.Combobox(bar,textvariable=stat,values=["","Active","On Leave","Resigned"],state="readonly",width=14).pack(side="left")
        cols=("employee_code","full_name","email","phone","department","designation","joining_date","status"); tree=ttk.Treeview(b,columns=cols,show="headings");
        for c in cols: tree.heading(c,text=c.replace("_"," ").title(),command=lambda col=c:self.sort_tree(tree,col,False)); tree.column(c,width=110)
        tree.pack(fill="both",expand=True)
        def refresh(*_):
            tree.delete(*tree.get_children())
            for i,r in enumerate(self.employees.list(q.get(),dep.get(),stat.get())): tree.insert("","end",iid=str(r["id"]),values=tuple(r[c] for c in cols),tags=("odd" if i%2 else "even",))
            tree.tag_configure("odd",background="#f0f4f9")
        q.trace_add("write",refresh); dep.trace_add("write",refresh); stat.trace_add("write",refresh); refresh()
        actions=ttk.Frame(b); actions.pack(fill="x",pady=12)
        def selected():
            item=tree.selection()
            if not item: messagebox.showinfo("Select employee","Select an employee first.",parent=self.root); return None
            return int(item[0])
        ttk.Button(actions,text="Add employee",command=lambda:self.employee_form(refresh)).pack(side="left",padx=4)
        ttk.Button(actions,text="View profile",command=lambda: self.profile(selected())).pack(side="left",padx=4)
        ttk.Button(actions,text="Edit",command=lambda: self.employee_form(refresh,selected())).pack(side="left",padx=4)
        def delete():
            eid=selected()
            if eid:
                r=self.employees.get(eid)
                if messagebox.askyesno("Confirm deletion",f"Delete {r['full_name']} ({r['employee_code']})? This cannot be undone.",parent=self.root): self.employees.delete(eid); refresh(); self.dashboard()
        ttk.Button(actions,text="Delete",command=delete).pack(side="left",padx=4); ttk.Button(actions,text="Refresh",command=refresh).pack(side="right")
    def sort_tree(self,tree,col,reverse):
        data=[(tree.set(k,col),k) for k in tree.get_children("")]; data.sort(reverse=reverse)
        for ix,(_,k) in enumerate(data): tree.move(k,"",ix)
        tree.heading(col,command=lambda:self.sort_tree(tree,col,not reverse))
    def employee_form(self,refresh,employee_id=None):
        old=self.employees.get(employee_id) if employee_id else None; win=tk.Toplevel(self.root); win.title("Edit employee" if old else "Add employee"); win.geometry("720x700"); win.transient(self.root); win.grab_set()
        canvas=tk.Canvas(win,highlightthickness=0); scroll=ttk.Scrollbar(win,orient="vertical",command=canvas.yview); form=ttk.Frame(canvas,padding=22); canvas.create_window((0,0),window=form,anchor="nw"); canvas.configure(yscrollcommand=scroll.set); canvas.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y"); form.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        vars={}; fields=[("full_name","Full name"),("email","Email"),("phone","Phone"),("gender","Gender (optional)"),("date_of_birth","Date of birth YYYY-MM-DD"),("address","Address"),("designation","Designation"),("joining_date","Joining date YYYY-MM-DD"),("salary","Salary"),("emergency_contact","Emergency contact"),("notes","Notes")]
        for key,label in fields:
            box,v=self.field(form,label,old[key] if old and old[key] is not None else ""); box.pack(fill="x"); vars[key]=v
        depv=tk.StringVar(); deps=self.departments.list(); combo=ttk.Frame(form); ttk.Label(combo,text="Department").pack(anchor="w"); depbox=ttk.Combobox(combo,textvariable=depv,values=[d["name"] for d in deps],state="readonly"); depbox.pack(fill="x",pady=(4,12)); combo.pack(fill="x")
        if old:
            for d in deps:
                if d["id"]==old["department_id"]: depv.set(d["name"])
        elif deps: depv.set(deps[0]["name"])
        status=tk.StringVar(value=old["status"] if old else "Active"); box=ttk.Frame(form); ttk.Label(box,text="Employment status").pack(anchor="w"); ttk.Combobox(box,textvariable=status,values=["Active","On Leave","Resigned"],state="readonly").pack(fill="x",pady=(4,12)); box.pack(fill="x")
        def save():
            try:
                dm={d["name"]:d["id"] for d in deps}; data={k:v.get().strip() for k,v in vars.items()}; data.update(department_id=dm.get(depv.get()),status=status.get())
                self.employees.save(data,employee_id); messagebox.showinfo("Saved","Employee record saved.",parent=win); win.destroy(); refresh()
            except ValueError as e: messagebox.showerror("Check employee details",str(e),parent=win)
            except Exception: logging.exception("Employee save failure"); messagebox.showerror("Error","Could not save the employee record. Check email uniqueness and the application log.",parent=win)
        ttk.Button(form,text="Save employee",command=save).pack(anchor="e")
    def profile(self,eid):
        if not eid:return
        r=self.employees.get(eid)
        if not r:return
        from app.services.employee_service import EmployeeService
        row=dict(r); row["department"]=next((d["name"] for d in self.departments.list() if d["id"]==r["department_id"]),"")
        path=filedialog.asksaveasfilename(parent=self.root,title="Save printable employee profile",defaultextension=".html",filetypes=[("HTML document","*.html")],initialfile=f"{row['employee_code']}-profile.html")
        if path:
            try:
                Path(path).write_text(employee_html(row),encoding="utf-8"); import webbrowser; webbrowser.open(Path(path).as_uri())
            except OSError: logging.exception("Profile export failed"); messagebox.showerror("Export failed","Could not write the profile file.",parent=self.root)
    def department_page(self):
        b=self.page("Departments","Manage department names and descriptions")
        tree=ttk.Treeview(b,columns=("name","description","employee_count"),show="headings")
        for c in ("name","description","employee_count"): tree.heading(c,text=c.replace("_"," ").title()); tree.column(c,width=240)
        tree.pack(fill="both",expand=True)
        def refresh():
            tree.delete(*tree.get_children())
            for d in self.departments.list(): tree.insert("","end",iid=str(d["id"]),values=(d["name"],d["description"],d["employee_count"]))
        def edit(_=None):
            sel=tree.selection(); old=next((d for d in self.departments.list() if str(d["id"])==sel[0]),None) if sel else None
            win=tk.Toplevel(self.root); win.title("Edit department" if old else "Add department"); f=ttk.Frame(win,padding=20); f.pack(fill="both",expand=True); _,name=self.field(f,"Name",old["name"] if old else ""); _.pack(fill="x"); _,desc=self.field(f,"Description",old["description"] if old else ""); _.pack(fill="x")
            def save():
                try:self.departments.save(name.get(),desc.get(),old["id"] if old else None);win.destroy();refresh()
                except ValueError as e:messagebox.showerror("Department",str(e),parent=win)
            ttk.Button(f,text="Save",command=save).pack(anchor="e")
        actions=ttk.Frame(b); actions.pack(fill="x",pady=12); ttk.Button(actions,text="Add department",command=edit).pack(side="left",padx=4); ttk.Button(actions,text="Edit selected",command=edit).pack(side="left",padx=4)
        def delete():
            if not tree.selection():return
            try:self.departments.delete(int(tree.selection()[0]));refresh()
            except ValueError as e:messagebox.showerror("Department",str(e),parent=self.root)
        ttk.Button(actions,text="Delete selected",command=delete).pack(side="left",padx=4); refresh()
    def report_page(self):
        b=self.page("Reports","Export the current employee directory or filtered report as CSV")
        ttk.Label(b,text="Export includes employee ID, name, work email and phone, department, designation, joining date, status and salary.",wraplength=650).pack(anchor="w",pady=12)
        filters=ttk.Frame(b); filters.pack(anchor="w",pady=8); q=tk.StringVar(); department=tk.StringVar(); status=tk.StringVar()
        ttk.Label(filters,text="Search").grid(row=0,column=0,sticky="w"); ttk.Entry(filters,textvariable=q,width=28).grid(row=1,column=0,padx=(0,10))
        ttk.Label(filters,text="Department").grid(row=0,column=1,sticky="w"); ttk.Combobox(filters,textvariable=department,values=[""]+[d["name"] for d in self.departments.list()],state="readonly",width=23).grid(row=1,column=1,padx=(0,10))
        ttk.Label(filters,text="Employment status").grid(row=0,column=2,sticky="w"); ttk.Combobox(filters,textvariable=status,values=["","Active","On Leave","Resigned"],state="readonly",width=18).grid(row=1,column=2)
        ttk.Button(b,text="Export filtered report to CSV",command=lambda:self.export(q.get(),department.get(),status.get())).pack(anchor="w",pady=8)
        ttk.Label(b,text="Leave filters blank for the complete directory. Department and status filters generate department-wise and employment-status reports; search supports employee ID, name, email and phone. Joining-date data is included in each exported row.",wraplength=680).pack(anchor="w",pady=8)
        ttk.Label(b,text="For an individual printable profile, open Employees, select a record and choose View profile.").pack(anchor="w",pady=12)
    def export(self,query="",department="",status=""):
        path=filedialog.asksaveasfilename(parent=self.root,title="Export employees",defaultextension=".csv",filetypes=[("CSV file","*.csv")])
        if path:
            try:export_csv(self.employees.list(query,department,status),path);messagebox.showinfo("Export complete",f"Employee report saved to:\n{path}",parent=self.root)
            except OSError:logging.exception("CSV export failed");messagebox.showerror("Export failed","Could not write the CSV file. Check the destination and permissions.",parent=self.root)
    def settings_page(self):
        b=self.page("Settings","Local application information and data protection")
        from app.config import DB_PATH
        ttk.Label(b,text=f"Database location:\n{DB_PATH}",wraplength=700).pack(anchor="w",pady=8)
        ttk.Label(b,text="Back up by closing the application and copying employees.sqlite3 to a secure location. Restore by replacing that file while the application is closed. The database is local; use a strong administrator password and restrict access to your Windows account.",wraplength=700).pack(anchor="w",pady=10)
        ttk.Button(b,text="Log out",command=self.login).pack(anchor="w",pady=10)

def main():
    LOG_PATH.parent.mkdir(parents=True,exist_ok=True); logging.basicConfig(filename=LOG_PATH,level=logging.ERROR,format="%(asctime)s %(levelname)s %(message)s")
    root=tk.Tk(); App(root); root.mainloop()
if __name__=="__main__":main()
