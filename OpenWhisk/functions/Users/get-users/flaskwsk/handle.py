from flask import Response
from base64 import b64decode, b64encode
from werkzeug.security import generate_password_hash
import json
import psycopg2
from werkzeug.security import check_password_hash
from decimal import Decimal

def invoke(app, args):
    environ = {
        'REQUEST_METHOD': args.get('__ow_method', 'GET').upper(),
    }

    if environ['REQUEST_METHOD'] == 'GET':
        
        conn = psycopg2.connect(
        host="host.docker.internal",
        port="12107",
        database="faas_db",
        user="postgres",
        password="postgres"
    )
        cursor = conn.cursor()
        # Create the users table if it doesn't exist
        cursor.execute("SELECT firstname, lastname, email, address, birthdate, gender, role FROM users")
        rows = cursor.fetchall()
        conn.close()

        users_data = []
        for row in rows:
            user_obj = {
                'firstname': row[0],
                'lastname': row[1],
                'email': row[2],
                'address': row[3],
                'birthdate': row[4].strftime('%Y-%m-%d'),  # Convert datetime to string
                'gender': row[5],
                'role': row[6]
            }
            users_data.append(user_obj)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'users_data': users_data})
        }
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
        }
