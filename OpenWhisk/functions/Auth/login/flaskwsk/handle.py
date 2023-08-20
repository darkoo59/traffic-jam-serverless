from flask import Response
from base64 import b64decode,b64encode
from werkzeug.http import parse_options_header
import sys,io
import json
import psycopg2
from werkzeug.security import check_password_hash
import jwt

block = set(['x-client-ip','x-forwarded-for','x-forwarded-proto','x-global-transaction-id'])
         
def generate_access_token(email, role):
    payload = {'email': email, 'role': role}
    return jwt.encode(payload, "secret", algorithm="HS256")

def invoke(app,args):
   environ = {
      'REQUEST_METHOD': args.get('__ow_method','GET').upper(),
   }
   
   if environ['REQUEST_METHOD']=='POST':
      raw = args.get('__ow_body')
      # Decode the base64-encoded string
      decoded_bytes = b64decode(raw)
      decoded_string = decoded_bytes.decode('utf-8')

      # Parse the JSON content
      data = json.loads(decoded_string)

      # Get the value of the "username" field and store it in a variable
      email = data["email"]
      password = data["password"]
      if not email or not password:
               return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 400,'message': 'Missing required data'})
    }
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
         return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 401, 'message': 'Invalid credentials'})
    }
      hashed_password = user_data[0]
      role = user_data[1]
      if check_password_hash(hashed_password, password):
         access_token = generate_access_token(email, role)
         return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'access_token': access_token})
    }
      return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 401, 'message': 'Invalid credentials'})
    }
   else:
      return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
    }
