from constant import SECRET_KEY
from datetime import datetime, timedelta ,timezone
import jwt

from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token with payload and expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode the JWT token."""
    try:
        jwt_token = token.split(" ")[1]
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        
        return payload
    except Exception as e:

        return False