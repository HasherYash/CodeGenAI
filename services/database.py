import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()

db = os.getenv("DB")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")

# Step 1: Connect to default database to create the target DB if not exists

def create_database_if_not_exists():

    try:

        conn = psycopg2.connect(
            dbname="postgres",
            user="user-name",
            password="user-password",
            host=host,
            port=port
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {db}")
            print(f"Database '{db}' created successfully.")

        else:
            print(f"Database '{db}' already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error checking or creating database:", e)

# Step 2: SQLAlchemy setup for your database

DATABASE_URL = (f"postgresql://{user}:{password}@{host}:{port}/{db}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DataBase model

class CodeLog(Base):

    __tablename__ = "code_logs"
    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String)
    code = Column(Text)
    test = Column(Text)
    debug_log = Column(Text)

# Step 3: Initialize the database (create tables)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created (if not existing).")