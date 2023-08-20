from flask import Response
from base64 import b64decode, b64encode
from werkzeug.security import generate_password_hash
import sys
import io
import json
import psycopg2
from werkzeug.security import check_password_hash
import jwt


def generate_access_token(email, role):
    payload = {'email': email, 'role': role}
    return jwt.encode(payload, "secret", algorithm="HS256")


def invoke(app, args):
    environ = {
        'REQUEST_METHOD': args.get('__ow_method', 'GET').upper(),
    }

    if environ['REQUEST_METHOD'] == 'POST':
        raw = args.get('__ow_body')
        # Decode the base64-encoded string
        decoded_bytes = b64decode(raw)
        decoded_string = decoded_bytes.decode('utf-8')

        # Parse the JSON content
        data = json.loads(decoded_string)

        # Get the value of the "username" field and store it in a variable
        email = data["email"]
        password = data["password"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        address = data["address"]
        birthdate = data["birthdate"]
        gender = data["gender"]
        if not firstname or not lastname or not password or not email or not address or not birthdate or not gender:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 400, 'message': 'Missing required data'})
            }
        hashed_password = generate_password_hash(password, "sha256")
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
            return {
                'statusCode': 409,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 409, 'message': 'Email already exists'})
            }
        cursor.execute("INSERT INTO users (password, firstname, lastname, email, address, birthdate, gender) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (hashed_password, firstname, lastname, email, address, birthdate, gender))
        conn.commit()
        conn.close()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'message': 'Registration successful'})}
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
        }
