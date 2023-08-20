from flask import Response
from base64 import b64decode
import json
import psycopg2

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
        lat = data["lat"]
        lng = data["lng"]
        type = data["type"]
        if not lat or not lng or not type:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 400, 'message': 'Missing required data'})
            }
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
                CREATE TABLE IF NOT EXISTS markers (
                    id SERIAL PRIMARY KEY,
                    lat DECIMAL NOT NULL,
                    lng DECIMAL NOT NULL,
                    type VARCHAR(255) NOT NULL
                )
                """
            )

        conn.commit()
        cursor.execute( "INSERT INTO markers (lat, lng, type) "
                "VALUES (%s, %s, %s)",
                (lat, lng, type))
        conn.commit()
        conn.close()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'message': 'Marker successfully added'})
        }
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
        }
