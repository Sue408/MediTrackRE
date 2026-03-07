"""
核心配置对象-config-定义模块
属性:
- host: 服务运行地址
- port: 服务运行端口
- database_url: 数据库连接字符串
- algorithm: JWT加密算法
- secret_key: JWT加密密钥
- access_token_expire_minutes: 访问令牌有效时长（分钟）
- refresh_token_expire_days: 刷新令牌有效时长（天）
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """核心配置对象定义"""
    # 项目运行模式
    debug: bool = True

    # 后端服务地址、端口信息
    host: str = "127.0.0.1"
    port: int = 8080

    # 数据库连接字符串
    database_url: str = "sqlite:///./test.db"

    # JWT算法、密钥与令牌有效期
    algorithm: str = "HS256"
    secret_key: str = "MediTrack"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 1

    # 核心配置对象配置参数
    model_config = SettingsConfigDict(
        env_file=[".env.local", ".env"],
        env_file_encoding="utf-8"
    )

config: Settings = Settings() # 实例化核心配置对象
