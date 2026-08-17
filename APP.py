import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as sql
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- DB CONFIG ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "employee_system"
}

conn = None
try:
    conn = sql.connect(**DB_CONFIG)
except Error as e:
    messagebox.showerror("DB Error", f"Cannot connect to database: {e}")
    exit()

# ---------------- Utility Functions ----------------
def get_next_emp_id():
    cur = conn.cursor()
    cur.execute("SELECT ID FROM available_ids ORDER BY ID LIMIT 1")
    row = cur.fetchone()
    if row:
        next_id = row[0]
        cur.execute("DELETE FROM available_ids WHERE ID=%s", (next_id,))
    else:
        cur.execute("SELECT MAX(EmployeeID) FROM employees")
        max_id = cur.fetchone()[0]
        next_id = 1 if max_id is None else max_id + 1
    conn.commit()
    cur.close()
    return next_id

def calculate_payroll(salary):
    salary = float(salary)
    hra = 0.1 * salary
    da = 0.2 * salary
    tax = 0.05 * salary
    net = salary + hra + da - tax
    return hra, da, tax, net

def clear_inputs():
    name_var.set("")
    dept_var.set("")
    pos_var.set("")
    salary_var.set("")

# ---------------- CRUD Operations ----------------
def add_employee():
    name = name_var.get().strip()
    dept = dept_var.get().strip()
    pos = pos_var.get().strip()
    salary = salary_var.get().strip()
    if not (name and dept and pos and salary):
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM employees WHERE Name=%s AND Department=%s", (name, dept))
        if cur.fetchone():
            cur.close()
            messagebox.showwarning("Duplicate", f"{name} already exists in {dept}.")
            return
        emp_id = get_next_emp_id()
        cur.execute("INSERT INTO employees (EmployeeID, Name, Department, Position, Salary) VALUES (%s,%s,%s,%s,%s)",
                    (emp_id, name, dept, pos, float(salary)))
        conn.commit()
        cur.close()
        messagebox.showinfo("Added", f"Employee {name} added with ID {emp_id}.")
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_employee():
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Select", "Select an employee to update.")
        return
    vals = tree.item(sel)["values"]
    emp_id = vals[0]
    name = name_var.get().strip() or vals[1]
    dept = dept_var.get().strip() or vals[2]
    pos = pos_var.get().strip() or vals[3]
    salary = salary_var.get().strip() or vals[4]
    try:
        cur = conn.cursor()
        cur.execute("UPDATE employees SET Name=%s, Department=%s, Position=%s, Salary=%s WHERE EmployeeID=%s",
                    (name, dept, pos, float(salary), emp_id))
        conn.commit()
        cur.close()
        messagebox.showinfo("Updated", f"Employee ID {emp_id} updated.")
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_employee():
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Select", "Select an employee to delete.")
        return
    emp_id = tree.item(sel)["values"][0]
    if not messagebox.askyesno("Confirm Delete", f"Delete Employee ID {emp_id}?"):
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE EmployeeID=%s", (emp_id,))
        cur.execute("INSERT INTO available_ids (ID) VALUES (%s)", (emp_id,))
        conn.commit()
        cur.close()
        messagebox.showinfo("Deleted", f"Employee ID {emp_id} deleted.")
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- Dashboard / Pie Chart ----------------
individual_pie_canvas = None
dashboard_canvases = []

def clear_dashboard():
    global dashboard_canvases, individual_pie_canvas
    for c in dashboard_canvases:
        c.get_tk_widget().destroy()
    dashboard_canvases = []
    if individual_pie_canvas:
        individual_pie_canvas.get_tk_widget().destroy()
        individual_pie_canvas = None

def update_dashboard():
    clear_dashboard()
    df = pd.read_sql("SELECT Department, Salary, EmployeeID FROM employees", conn)
    if df.empty:
        return
    df['HRA'] = df['Salary']*0.1
    df['DA'] = df['Salary']*0.2
    df['TDS'] = df['Salary']*0.05
    df['NetSalary'] = df['Salary'] + df['HRA'] + df['DA'] - df['TDS']

    grp = df.groupby("Department")["NetSalary"].mean()
    fig1, ax1 = plt.subplots(figsize=(4,3))
    grp.plot(kind="bar", ax=ax1, color="#4CAF50")
    ax1.set_title("Avg Net Salary by Department")
    canvas1 = FigureCanvasTkAgg(fig1, dashboard_tab)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)
    dashboard_canvases.append(canvas1)

    grp2 = df.groupby("Department")["EmployeeID"].count()
    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.pie(grp2, labels=grp2.index, autopct="%1.1f%%", startangle=90,
            colors=["#2196F3","#FF9800","#f44336","#9C27B0"])
    ax2.set_title("Employee Count by Department")
    canvas2 = FigureCanvasTkAgg(fig2, dashboard_tab)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, padx=10, pady=10)
    dashboard_canvases.append(canvas2)

def update_individual_pie(emp_id, salary, hra, da, tax):
    global individual_pie_canvas
    if individual_pie_canvas:
        individual_pie_canvas.get_tk_widget().destroy()
    labels = ["Basic Salary","HRA","DA","TDS"]
    values = [salary, hra, da, tax]
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90,
           colors=["#4CAF50","#2196F3","#FF9800","#f44336"])
    ax.set_title(f"Employee ID {emp_id} Salary Distribution")
    individual_pie_canvas = FigureCanvasTkAgg(fig, manage_tab)
    individual_pie_canvas.draw()
    individual_pie_canvas.get_tk_widget().grid(row=4, column=4, rowspan=6, padx=10, pady=10)

def generate_payroll():
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Select", "Select an employee to generate payroll.")
        return
    emp_id, name, dept, pos, salary, _ = tree.item(sel)["values"]
    hra, da, tax, net = calculate_payroll(salary)
    messagebox.showinfo("Payroll Generated",
        f"Employee: {name}\nBasic: ₹{salary}\nHRA: ₹{hra}\nDA: ₹{da}\nTDS: ₹{tax}\nNet: ₹{net}")
    update_individual_pie(emp_id, float(salary), hra, da, tax)
    refresh_tree()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Employee Payroll Management System")
root.geometry("1200x700")

tab_control = ttk.Notebook(root)
manage_tab = ttk.Frame(tab_control)
dashboard_tab = ttk.Frame(tab_control)
tab_control.add(manage_tab, text="Manage Employees")
tab_control.add(dashboard_tab, text="Dashboard")
tab_control.pack(expand=1, fill="both")

# Input Fields
name_var = tk.StringVar()
dept_var = tk.StringVar()
pos_var = tk.StringVar()
salary_var = tk.StringVar()

tk.Label(manage_tab, text="Name").grid(row=0,column=0,padx=5,pady=5)
tk.Entry(manage_tab, textvariable=name_var).grid(row=0,column=1,padx=5,pady=5)
tk.Label(manage_tab, text="Department").grid(row=0,column=2,padx=5,pady=5)
tk.Entry(manage_tab, textvariable=dept_var).grid(row=0,column=3,padx=5,pady=5)
tk.Label(manage_tab, text="Position").grid(row=1,column=0,padx=5,pady=5)
tk.Entry(manage_tab, textvariable=pos_var).grid(row=1,column=1,padx=5,pady=5)
tk.Label(manage_tab, text="Salary").grid(row=1,column=2,padx=5,pady=5)
tk.Entry(manage_tab, textvariable=salary_var).grid(row=1,column=3,padx=5,pady=5)

# Buttons
tk.Button(manage_tab, text="Add Employee", command=add_employee, bg="#4CAF50", fg="white").grid(row=2,column=0,padx=5,pady=5)
tk.Button(manage_tab, text="Update Employee", command=update_employee, bg="#2196F3", fg="white").grid(row=2,column=1,padx=5,pady=5)
tk.Button(manage_tab, text="Delete Employee", command=delete_employee, bg="#f44336", fg="white").grid(row=2,column=2,padx=5,pady=5)
tk.Button(manage_tab, text="Generate Payroll", command=generate_payroll, bg="#FF9800", fg="white").grid(row=2,column=3,padx=5,pady=5)

# Treeview
tree = ttk.Treeview(manage_tab, columns=("ID","Name","Department","Position","Salary","Net Salary"), show="headings", height=15)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=3, column=0, columnspan=4, padx=5,pady=5)

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25, font=("Arial",10))
style.map('Treeview', background=[('selected','#90CAF9')])

def refresh_tree():
    for r in tree.get_children():
        tree.delete(r)
    cur = conn.cursor()
    cur.execute("SELECT EmployeeID, Name, Department, Position, Salary FROM employees ORDER BY EmployeeID")
    rows = cur.fetchall()
    for i, row in enumerate(rows):
        hra, da, tax, net = calculate_payroll(row[4])
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], round(net,2)))
    cur.close()
    update_dashboard()
    clear_inputs()

refresh_tree()
root.mainloop()