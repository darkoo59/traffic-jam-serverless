from flask import Flask, request
import json
import psycopg2
from werkzeug.security import check_password_hash
import jwt

app = Flask(__name__)

def generate_access_token(email, role):
    payload = {'email': email, 'role': role}
    return jwt.encode(payload, "secret", algorithm="HS256")

def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return json.dumps({'status': 400, 'message': 'Missing required data'})

    conn = psycopg2.connect(
        host="host.docker.internal",
        port="12107",
        database="faas_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    conn.close()
    if not user_data:
        # User does not exist in the database
        return json.dumps({'status': 401, 'message': 'Invalid credentials'})
    hashed_password = user_data[0]
    role = user_data[1]
    if check_password_hash(hashed_password, password):
        access_token = generate_access_token(email, role)
        return json.dumps({'status': 200, 'access_token': access_token})
    return json.dumps({'status': 401, 'message': 'Invalid credentials'})

def handle(req):
    """handle a login request"""
    if request.method == 'POST':
        return login_user()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
