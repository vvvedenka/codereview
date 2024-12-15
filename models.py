from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    syllables = Column(Integer, nullable=False)
    rare_letters = Column(String, nullable=True)
