from flask import Flask, request
import json
import psycopg2
import os
import logging
from urllib.parse import parse_qs
from urllib.parse import urlparse

app = Flask(__name__)

def delete_user():
    url = request.url
    parsed_url = urlparse(url)
    email = parse_qs(parsed_url.query)['email'][0]
    if not email:
        return json.dumps({'status': 400, 'message': "You aren't provided email"})
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
        return json.dumps({'status': 409, 'message': "There isn't users with that email!"})
    cursor.execute("DELETE FROM users WHERE email = %s",(email,))
    conn.commit()
    conn.close()
    return json.dumps({'status': 200, 'message': "User successfully deleted!"})

def main():
    """handle a get-markers request"""
    if request.method == 'GET':
        return delete_user()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
