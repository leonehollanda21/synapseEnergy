import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
print("-" * 30)
print(f"DEBUG: DATABASE_URL encontrada: {os.getenv('DATABASE_URL')}")
print(f"DEBUG: DB_HOST encontrado: {os.getenv('DB_HOST')}")
print("-" * 30)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    USER = os.getenv("DB_USER", "postgres")
    PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = os.getenv("DB_NAME", "SYNENG")
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = os.getenv("DB_PORT", "5432")
    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def create_database_if_not_exists():
    host = os.getenv("DB_HOST", "localhost")
    if host != "localhost":
        print("Ambiente de produção detectado: Pulando criação automática de DB.")
        return

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "root"),
            host=host,
            port=os.getenv("DB_PORT", "5432")
        )
        conn.autocommit = True
        cursor = conn.cursor()

        db_name = os.getenv("DB_NAME", "SYNENG")
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Banco de dados '{db_name}' criado com sucesso!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Nota: Verificação de banco ignorada: {e}")

# Executa apenas se necessário
create_database_if_not_exists()

# 3. Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()