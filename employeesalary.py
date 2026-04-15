import sqlite3
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER,
        joining_year INTEGER    
    )
''')
conn.commit()
print("Table created successfully")
emp_table = [
    ("naveen", "engineering", "51000", "2026"),
    ("abi", "diploma", "75000", "2025"),
    ("rex", "engineering", "38000", "2021"),
    ("ramya", "engineering", "98000","2020"),
    ("vinoth", "arts", "150000", "2022")
]
cursor.executemany('''
    INSERT INTO employees(name, department, salary, joining_year)
    VALUES(?, ?, ?, ?)
''',emp_table
)
conn.commit()
print("records are inserted")
cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.execute('SELECT * FROM employees WHERE department = "engineering" AND salary > 50000')
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.execute('SELECT SUM(salary) FROM employees')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.commit()
conn.close()