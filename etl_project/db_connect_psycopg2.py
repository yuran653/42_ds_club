import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv('db_name'),
        user=os.getenv('db_user'),
        password=os.getenv('db_pass'),
        host=os.getenv('db_host'),
        port=os.getenv('db_port'),
        sslmode='verify-full',
        sslrootcert = os.getenv('ssl_cert')
    )
    print('Connection successful')
except psycopg2.Error as e:
    print(f'Error connecting to the database: {e}')
finally:
    if conn:
        conn.close()
        print('Connection closed')
