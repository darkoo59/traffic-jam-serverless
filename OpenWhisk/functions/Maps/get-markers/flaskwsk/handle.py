from flask import Response
from base64 import b64decode, b64encode
from werkzeug.security import generate_password_hash
import json
import psycopg2
from werkzeug.security import check_password_hash
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


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
        cursor.execute("SELECT lat, lng, type  FROM markers")
        rows = cursor.fetchall()  # Fetch all rows, not just one
        conn.close()
        markers_data = []
        for row in rows:
            marker_obj = {
                'lat': row[0],
                'lng': row[1],
                'type': row[2]
            }
            markers_data.append(marker_obj)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 200, 'markers_data': markers_data}, cls=DecimalEncoder)
        }
        return json.dumps({'status': 200, 'markers_data': markers_data}, cls=DecimalEncoder)
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 405, 'message': 'Invalid request method'})
        }
