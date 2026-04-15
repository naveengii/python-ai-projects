import sqlite3
from flask import flash , request, jsonify
from flask_cors import CORS

app = flash(__name__)
CORS(app)

def init_i():
    conn = sqlite3.connect('artik.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            mail TEXT,
            company TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
@app.route ('/submit-form', methods=['POST'])
def submit_form():
    data = request.json()
    conn = sqlite3.connect('artik.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts(name , phone, mail, company, message)
        VALUES(?, ?, ?, ?, ?)
    ''',(
        data.get('name'),
        data.get('phone'),
        data.get('mail'),
        data.get('company'),
        data.get('message')
        )
    )