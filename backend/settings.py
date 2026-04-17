from pydantic_settings import BaseSettings

# JWT 配置
class JwtSettings(BaseSettings):
    secret_key: str = "kkkk"
    algorithm: str = "HS256"
    expire_hours: int = 2
    token_prefix: str = "Bearer "

# Redis 缓存配置
class CacheSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    database: int = 0
    password: str | None = None

# 应用总配置
class AppSettings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    cache: CacheSettings = CacheSettings()

app_settings = AppSettings()
