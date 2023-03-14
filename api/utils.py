from datetime import datetime, timedelta
from typing import Any, Dict

from config import Config
from jose import jwt


def create_access_token(claims: Dict[str, Any]) -> str:
    expires = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims.update({"exp": expires})
    return jwt.encode(
        claims, Config.SECRET_KEY, algorithm=Config.ACCESS_TOKEN_ALGORITHM
    )
