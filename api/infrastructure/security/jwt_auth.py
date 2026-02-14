"""JWT authentication for the MangoAI API.

Validates Bearer tokens using the same SECRET_KEY and HS256 algorithm
as Mango Reach, so tokens issued by Mango Reach work here too.
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.infrastructure.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """Validate JWT and return user email from the 'sub' claim."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


def get_raw_token(token: str = Depends(oauth2_scheme)) -> str:
    """Return the raw JWT token to be forwarded to Mango Reach API."""
    # Validate first
    get_current_user_email(token)
    return token
