import os
from dotenv import load_dotenv
import psycopg2

# Lê as configurações do banco do arquivo .env (que não vai para o git)
load_dotenv(override=True)

db_host=os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name=os.getenv("DB_NAME")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")

def conectar():
    """Abre e devolve uma conexão com o PostgreSQL."""
    return psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)