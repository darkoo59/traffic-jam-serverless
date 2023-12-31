from flask import Flask, request
import json
import psycopg2
import os
import logging

app = Flask(__name__)
def get_users():
    conn = psycopg2.connect(
        host="host.docker.internal",
        port="12107",
        database="faas_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
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
    return json.dumps({'status': 200, 'users_data': users_data})

def main():
    """handle a get-markers request"""
    if request.method == 'GET':
        return get_users()
    else:
        return json.dumps({'status': 405, 'message': 'Invalid request method'})
