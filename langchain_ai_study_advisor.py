from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import sqlite3

def init_db():
    conn = sqlite3.connect('ai_study_advisor')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

llm = ChatGroq(api_key="api_key", model="llama-3.3-70b-versatile")
messages = [SystemMessage(content = " you are an mentor for student ")]
init_db()
while True:
    user_input = input("you : ")
    if user_input == "quit":
        break
    messages.append(HumanMessage(content= user_input))
    response = llm.invoke(messages)
    messages.append(response)
    print(response.content)
    conn = sqlite3.connect('ai_study_advisor')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_logs(user_input, ai_response)
        VALUES (?,?)
    ''', (user_input, response.content))
    conn.commit()
    conn.close()




    