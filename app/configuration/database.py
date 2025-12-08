import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Ajuste aqui para pegar as variaveis do seu .env corretamente
# No GSport estava apenas "USER", aqui mantive os nomes padrões mais seguros
USER = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "SYNENG")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")


def create_database_if_not_exists():
    """Cria o banco de dados se ele não existir (PostgreSQL)"""
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Banco de dados '{DB_NAME}' criado com sucesso!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Nota: Verificação de banco ignorada ou falhou: {e}")


# Executa a criação do banco antes de conectar o SQLAlchemy
create_database_if_not_exists()

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()