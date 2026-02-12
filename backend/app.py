from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_portfolio_data():
    # This mimics data coming from a database
    data = {
        "name": "Sandeep Vakiti",
        "role": "DevOps Engineer",
        "skills": ["Docker", "Python", "Flask", "Linux", "WSL2", "Nginx"],
        "status": "Online"
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
