from pydantic import BaseModel, HttpUrl
from typing import Optional

class AgentResponse(BaseModel):
    industry: Optional[str]
    company_size: Optional[str]
    location: Optional[str]