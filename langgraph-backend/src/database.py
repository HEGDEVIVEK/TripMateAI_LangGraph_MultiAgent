import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from pymongo import MongoClient

load_dotenv()


def get_postgres_conn():

    database_url = os.getenv("POSTGRES_DATABASE_URL")

    if not database_url:
        raise ValueError("POSTGRES_DATABASE_URL is not set")
    
    return psycopg.connect(
        database_url, 
        sslmode="require",
        autocommit=True,
        row_factory=dict_row
    )

def get_mongodb_client():
   
    mongodb_uri = os.getenv("MONGODB_DATABASE_URL")

    if not mongodb_uri:
        raise ValueError("MONGODB_DATABASE_URL is not set")

    return MongoClient(mongodb_uri)
    