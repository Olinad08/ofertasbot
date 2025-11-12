import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# We support DATABASE_URL (Render) or separate DB_* env vars
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_conn():
    if DATABASE_URL:
        # Parse DATABASE_URL and connect
        result = urlparse(DATABASE_URL)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        return psycopg2.connect(
            dbname=database, user=username, password=password, host=hostname, port=port
        )
    else:
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT') or 5432
        )

def init_db():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        ml_id VARCHAR(80) UNIQUE,
        titulo TEXT,
        preco NUMERIC,
        imagem TEXT,
        link TEXT,
        categoria TEXT,
        criado_em TIMESTAMP DEFAULT NOW()
    );""")
    conn.commit()
    cur.close()
    conn.close()
