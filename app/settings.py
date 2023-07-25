from fastapi import HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


setting_object = Settings()
security = HTTPBearer()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
