from flask import Flask, request
import json
import psycopg2
import os
import logging

app = Flask(__name__)

def add_marker():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    type = data.get('type')
    if not lat or not lng or not type:
        return json.dumps({'status': 400, 'message': 'Missing required data'})
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
    return json.dumps({'status': 200, 'message': 'Marker successfully added'})

def main():
    """Handle add marker request"""
    if request.method == 'POST':
        return add_marker()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
