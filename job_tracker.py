import sqlite3
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage , HumanMessage
def init():
    conn = sqlite3.connect('jobdata.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            status TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            ai_tip TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database is created")
init()
llm = ChatGroq(api_key="api_key", model="llama-3.3-70b-versatile")
messages = [SystemMessage(content="give one tip for applying to {role} position at  company. keep it short and pratical")]

while True:
    company = input("which company you applied :")
    if company == 'quit':
        break
    role = input("what role you applied : ")
    status = input("applied or not : ")
    messages.append(HumanMessage(content= f"give tip for {role} at {company} "))
    response = llm.invoke(messages)
    messages.append(response)
    print(response.content) 
    conn = sqlite3.connect('jobdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs(company, role, status,ai_tip)
        VALUES (?, ?, ?, ?)
    ''',(company,role,status,response.content))
    conn.commit()
    conn.close()
    print("datas are inserted.")






