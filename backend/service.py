from sqlalchemy.orm import Session
from database import User
from domain.vo import (
    UserLoginRequest,
    UserRegisterRequest,
    UserPasswordResetRequest,
    UserUpdateRequest
)
from domain.dto import JwtPayload
from utils import PasswordHasher, JwtUtil, DateTimeUtils, CacheUtils
from exception import BusinessException
from constant import CacheKey


class UserService:

    @staticmethod
    def get(db: Session, phone: str) -> User | None:
        return db.query(User).filter(User.phone == phone, User.is_deleted == 0).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id, User.is_deleted == 0).first()

    @staticmethod
    def register(db: Session, req: UserRegisterRequest) -> User:
        exist_user = UserService.get(db, req.phone)
        if exist_user:
            raise BusinessException("该手机号已注册")

        password_hash = PasswordHasher.hash(req.password)
        user = User(
            phone=req.phone,
            password=password_hash,
            nickname=req.nickname
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, req: UserLoginRequest) -> tuple[str, User]:
        user = UserService.get(db, req.phone)
        if not user:
            raise BusinessException("账号或密码错误")

        if not PasswordHasher.verify(req.password, user.password): # type: ignore
            raise BusinessException("账号或密码错误")

        payload = JwtPayload(user_id=user.id, iat=DateTimeUtils.now(), exp=DateTimeUtils.expire()) # type: ignore
        token = JwtUtil.encode(payload)
        return token, user

    @staticmethod
    def reset_password(db: Session, req: UserPasswordResetRequest) -> User:
        user = UserService.get(db, req.phone)
        if not user:
            raise BusinessException("用户不存在")

        cache_key = CacheKey.reset_password_code(req.phone)
        cache_code = CacheUtils.get(cache_key)
        if not cache_code or cache_code != req.code:
            raise BusinessException("验证码错误或已过期")

        user.password = PasswordHasher.hash(req.password) # type: ignore
        db.commit()
        CacheUtils.delete(cache_key)
        return user

    @staticmethod
    def update_info(db: Session, user_id: int, req: UserUpdateRequest) -> User:
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise BusinessException("用户不存在")

        if req.nickname is not None:
            user.nickname = req.nickname # type: ignore
        if req.avatar_url is not None:
            user.avatar_url = req.avatar_url # type: ignore
        if req.gender is not None:
            user.gender = req.gender # type: ignore
        if req.birthday is not None:
            user.birthday = req.birthday # type: ignore
        if req.bio is not None:
            user.bio = req.bio # type: ignore

        db.commit()
        db.refresh(user)
        return user
