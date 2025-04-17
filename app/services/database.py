from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/codegen"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class CodeLog(Base):
   __tablename__ = "code_logs"
   id = Column(Integer, primary_key=True, index=True)
   entity = Column(String)
   code = Column(Text)
   test = Column(Text)
   debug_log = Column(Text)
def init_db():
   Base.metadata.create_all(bind=engine)