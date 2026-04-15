import sqlite3
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    conn =sqlite3.connect('artik1.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            company TEXT,
            service TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Table is created")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = "your_groq_key"
GROQ_HEADERS = {
    "Authorization" : f"Bearer {GROQ_KEY}",
    "Content-Type" : "application/json"
}
SYSTEM_PROMPT = """Yor are Artik assisant of Artik Global Technology . Services : custom software development, app development, ai integration. Location: coimbatore,tamilnadu. Contact : infor@artikglobal.com +91 9876500032. Be professional and friendly , keep response short"""

@app.route('/chat', methods = ['POST'])
def chat():
    user_message = request.json.get('message','')
    data = {
        "model" :"llama-3.3-70b-versatile",
        "messages" :[
            {"role" : "system", "content": SYSTEM_PROMPT},
            {"role" : "user" , "content" : user_message}
        ] 
    }
    response = requests.post(GROQ_URL, headers=GROQ_HEADERS, json=data)
    result = response.json()
    print(result)
    ai_response = result['choices'][0]['message']['content']
    conn = sqlite3.connect('artik1.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_logs (user_message,ai_response)
        VALUES (?, ?)
    ''', (user_message,ai_response)
    )
    conn.commit()
    conn.close()
    return jsonify({"response" : ai_response})

print("Flask is now ready")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)