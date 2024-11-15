# # # backend/app/schemas/user.py
# # from pydantic import BaseModel, EmailStr
# # from typing import Optional
# # import uuid
# # from enum import Enum

# # class SubscriptionPlan(str, Enum):
# #     Free = "Free"
# #     Pro = "Pro"
# #     Enterprise = "Enterprise"

# # class UserCreate(BaseModel):
# #     email: EmailStr
# #     password: str

# # class UserResponse(BaseModel):
# #     id: uuid.UUID
# #     email: EmailStr
# #     subscription_plan: SubscriptionPlan

# #     class Config:
# #         from_attributes = True  # Updated for Pydantic V2

# # class UserBase(BaseModel):
# #     email: EmailStr


# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional
# from uuid import UUID
# from app.models.user import SubscriptionPlan

# class UserBase(BaseModel):
#     email: EmailStr

# class UserCreate(UserBase):
#     password: str

# class UserUpdate(BaseModel):
#     subscription_plan: Optional[SubscriptionPlan] = None

# class UserResponse(UserBase):
#     id: UUID
#     subscription_plan: SubscriptionPlan
#     created_at: datetime

#     class Config:
#         from_attributes = True
#         json_encoders = {
#             UUID: str,
#             datetime: lambda dt: dt.isoformat()
#         }

from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum

class SubscriptionPlan(str, Enum):
    Free = "Free"
    Pro = "Pro"
    Enterprise = "Enterprise"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID4
    subscription_plan: SubscriptionPlan
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str