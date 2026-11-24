import os
from datetime import datetime, timedelta, timezone

import jwt

def create_access_token(user_id: int) -> str:
    secret = os.environ.get("JWT_SECRET")

    if not secret:
        raise RuntimeError("JWT_SECRET must be configured")

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
    )
