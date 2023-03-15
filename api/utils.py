from datetime import datetime, timedelta
from typing import Any, Dict

from config import settings
from jose import jwt


def create_access_token(claims: Dict[str, Any]) -> str:
    expires = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    claims.update({"exp": expires})
    return jwt.encode(
        claims, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM
    )
