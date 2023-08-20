from flask import Response
from base64 import b64decode, b64encode
from werkzeug.security import generate_password_hash
import json
import psycopg2
from werkzeug.security import check_password_hash
from decimal import Decimal
import sys,io

def invoke(app, args):
    headers = args.get('__ow_headers',{})
    environ = {
        'REQUEST_METHOD': args.get('__ow_method','GET').upper(),
        'QUERY_STRING': args.get('__ow_query',None),
    }

    if environ['REQUEST_METHOD'] == 'GET':
        _, email = environ['QUERY_STRING'].split("=")
        if not email:
            return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 400, 'message': "You aren't provided email"})
        }
        conn = psycopg2.connect(
            host="host.docker.internal",
            port="12107",
            database="faas_db",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        conn.commit()
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            conn.close()
            return {
            'statusCode': 409,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 409, 'message': "There isn't users with that email!"})
        }
        cursor.execute("DELETE FROM users WHERE email = %s",(email,))
        conn.commit()
        conn.close()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'message': "User successfully deleted!"})
        }
        
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
        }
