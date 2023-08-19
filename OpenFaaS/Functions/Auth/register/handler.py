from _json import make_encoder

from flask import Flask, request, make_response
import json
from werkzeug.security import generate_password_hash
import psycopg2
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def register_user():
    data = request.get_json()
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    address = data.get('address')
    birthdate = data.get('birthdate')
    gender = data.get('gender')
    if not firstname or not lastname or not password or not email or not address or not birthdate or not gender:
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
                password VARCHAR(255) NOT NULL,
                firstname VARCHAR(255) NOT NULL,
                lastname VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                address VARCHAR(255),
                birthdate DATE,
                gender VARCHAR(10),
                role VARCHAR(50) DEFAULT 'Client'
            )
            """
        )

    conn.commit()
    # Check if the user already exists in the database
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    user_count = cursor.fetchone()[0]

    if user_count > 0:
        conn.close()
        return json.dumps({'status': 409, 'message': 'Email already exists'})

    cursor.execute( "INSERT INTO users (password, firstname, lastname, email, address, birthdate, gender) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (hashed_password, firstname, lastname, email, address, birthdate, gender))
    conn.commit()
    conn.close()
    return json.dumps({'status': 200, 'message': 'Registration successful'})

@cross_origin()
def handle(req):
    """Handle registration request"""
    if request.method == 'POST':
        return _corsify_actual_response(make_response(register_user()))
    else:
        return _corsify_actual_response(make_response(json.dumps({'status': 405, 'message': 'Invalid request method'})))
