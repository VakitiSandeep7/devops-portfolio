import os
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db_connection():
    # This pulls your database URL from Render's environment variables
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Create table if it doesn't exist
        cur.execute('CREATE TABLE IF NOT EXISTS projects (title TEXT, description TEXT, details TEXT, tech_stack TEXT);')

        # Check if table is empty
        cur.execute('SELECT COUNT(*) FROM projects;')
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)', 
                       ('Cyber Hacking', 'ML security.', 'ML with Django.', 'Python, Django'))

        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database error: {e}")

@app.route('/')
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT title, description, details, tech_stack FROM projects;')
        rows = cur.fetchall()
        projects = []
        for r in rows:
            projects.append({
                'title': r[0],
                'description': r[1],
                'details': r[2],
                'tech_stack': r[3]
            })
        cur.close()
        conn.close()
        return jsonify({'projects': projects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Render uses the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
