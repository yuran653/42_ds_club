import os
import logging
from psycopg2 import connect, sql, extras
from psycopg2 import Error as psycopg2_error
from psycopg2.extensions import connection as Connection
from dotenv import load_dotenv
import pandas as pd
import click

logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("db_connect_psycopg2.log"),
    logging.StreamHandler()
], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

db_params = {
    'dbname': os.getenv('db_name'),
    'user': os.getenv('db_user'),
    'password': os.getenv('db_pass'),
    'host': os.getenv('db_host'),
    'port': os.getenv('db_port'),
    'sslmode': 'verify-full',
    'sslrootcert': os.getenv('ssl_cert')
}

def open_connection_psycopg2(db_params: dict) -> Connection:
    try:
        conn = connect(**db_params)
        logger.info('Connection opened successfully')
        return conn
    except psycopg2_error as e:
        logger.error(f'Error connecting to the database: {e}')
        return None

def close_connection_psycopg2(conn: Connection) -> None:
    if conn:
        conn.close()
        logger.info('Connection closed')
    else:
        logger.warning('Connection not opened')

def to_sql_primary(
    table_name: str,
    df: pd.DataFrame,
    conn: Connection,
    on_conflict_section: str
    ) -> None:
    
    df_columns = list(df.columns)
    column_names = sql.SQL(', ').join(map(sql.Identifier, df_columns))
    placeholders = sql.SQL(', ').join(sql.Placeholder() for _ in df_columns)

    insert_stmt = sql.SQL('''
       INSERT INTO public.{table} ({columns}) VALUES ({placeholders}) {on_conflict}
    ''').format(
        table=sql.Identifier(table_name),
        columns=column_names,
        placeholders=placeholders,
        on_conflict=sql.SQL(on_conflict_section)
    )
    
    cur = conn.cursor()
    try:
        extras.execute_batch(cur, insert_stmt, df.values)
    except psycopg2_error as e:
        logger.error(f"Insertion error: {' '.join(str(e).splitlines())}")
    finally:
        conn.commit()
        cur.close()

@click.command()
@click.option('--batch_path', type=str, help='Path to of csv file to load into database')
def load_step(batch_path):
    df = pd.read_csv(batch_path)
    df.rename(columns={df.columns[0]: '_id'}, inplace=True)
    conn = open_connection_psycopg2(db_params)
    on_conflict_section = ''
    if conn:
        to_sql_primary(os.getenv('table_name'), df, conn, on_conflict_section)
        close_connection_psycopg2(conn)

load_step()
