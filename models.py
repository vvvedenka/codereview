from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    syllables = Column(Integer, nullable=False)
    is_rare = Column(Boolean, default=False)
