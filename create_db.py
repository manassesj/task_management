import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def create_database():
    dbname = os.environ.get('POSTGRES_DB', 'taskdb')
    user = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '5432')

    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()

        if not exists:
            print(f'Creating database {dbname}...')
            cursor.execute(f'CREATE DATABASE "{dbname}";')
        else:
            print(f'Database {dbname} already exists.')

        cursor.close()
        connection.close()

    except Exception as e:
        print(f'Error creating database: {e}')

if __name__ == '__main__':
    create_database()
