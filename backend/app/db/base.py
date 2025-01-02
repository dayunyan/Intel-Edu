from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime


Base = declarative_base()

class TimeStampMixin:
    """为所有模型添加创建时间和更新时间"""
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now) 