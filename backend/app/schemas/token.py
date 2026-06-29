from typing import Optional

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Optional[str] = None
    sub: Optional[str] = None
