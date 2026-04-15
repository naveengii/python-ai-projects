import sqlite3

conn = sqlite3.connect('artik.db')
cursor = conn.cursor()
cursor.execute('''
    create table if not exists contacts(
        id integer primary key autoincrement,
        name text,
        phone text,
        email text,
        message text
    )
''')
conn.commit()
print("Database and table created successfully")

cursor.execute('DELETE from contacts')
cursor.execute('''
    INSERT INTO contacts(name, phone, email, message)
    VALUES (?,?,?,?)
''', ("naveen", "9876543021", "naveen@gmail.com", "i need software development"))

conn.commit()
print("Data inserted successfully")

cursor.execute('SELECT * from contacts')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()