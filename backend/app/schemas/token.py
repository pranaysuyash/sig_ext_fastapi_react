# # backend/app/schemas/token.py
# from pydantic import BaseModel
# from typing import Optional

# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     class Config:
#         from_attributes = True  # For Pydantic V2 compatibility

# class TokenData(BaseModel):
#     id: Optional[str] = None
#     class Config:
#         from_attributes = True  # For Pydantic V2 compatibility


from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str] = None
    sub: Optional[str] = None  # For storing user ID

    class Config:
        from_attributes = True