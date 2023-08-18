import json
import psycopg2
from psycopg2.extras import RealDictCursor



conn = psycopg2.connect(
    host="host.docker.internal",
    port="12107",
    database="faas_db",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor(cursor_factory=RealDictCursor)
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
cursor.execute("SELECT * FROM markers")
markers_data = cursor.fetchall()  # Fetch all rows, not just one
conn.close()
print('darko dsadka')
#
# markers_data = [{'lat': 1.0, 'lng': 2.0, 'type': 'Traffic jam'}, {'lat': 2.0, 'lng': 1.0, 'type': 'Police'}]
# markers_list = [{'lat': row['lat'], 'lng': row['lng'], 'type': row['type']} for row in markers_data]
# response_data = {'status': 200, 'markers_data': markers_list}
# response_json = json.dumps(response_data)
# print(response_json)
