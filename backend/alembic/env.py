from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所有模型
from app.models.base import Base
from app.models.user import User,  Student,Teacher, UserRole, Gender
from app.models.curriculum import Subject, Chapter, Section, Book
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.classes import Class
from app.models.analysis import AnalysisResult
from app.models.scale import TestPaper, TestPaperRecord
from app.models.agent import AIAgent
from app.models.chat import Chat

# 这行很重要，确保所有模型都被导入后再设置
target_metadata = Base.metadata

# 从 alembic.ini 获取配置
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()