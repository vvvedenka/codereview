from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vvvedenka:1230@db:5432/vvvedenka")

engine = create_engine("postgresql://vvvedenka:1230@db:5432/vvvedenka")
Session = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()
