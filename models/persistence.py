import os
from sqlalchemy import Column, Integer, Text, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

db = os.getenv("DB")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")

# Define Base
Base = declarative_base()

# Define table model
class GenerationLog(Base):

    __tablename__ = "generation_logs"
    id = Column(Integer, primary_key=True, index=True)
    srs_content = Column(Text)
    extracted_info = Column(Text)
    generated_code = Column(Text)
    generated_tests = Column(Text)
    test_results = Column(Text)
    debug_logs = Column(Text)

# Database connection URL
DATABASE_URL = (f"postgresql://{user}:{password}@{host}:{port}/{db}")

# Engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create table
def init_db():
    Base.metadata.create_all(bind=engine)

# Get all results from DB
def get_all_results():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM generation_logs")).fetchall()
        return [dict(row._mapping) for row in result] 