"""
用户认证与鉴权安全模块
本模块提供用户密码哈希与JWT（JSON Web Token）令牌的创建、验证与管理功能。

模块构成:
1. TokenData (dataclass)
   - 作用: 定义了JWT令牌payload（载荷）的核心数据结构。
   - 内容: 用户ID (user_id) 与 用户昵称 (nickname)。

2. PasswordHasher (类)
   - 作用: 使用 bcrypt 算法对用户密码进行安全的哈希加密与验证。
   - 特点: 自动加盐，有效抵御彩虹表攻击。

3. JWTManager (类)
   - 作用: 统一管理JWT令牌的生命周期。
   - 功能:
     * create_access_token: 生成短期有效的访问令牌 (Access Token)。
     * create_refresh_token: 生成长期有效的刷新令牌 (Refresh Token)。
     * verify_token: 验证令牌的有效性、完整性，并解析出用户数据。

使用说明:
- 用户注册/修改密码时，使用 `PasswordHasher.get_hashed_password` 处理密码。
- 用户登录验证时，使用 `PasswordHasher.verify_password` 比对密码。
- 登录成功后，使用 `JWTManager.create_*_token` 为用户颁发令牌。
- 在需要鉴权的接口，使用 `JWTManager.verify_token` 验证请求中的令牌。

安全提示:
- 令牌密钥 (`config.secret_key`) 必须严格保密，并具备足够的强度。
- 访问令牌过期时间应较短，刷新令牌过期时间可较长，结合使用以平衡安全与体验。
- 本模块验证失败时均抛出 401 状态码的 HTTPException。
"""
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Literal
import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status

from .config import config

# ========= token payload数据结构定义 =========
@dataclass
class TokenData:
    """token payload基础数据结构"""
    user_id: int|None
    nickname: str|None

    def to_dict(self) -> dict:
        """数据字典生成"""
        return {
            "sub": str(self.user_id), # payload默认字段
            "user_id": self.user_id,
            "nickname": self.nickname
        }

# ========= password hash管理模块定义 =========
class PasswordHasher:
    """password hash管理模块"""
    @staticmethod
    def get_hashed_password(password: str) -> str:
        """
        生成密码对应的hash值 (自动加盐)

        Args:
            password: 明文密码

        Returns:
            str: 加密后的密码hash
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        验证密码是否与hash匹配

        Args:
            password: 明文密码
            hashed_password: 已经加密的密码hash

        Returns:
            bool: 验证结果
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# ========= JWT管理模块定义 =========
class JWTManager:
    """JWT管理模块"""
    @staticmethod
    def _create_token(
            token_data: TokenData,
            token_type: Literal["access", "refresh"],
            expires_delta: timedelta
    ) -> str:
        """
        统一的token生成方法

        Args:
            token_data: token payload基础数据
            token_type: token类型 ("access" or "refresh")
            expires_delta: token有效时长

        Returns:
            str: JWT token
        """
        # 获取token payload的基础数据字典
        to_encode = token_data.to_dict()

        # 计算token的失效时间
        expire = datetime.now(timezone.utc) + expires_delta

        # 构造完整的payload
        to_encode.update({
            "exp": expire, # 失效时间
            "type": token_type, # token类型
            "iat": datetime.now(timezone.utc) # 签发时间
        })
        return jwt.encode(
            to_encode,
            config.secret_key,
            algorithm=config.algorithm
        )

    @staticmethod
    def create_access_token(token_data: TokenData) -> str:
        """
        生成访问token

        Args:
            token_data: token payload基础数据

        Returns:
            str: access JWT token
        """
        return JWTManager._create_token(
            token_data,
            token_type="access",
            expires_delta=timedelta(minutes=config.access_token_expire_minutes)
        )

    @staticmethod
    def create_refresh_token(token_data: TokenData) -> str:
        """
        生成刷新token

        Args:
            token_data: token payload基础数据

        Returns:
            str: refresh JWT token
        """
        return JWTManager._create_token(
            token_data,
            token_type="refresh",
            expires_delta=timedelta(days=config.refresh_token_expire_days)
        )

    @staticmethod
    def verify_token(token: str) -> TokenData:
        """
        验证并解码JWT token

        Args:
            token: JWT token字符串

        Returns:
            TokenData: 解码后的token payload基础数据

        Raises:
            HTTPException: 当发生以下任何一种情况时抛出，状态码均为401：
            1. token过期 (jwt.ExpiredSignatureError)
            2. token无效，包括签名错误、格式错误、解码失败等 (jwt.InvalidTokenError)
            3. token中缺少必要的user_id或nickname字段
        """
        try:
            # 解码JWT token
            payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])

            # 提取用户ID和用户昵称
            user_id: int = payload.get("user_id")
            nickname: str = payload.get("nickname")

            # 检测用户ID和昵称内容完整性
            if user_id is None or nickname is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无法验证的token",
                    headers={"WWW-Authenticate": "Bearer"}
                )

            return TokenData(user_id=user_id, nickname=nickname)
        except jwt.ExpiredSignatureError:
            # 捕获token过期错误
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="过期的token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except jwt.InvalidTokenError:
            # 捕获其他token错误（签名错误、格式错误、解码失败等）
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的token",
                headers={"WWW-Authenticate": "Bearer"}
            )

