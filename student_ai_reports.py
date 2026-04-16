
import sqlite3
import requests

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS add_student(
            name TEXT,
            subject TEXT,
            marks INTEGER,
            grade TEXT,
            ai_feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
students_data = [
    ("Naveen", "Python", 85),
    ("Abi", "React", 52),
    ("Rex", "AI", 41),
    ("Priya", "SQL", 45)
]
print("student datas are added.")
def add_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO add_student(name, subject, marks)
        VALUES(?, ?, ?)
    ''', students_data)
    conn.commit()
    conn.close()
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = "api_key"
GROQ_HEADERS = {
    "Authorization" : f"Bearer {GROQ_KEY}",
    "Content-Type" : "application/json"
}
SYSTEM_PROMPT = "you are an assistant this program. you need to give the feedback for each student. should be little hard, motivate and make it short"

for student in students_data:
    print(student)
    init_db()
    if student[2] > 80:
        result = 'A'
    elif student[2] > 60:
        result = 'B'
    elif student[2] > 40:
        result = 'C'
    else :
        result = 'F'
    print (f"{student[0]} | {student[1]} | {student[2]} | {result}")
    user_message = user_message = f"Student {student[0]} scored {student[2]} in {student[1]} and got grade {result}"
    data = {
        "model" : "llama-3.3-70b-versatile",
        "messages" : [
            {"role" : "system" , "content" : SYSTEM_PROMPT},
            {"role" : "user" , "content" : user_message}
        ]
    }
    response = requests.post(GROQ_URL, headers=GROQ_HEADERS, json=data)
    ai_result = response.json()
    ai_feedback = ai_result['choices'][0]['message']['content']
    print(ai_feedback)

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO add_student(name, subject, marks ,grade, ai_feedback)
        VALUES (?,?,?,?,?)
    ''',(student[0],student[1],student[2],result,ai_feedback))
    conn.commit()
    conn.close()
print("Database ready!")


