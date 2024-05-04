from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class JokeDB(Base):
    __tablename__ = 'jokes_sytaya'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    category = Column(String)
