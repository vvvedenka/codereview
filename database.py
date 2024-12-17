from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vvvedenka:1230@127.0.0.1:5433/vvvedenka")

engine = create_engine("postgresql://vvvedenka:1230@127.0.0.1:5433/vvvedenka")
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()
