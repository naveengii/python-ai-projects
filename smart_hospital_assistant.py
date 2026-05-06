from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage , HumanMessage
import sqlite3
from pydantic import BaseModel
from fastapi import FastAPI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

app = FastAPI()
llm = ChatGroq(api_key="api-key", model="llama-3.3-70b-versatile")

def rag_setup():
    loader1 = TextLoader('fake_patients.txt')
    loader2 = TextLoader('drug_database.txt')
    document = loader1.load() + loader2.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 15)
    chunks = splitter.split_documents(document)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever()
    return retriever
retriever = rag_setup()

def init():
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            user_name TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_id INTEGER,
            age INTEGER,
            blood_group TEXT,
            treatment TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            question TEXT,
            ai_response TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("database is created")

init()

def router(querry):
    decision = llm.invoke([
        SystemMessage(content=""" You are a router. If the question is about patients, medications, or hospital records reply with exactly: HOSPITAL. Otherwise reply with exactly: GENERAL"""),
        HumanMessage(content=querry)
    ])
    if "HOSPITAL" in decision.content:
        return rag_node(querry)
    return general_node(querry)

def rag_node(querry):
    docs = retriever.invoke(querry)
    if docs:
        return docs[0].page_content
    return "i dont have the information"

def general_node(querry):
    response = llm.invoke(querry)
    return response.content

class doctors(BaseModel):
    user_name : str
    password : str
    name : str

@app.post("/register")
def register(data : doctors):
    doctors_data = data.name, data.user_name, data.password
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors(name, user_name, password)
        VALUES (?, ?, ?)
    """,(doctors_data[0], doctors_data[1], doctors_data[2]))
    conn.commit()
    conn.close()
    return{"response" : "user logged in successfully"}

@app.post("/login")
def login(data:doctors):
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doctors WHERE user_name = ? AND password = ?',(data.user_name, data.password))
    row = cursor.fetchone()
    conn.commit()
    if row :
        return{"response" : "login successfully", "doctors_id" : row[0]}
    else:
        return{"response" : "invalid username or password"}
    
class patient (BaseModel):
    patient_name : str
    age : int
    blood_group : str
    treatment : str
    doctor_id : int

@app.post("/add_patient")
def add_patient (data : patient):
    patient_data = data.patient_name, data.age, data.blood_group, data.treatment, data.doctor_id
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (patient_name, age, blood_group, treatment, doctor_id)
        VALUES (?, ?, ?, ?, ?)
    """,(patient_data[0], patient_data[1], patient_data[2], patient_data[3], patient_data[4]))
    conn.commit()
    conn.close()
    return{"response" : "patient datas are added successful"}

@app.get("/patients")
def get_patients():
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    rows = cursor.fetchall()
    conn.close()
    return rows

class ask_question(BaseModel):
    question : str
    doctor_id : int

@app.post("/ask")
def user_question(data: ask_question):
    response = router(data.question)
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation(doctor_id, question, ai_response)
        VALUES (?, ?, ?)
    """,(data.doctor_id, data.question, response))
    conn.commit()
    conn.close()
    return {"response" : response}

@app.get("/history/{doctor_id}")
def history(doctor_id : int):
    conn = sqlite3.connect('hospital_docs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversation WHERE doctor_id = ?', (doctor_id,))
    rows = cursor.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "doctor_id" : row[1],
            "question" : row[2],
            "ai_response" : row[3]
        })
    return history