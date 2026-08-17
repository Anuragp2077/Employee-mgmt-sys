# 💼 Employee Payroll Management System

A desktop-based **Employee Payroll Management System** built with **Python, Tkinter, MySQL, Pandas, and Matplotlib**.

It provides a simple graphical interface for managing employee records, calculating payroll, and viewing salary and department statistics through an interactive dashboard.

---

## ✨ What does this project do?

This application is designed to make basic employee and payroll management easier.

Instead of maintaining employee records manually, the application stores them in a **MySQL database** and provides a graphical interface for working with them.

With the application, you can:

* 👤 Add employees
* ✏️ Update employee information
* 🗑️ Delete employees
* 🆔 Automatically assign employee IDs
* 💰 Calculate employee payroll
* 📊 View department-wise salary statistics
* 🥧 View employee distribution by department
* 📈 View an individual employee's salary breakdown
* 🗄️ Store employee information in MySQL

The project was created as an **Informatics Practices Class XII project**, but the code can also be used as a starting point for learning how Python applications interact with databases.

---

## 🛠️ Built With

| Technology             | Why it's used                |
| ---------------------- | ---------------------------- |
| 🐍 **Python**          | Main programming language    |
| 🖥️ **Tkinter**        | Graphical user interface     |
| 🗄️ **MySQL**          | Employee data storage        |
| 🔌 **MySQL Connector** | Connects Python to MySQL     |
| 🐼 **Pandas**          | Data processing and analysis |
| 📊 **Matplotlib**      | Charts and visualizations    |

---

# 🚀 Getting Started

Follow the steps below to run the project on your computer.

## 1. Requirements

Before starting, make sure you have:

* Python 3.x
* MySQL Server
* pip
* A working MySQL user account

You can check Python with:

```bash
python --version
```

and MySQL with:

```bash
mysql --version
```

---

## 2. Clone the Repository

```bash
git clone https://github.com/Anuragp2077/Employee-Payroll-Management-System.git
cd Employee-Payroll-Management-System
```

---

## 3. Install Python Dependencies

Run:

```bash
pip install mysql-connector-python pandas matplotlib
```

---

# 🗄️ Setting Up MySQL

The application requires a MySQL database before it can start.

Create the database:

```sql
CREATE DATABASE employee_system;
USE employee_system;
```

Then create the employee table:

```sql
CREATE TABLE employees (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(50),
    Position VARCHAR(50),
    Salary DECIMAL(10,2)
);
```

The project documentation also defines a `users` table for authentication:

```sql
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    role VARCHAR(20)
);
```

If you need the authentication table:

```sql
INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin');
```

---

# ⚙️ Configure the Database

Open `APP.py` and find:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "employee_system"
}
```

Change it to match your MySQL setup:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "employee_system"
}
```

# ▶️ Run the Application

Once MySQL is running and the database is configured:

```bash
python APP.py
```

The application should open a desktop window containing the employee management interface.

---

# 🧑‍💼 Employee Management

The **Manage Employees** section is where employee records are maintained.

You can enter:

* Name
* Department
* Position
* Salary

Then use the available actions:

### ➕ Add Employee

Creates a new employee record in the database.

The application also checks whether an employee with the same name already exists in the department.

### ✏️ Update Employee

Select an employee from the table and update their information.

### 🗑️ Delete Employee

Select an employee and delete their record.

The application asks for confirmation before deleting the record.

### 💰 Generate Payroll

Select an employee and generate their payroll calculation.

---

# 💰 Payroll Calculation

The project uses a simple predefined payroll formula.

For an employee with a basic salary of `S`:

```text
HRA = S × 10%
DA  = S × 20%
TDS = S × 5%
```

The final salary is:

```text
Net Salary = Basic Salary + HRA + DA - TDS
```

### Example

For a basic salary of:

```text
₹50,000
```

the calculation becomes:

```text
HRA = ₹5,000
DA  = ₹10,000
TDS = ₹2,500

Net Salary = ₹62,500
```

The application performs these calculations automatically.

---

# 📊 Dashboard

The **Dashboard** turns the employee data stored in MySQL into visual information.

It currently provides two main charts.

### Average Net Salary by Department

A bar chart showing the average net salary for each department.

### Employee Count by Department

A pie chart showing how employees are distributed between departments.

This makes it easier to understand the workforce without manually analyzing the database.

---

# 🥧 Individual Salary Breakdown

When payroll is generated for an employee, the application also creates a salary distribution chart.

It displays:

```text
Basic Salary
     │
     ├── HRA
     ├── DA
     └── TDS
```

This provides a visual representation of how the employee's payroll is composed.

---

# 🧠 How It Works

The application follows a simple flow:

```text
                    ┌───────────────┐
                    │    Tkinter    │
                    │      GUI      │
                    └───────┬───────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Application Logic │
                  │                   │
                  │ • CRUD            │
                  │ • Payroll         │
                  │ • Validation      │
                  │ • Calculations    │
                  └─────────┬─────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     MySQL     │
                    │    Database   │
                    └───────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Pandas +      │
                    │ Matplotlib    │
                    │               │
                    │ Charts & Data │
                    └───────────────┘
```

In simple terms:

**Tkinter → Python logic → MySQL → Pandas → Matplotlib**

---

# 📁 Project Structure

```text
Employee-Payroll-Management-System/
│
├── APP.py
├── requirements.txt
├── README.md
│
├── screenshots/
│   ├── employee-management.png
│   ├── dashboard.png
│   └── payroll.png
│
└── docs/
    └── project-report.pdf
```

### `APP.py`

The main application containing:

* GUI
* Database connection
* Employee CRUD operations
* Payroll calculations
* Dashboard generation
* Salary visualization

### `requirements.txt`

Contains the Python dependencies required by the project.

### `screenshots/`

Recommended location for screenshots used in this README.

### `docs/`

Optional location for the complete academic project report.

---

# 🗃️ Database

The main employee table contains:

| Column       | Description         |
| ------------ | ------------------- |
| `EmployeeID` | Unique employee ID  |
| `Name`       | Employee name       |
| `Department` | Employee department |
| `Position`   | Job position        |
| `Salary`     | Basic salary        |

The project documentation also defines a separate `users` table for authentication and roles.

---

# 🔐 Security Note

This project is primarily an **academic/educational application**, so the current implementation keeps the database configuration simple.

For real-world use, several things should be improved:

* Store passwords using secure hashing
* Never hard-code database passwords
* Use environment variables for credentials
* Add proper authentication
* Implement role-based permissions
* Validate all user input
* Add database access controls
* Add audit logging

**Do not use the default credentials from the academic example in a production environment.**

---

# ⚠️ Current Limitations

The current version intentionally keeps the application relatively simple.

It does **not currently implement**:

* Attendance management
* Leave management
* Dynamic government tax slabs
* Cloud deployment
* Mobile application
* Employee self-service portal

The accompanying academic report also discusses additional functionality such as authentication, admin management, PDF salary slips, and CSV export. Those features should only be considered available if their corresponding implementation is present in the version of the source code you are running.

---

# 🔮 Future Improvements

There are several directions in which this project could be developed further.

### 🌐 Web Version

Convert the desktop application into a web application using:

* Flask
* Django

### 🔐 Better Authentication

Add:

* Password hashing
* Role-based access
* Admin accounts
* HR accounts
* Employee accounts

### 🕒 Attendance & Leave

Integrate:

* Attendance
* Leave
* Overtime
* Working days

This would allow payroll to be calculated using actual attendance information.

### 🧾 Advanced Payroll

Support:

* Configurable allowances
* Government tax slabs
* Bonuses
* Overtime
* Deductions
* Multiple salary structures

### ☁️ Cloud Support

Move the database to a cloud environment so authorized users can access the application remotely.

### 📧 Email Integration

Automatically send salary slips and payroll information to employees.

### 📱 Mobile Application

Create a mobile interface where employees can view:

* Salary slips
* Payroll history
* Attendance
* Leave information

### 📈 Better Analytics

Add dashboards for:

* Monthly payroll
* Annual payroll
* Department expenditure
* Salary trends
* Employee growth
* Tax summaries

---

# 🧪 Testing

Before considering the application ready, test the following:

* [ ] MySQL connection works
* [ ] Application starts successfully
* [ ] Employee can be added
* [ ] Duplicate employee validation works
* [ ] Employee can be updated
* [ ] Employee can be deleted
* [ ] Employee IDs are generated correctly
* [ ] Payroll calculation is correct
* [ ] Net salary is displayed correctly
* [ ] Dashboard loads correctly
* [ ] Department salary chart works
* [ ] Department employee chart works
* [ ] Individual salary chart works
* [ ] Invalid input is handled
* [ ] Database errors are handled

---

# 🤝 Contributing

Want to improve the project?

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/my-new-feature
```

3. Make your changes
4. Test the application
5. Commit your changes

```bash
git add .
git commit -m "Add new feature"
```

6. Push your branch

```bash
git push origin feature/my-new-feature
```

7. Open a Pull Request

---

# 📚 What I Learned From This Project

This project demonstrates practical experience with:

* Python
* Tkinter GUI development
* MySQL
* SQL queries
* Database connectivity
* CRUD operations
* Data validation
* Payroll calculations
* Pandas
* Matplotlib
* Data visualization
* Error handling
* Database-driven applications

It also demonstrates how different technologies can work together to build a complete desktop application.

---

# 🎓 About the Project

This project was developed as an **Informatics Practices (065) Class XII project** for the **2025–2026 academic session** at **Sagar Public School, Rohit Nagar, Bhopal**.

The accompanying project report describes the application as an Employee Management / Payroll Management System designed to automate employee record management and payroll-related operations.

---

# 👨‍💻 Author

**Anurag Pandey**

Class XII
Sagar Public School, Rohit Nagar, Bhopal

---

# ⭐ Support

If you found this project useful or helpful for learning:

**Give the repository a ⭐ on GitHub!**

---

<p align="center">
  Made with ❤️ using Python
</p>
