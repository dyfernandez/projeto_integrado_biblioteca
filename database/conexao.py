import os
from dotenv import load_dotenv
import psycopg2

load_dotenv(override=True)

db_host=os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name=os.getenv("DB_NAME")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")

def conectar():
   return psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)