from fastapi import FastAPI
import sqlite3
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel

app = FastAPI()
llm = ChatGroq(api_key="api-key", model="llama-3.3-70b-versatile")
prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. Answer only from the context , dont use any outside knowledge. say "i don't have the information".
context : {context}
question : {question}
""")
chain = prompt | llm
loader = TextLoader('artik_info.txt')
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 20)
chunks = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name= "all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings)
print("vector db is done!")
def init():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            ai_response TEXT
        )
    ''')
    conn.commit()
    conn.close()
init()
class question(BaseModel):
    question : str
@app.post("/ask")
def ask_question(data : question):
    user_question = data.question
    results = vectorstore.similarity_search(user_question, k=2)
    context = "\n".join([r.page_content for r in results])
    response = chain.invoke({"context": context, "question" : user_question})
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history(question, ai_response)
        VALUES (?, ?)
    ''',(user_question, response.content))
    conn.commit()
    conn.close()
    return {"answer": response.content}
@app.get("/history")
def get_history():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_history')
    rows = cursor.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "question" : row[1],
            "ai_response" : row[2]
        })
    return history
