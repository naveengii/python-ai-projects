import sqlite3
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        subject TEXT,
        marks INTEGER   
    )
''')
conn.commit()
print("Table created successfully")
students_data = [
    ("Naveen","27", "Python", "85"),
    ("Abi", "23", "React", "62"),
    ("Rex", "25", "AI", "91"),
    ("Priya", "22", "SQL", "45")
]
cursor.executemany('''
    INSERT INTO students(name, age, subject, marks)
    VALUES (?, ?, ?, ?)
''',students_data)
conn.commit()
print("Records are stored in the students database")
cursor.execute('SELECT * from students')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.commit()
print("Records are printed successfully")
cursor.execute('SELECT * FROM students WHERE marks > 70')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()