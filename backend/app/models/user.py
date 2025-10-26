# # backend/app/models/user.py
# from sqlalchemy import Column, String, Enum, DateTime
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql import func
# import uuid
# from app.database import Base
# import enum

# class SubscriptionPlan(enum.Enum):
#     Free = "Free"
#     Pro = "Pro"
#     Enterprise = "Enterprise"

# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.Free)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())


from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.app.database import Base
import enum

class SubscriptionPlan(enum.Enum):
    Free = "Free"
    Pro = "Pro"
    Enterprise = "Enterprise"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.Free)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
