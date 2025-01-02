from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# 根据环境变量选择数据库URL
TESTING = os.getenv("TESTING", "false").lower() == "true"
DATABASE_URL = settings.DATABASE_URL + "_test" if TESTING else settings.DATABASE_URL

# 创建引擎
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
