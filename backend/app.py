import os
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS projects (title TEXT, description TEXT, details TEXT, tech_stack TEXT);')
        cur.execute('SELECT COUNT(*) FROM projects;')
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO projects VALUES (%s, %s, %s, %s)', ('Cyber Hacking', 'ML security.', 'ML with Django.', 'Python, Django'))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e: print(e)

@app.route('/')
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT title, description, details, tech_stack FROM projects;')
        rows = cur.fetchall()
        return jsonify({'projects': [{'title': r[0], 'description': r[1], 'details': r[2], 'tech_stack': r[3]} for r in rows]})
    except Exception as e: return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)