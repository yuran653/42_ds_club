from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
ssl_cert = os.getenv('ssl_cert')

try:
    engine = create_engine(
        f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}',
        connect_args={
            'sslmode': 'verify-full',
            'sslrootcert': ssl_cert
        }
    )
    conn = engine.connect()
    print('Connection successful')
except Exception as e:
    print(f'Error connecting to the database: {e}')
finally:
    if conn:
        conn.close()
        print('Connection closed')
