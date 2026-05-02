import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

app = FastAPI()
llm = ChatGroq(api_key="api-key", model="llama-3.3-70b-versatile")

def init():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authentication(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade TEXT,
            user_name TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER ,
            question TEXT,
            ai_response TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("database is created ")
init()

class student(BaseModel):
    name : str
    grade : str
    user_name : str
    password : str

@app.post("/register")
def register(data : student):
    student_data = data.name, data.grade, data.user_name, data.password
    '''response = llm.invoke(data.name, data.grade, data.user_name, data.password)'''
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO authentication(name, grade, user_name, password)
        VALUES (?, ?, ?, ?)
    """,(student_data[0], student_data[1], student_data[2], student_data[3],))
    conn.commit()
    conn.close()
    return{"message" : "stuendent registered successfully"}

@app.post("/login")
def login(data : student):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM authentication WHERE user_name = ? AND password = ?',(data.user_name, data.password))
    row = cursor.fetchone()
    conn.commit()
    if row :
        return{"message": "login successfull" , "student_id": row[0]}
    else:
        return{"message" : "ivalid credentials"}


def student_study_docs(querry):
    return "found in docs : " + querry

def general_llm_answer(querry):
    user_question = querry
    response = llm.invoke(user_question)
    return response.content
    
def agent_decision(querry):
    decision = llm.invoke([
        SystemMessage(content="you are a router. user will ask the question . if the question like study, education, school, college reply with exactly one word : STUDY. otherwise reply : GENERAL not more than single word "),
        HumanMessage(content= querry)
    ])
    if "STUDY" in decision.content:
        return student_study_docs(querry)
    else :
        return general_llm_answer(querry)
    
class AskQuestion(BaseModel):
    student_id : int
    question : str

@app.post("/ask")
def ask(data: AskQuestion):
    response = agent_decision(data.question)
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation (student_id, question, ai_response)
        VALUES (?, ?, ?)
    """,(data.student_id, data.question, response))
    conn.commit()
    conn.close()
    return {"response" : response}

@app.get("/history/{student_id}")
def history(student_id : int):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversation WHERE student_id = ?',(student_id,))
    rows = cursor.fetchall()
    history= []
    for row in rows:
        history.append({
            "id" : row[0],
            "student_id" : row[1],
            "question" : row[2],
            "ai_response" : row[3]
        })
    return history