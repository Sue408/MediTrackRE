"""
数据库定义模块
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from ..core import config

# ========= 建立数据库连接 =========
engine = create_engine(config.database_url)

# ========= 初始化数据库会话工厂 =========
session_factory = sessionmaker(bind=engine)

# ========= 定义数据库模型基类 =========
class Base(DeclarativeBase):
    pass