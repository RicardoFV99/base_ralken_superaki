import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

## Obtain database connection using variables from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

## Database test connection
try:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connection established with database")
except Exception as error:
    print(f"Error while connecting to database: {error}")
finally:
    if connection:
        connection.close()
        print("Connection Closed")
## End of testing


async def get_db_connection():
        return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
