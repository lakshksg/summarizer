from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class AgentResponse(BaseModel):
    industry: Optional[str]
    company_size: Optional[str]
    location: Optional[str]

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    username: str
    exp: datetime