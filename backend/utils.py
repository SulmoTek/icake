import bcrypt
import jwt
from domain.dto import JwtPayload
from domain.vo import Response
from settings import app_settings
from datetime import datetime, timedelta
import redis



class PasswordHasher:
    """密码哈希与校验工具类"""

    @staticmethod
    def hash(plain_password: str) -> str:
        """
        对明文密码进行 bcrypt 加盐哈希

        :param plain_password: 明文密码
        :return: 哈希后的密码字符串
        """
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_pw.decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        校验明文密码与哈希密码是否匹配

        :param plain_password: 明文密码
        :param hashed_password: 数据库存储的哈希密码
        :return: 校验结果
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )




class JwtUtil:
    """JWT 签发、解析、校验工具类"""

    @staticmethod
    def encode(payload: JwtPayload) -> str:
        """
        生成 JWT 令牌

        :param payload: JWT 载荷对象
        :return: 加密后的 JWT 字符串
        """
        return jwt.encode(
            payload.model_dump(),
            app_settings.jwt.secret_key,
            algorithm=app_settings.jwt.algorithm
        )

    @staticmethod
    def decode(token: str) -> JwtPayload:
        """
        解析并验证 JWT 令牌

        :param token: JWT 字符串
        :return: 解析后的载荷对象
        """
        data = jwt.decode(
            token,
            app_settings.jwt.secret_key,
            algorithms=[app_settings.jwt.algorithm]
        )
        return JwtPayload(**data)

    @staticmethod
    def validate(token: str) -> JwtPayload:
        """
        校验令牌有效性，无效会自动抛出异常

        :param token: JWT 字符串
        :return: 有效载荷
        """
        return JwtUtil.decode(token)


class ApiResponse:
    """统一响应结果工具类"""

    @staticmethod
    def _wrap(data=None, msg: str = '', code: int = 0):
        return Response(code=code, msg=msg, data=data)

    @staticmethod
    def success(data=None, msg: str = '操作成功', code: int = 200):
        return ApiResponse._wrap(data, msg, code)

    @staticmethod
    def fail(msg: str = '操作失败', data=None, code: int = 400):
        return ApiResponse._wrap(data, msg, code)

class DateTimeUtils:
    """时间工具类"""
    @staticmethod
    def now() -> float:
        """获取当前时间戳"""
        return datetime.now().timestamp()
    
    @staticmethod
    def expire() -> float:
        """获取过期时间戳"""
        return (datetime.now() + timedelta(hours=app_settings.jwt.expire_hours)).timestamp()

class CacheUtils:
    """Redis 缓存工具类"""
    _redis_instance = redis.Redis(
        host=app_settings.cache.host,
        port=app_settings.cache.port,
        db=app_settings.cache.database,
        password=app_settings.cache.password,
        decode_responses=True,
        encoding="utf-8"
    )

    @classmethod
    def get_redis(cls):
        return cls._redis_instance

    @classmethod
    def set(cls, key: str, value: str, ex: int = None):
        cls._redis_instance.set(key, value, ex=ex)

    @classmethod
    def get(cls, key: str) -> str | None:
        return cls._redis_instance.get(key) #type: ignore

    @classmethod
    def delete(cls, key: str):
        cls._redis_instance.delete(key)
