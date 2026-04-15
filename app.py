import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('artik.db')
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
    conn.commit()
    conn.close()
@app.route('/submit-form', methods = ['POST'])
def submit_form():
    data = request.json
    conn = sqlite3.connect('artik.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts(name, phone, email, company, service, message )
        VALUES(?, ?, ?, ?, ?, ?)
    ''',(
        data.get('name'),
        data.get('phone'),
        data.get('email'),
        data.get('company'),
        data.get('service'),
        data.get('message'),
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Form submitted successfully"})

@app.route('/contacts', methods = ['GET'])
def get_contacts():
    conn = sqlite3.connect('artik.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from contacts')
    rows = cursor.fetchall()
    conn.close()

    contacts = []
    for row in rows:
        contacts.append({ 
            "id" : row[0],
            "name" : row[1],
            "phone" : row[2],
            "email" : row[3],
            "company": row[4],
            "service" : row[5],
            "message" : row[6],
            "timestamp" : row[7]
        })
    return jsonify(contacts)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)