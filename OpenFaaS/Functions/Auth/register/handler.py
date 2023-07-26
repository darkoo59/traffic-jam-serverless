from flask import Flask, request
import json
from werkzeug.security import generate_password_hash
import psycopg2

app = Flask(__name__)
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return json.dumps({'status': 400, 'message': 'Missing required data'})
    hashed_password = generate_password_hash(password, "sha256")
    # hashed_password = password
    # Save the user to the database (Assuming you have a 'users' table)
    conn = psycopg2.connect(
        host="host.docker.internal",
        port="12107",
        database="faas_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    # Create the users table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """
    )

    conn.commit()
    # Check if the user already exists in the database
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    user_count = cursor.fetchone()[0]

    if user_count > 0:
        conn.close()
        return json.dumps({'status': 409, 'message': 'Username already exists'})

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    conn.close()
    return json.dumps({'status': 200, 'message': 'Registration successful', 'password': str(hashed_password)})

def handle(req):
    """Handle registration request"""
    if request.method == 'POST':
        return register_user()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
