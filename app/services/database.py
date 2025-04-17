import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import create_engine, Column, Integer, Text, String

from sqlalchemy.orm import declarative_base, sessionmaker

# Config

POSTGRES_USER = "postgres"

POSTGRES_PASSWORD = "admin123"

POSTGRES_HOST = "localhost"

POSTGRES_PORT = "5432"

TARGET_DB = "codegenai"

# Step 1: Connect to default database to create the target DB if not exists

def create_database_if_not_exists():

    try:

        conn = psycopg2.connect(

            dbname="postgres",

            user="user-name",

            password="user-password",

            host=POSTGRES_HOST,

            port=POSTGRES_PORT

        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TARGET_DB}'")

        exists = cur.fetchone()

        if not exists:

            cur.execute(f"CREATE DATABASE {TARGET_DB}")

            print(f"Database '{TARGET_DB}' created successfully.")

        else:

            print(f"Database '{TARGET_DB}' already exists.")

        cur.close()

        conn.close()

    except Exception as e:

        print("Error checking or creating database:", e)

# Step 2: SQLAlchemy setup for your database

DATABASE_URL = "postgresql+psycopg2://user-name:user-password@localhost:5432/codegenai"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Your model

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