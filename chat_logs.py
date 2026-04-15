import sqlite3
conn = sqlite3.connect('aichat.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
chats = [
    ("what service you provide", "we provide software service, development service and ai generation"),
    ("where is you location","kalapatti, coimbatore , tamilnadu"),
    ("who are all you clients", "dev solar, social engineering, and ai service based company")
]
cursor.executemany('''
    INSERT INTO chat(user_message , ai_response)
    VALUES (?, ?)
''',chats
)
conn.commit()
print("datas are feeded")
cursor.execute('SELECT * FROM chat')
rows = cursor.fetchall()
for row in rows:
    print(row)
print("printed all details")
print("identifying the word service")
cursor.execute('SELECT * FROM chat WHERE user_message LIKE "%service%"')
rows = cursor.fetchall()
for row in rows:
    print(row)