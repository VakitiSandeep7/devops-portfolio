from flask import Flask, jsonify
from flask_cors import CORS
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            return conn
        except Exception as e:
            print(f"Database not ready... {e}")
            time.sleep(2)

@app.route('/')
def get_portfolio_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create Profile Table
    cur.execute('CREATE TABLE IF NOT EXISTS profile (name text, role text, skills text);')
    cur.execute('SELECT COUNT(*) FROM profile;')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO profile (name, role, skills) VALUES (%s, %s, %s)",
                    ("Sandeep Vakiti", "DevOps Engineer", "Docker, Python, Flask, Linux, PostgreSQL"))

    # Create Projects Table
    cur.execute('CREATE TABLE IF NOT EXISTS projects (title text, description text, details text, tech_stack text);')
    cur.execute('SELECT COUNT(*) FROM projects;')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)",
        ("Multi-Container Portfolio", 
        "A 3-tier architecture app using Docker Compose and Postgres.",
        "Managed multi-service orchestration with Docker and automated internal networking between Flask and PostgreSQL.",
        "Docker, Docker-Compose, PostgreSQL"))

        cur.execute("INSERT INTO projects (title, description, details, tech_stack) VALUES (%s, %s, %s, %s)",
        ("CI/CD Pipeline", 
        "Automated deployment workflow using GitHub Actions.",
        "Designed a workflow that triggers on every push, runs linting, and automatically deploys the latest build to Render.",
        "GitHub Actions, YAML, Render API"))

    conn.commit()

    # Fetch Data
    cur.execute('SELECT name, role, skills FROM profile LIMIT 1;')
    p = cur.fetchone()

    cur.execute('SELECT title, description, details, tech_stack FROM projects;')
    rows = cur.fetchall()
    proj_list = [{"title": r[0], "description": r[1], "details": r[2], "tech_stack": r[3]} for r in rows]

    cur.close()
    conn.close()

    return jsonify({
        "name": p[0],
        "role": p[1],
        "skills": p[2].split(", "),
        "projects": proj_list,
        "status": "Live from Database"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
