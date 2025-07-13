from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import config

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    url = Column(String(1024), unique=True, nullable=False)
    published_at = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)
    category = Column(String(64), nullable=True)
    sentiment = Column(String(16), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    job_name = Column(String(64), nullable=False)
    run_time = Column(DateTime, default=datetime.datetime.utcnow)
    articles_fetched = Column(Integer)
    errors = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
