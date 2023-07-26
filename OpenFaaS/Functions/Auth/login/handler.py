from flask import Flask, request
import json
import psycopg2
from werkzeug.security import check_password_hash

app = Flask(__name__)

def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return json.dumps({'status': 400, 'message': 'Missing required data'})

    conn = psycopg2.connect(
        host="host.docker.internal",
        port="12107",
        database="faas_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    hashed_password = cursor.fetchone()

    conn.close()
    if not hashed_password:
        # User does not exist in the database
        return json.dumps({'status': 401, 'message': 'Invalid credentials'})
    hashed_password = hashed_password[0]
    if check_password_hash(hashed_password, password):
        return json.dumps({'status': 200, 'message': 'Login successful'})
    return json.dumps({'status': 401, 'message': 'Invalid credentials'})

def handle(req):
    """handle a login request"""
    if request.method == 'POST':
        return login_user()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
