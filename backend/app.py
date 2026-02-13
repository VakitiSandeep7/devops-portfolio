from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Cleanup old structure if necessary (Run once then remove this line)
    # cur.execute('DROP TABLE IF EXISTS projects;') 
    
    cur.execute('''CREATE TABLE IF NOT EXISTS projects (
        title text, 
        description text, 
        details text, 
        tech_stack text
    );''')

    cur.execute('SELECT COUNT(*) FROM projects;')
    if cur.fetchone()[0] == 0:
        # Project 1: Cyber Hacking
        cur.execute("INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)",
            ("Cyber Hacking Breach Prediction", 
             "Predictive analytics model to forecast security breaches.",
             "Developed a model using stochastic processes and ML algorithms. Designed a Django-based web interface for data visualization and analyzed large historical datasets to identify patterns.",
             "Python, Django, MySQL, ML Algorithms"))

        # Project 2: Hybrid Cryptography
        cur.execute("INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)",
            ("Secure Cloud Storage (Hybrid Crypto)", 
             "Multi-algorithm encryption system for secure storage.",
             "Implemented AES, Blowfish, and RC6 algorithms with steganography. Developed J2EE-based authentication and file management modules to optimize security.",
             "J2EE, AES, Blowfish, RC6, Steganography"))

        # Project 3: 3-Tier Portfolio
        cur.execute("INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)",
            ("Multi-Container DevOps Portfolio", 
             "A 3-tier architecture app using Docker and Postgres.",
             "Managed multi-service orchestration with Docker-Compose. Automated networking between Flask and PostgreSQL and deployed via Render CI/CD.",
             "Docker, Docker-Compose, PostgreSQL, Python"))
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def get_portfolio_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, description, details, tech_stack FROM projects;')
    rows = cur.fetchall()
    proj_list = [{"title": r[0], "description": r[1], "details": r[2], "tech_stack": r[3]} for r in rows]
    cur.close()
    conn.close()
    
    return jsonify({
        "name": "Sandeep Vakiti",
        "role": "DevOps & Cloud Engineer",
        "projects": proj_list
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
