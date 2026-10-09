import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_postgres_conn():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")
    
    return psycopg.connect(
        database_url, 
        sslmode="require",
        autocommit=True,
        row_factory=dict_row
    )
    