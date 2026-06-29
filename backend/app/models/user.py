import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.sql import func

from backend.app.database import Base
from backend.app.db_types import GUID

class SubscriptionPlan(enum.Enum):
    Free = "Free"
    Pro = "Pro"
    Enterprise = "Enterprise"

class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    subscription_plan = Column(
        Enum(SubscriptionPlan, name="subscription_plan"),
        nullable=False,
        default=SubscriptionPlan.Free,
        server_default=SubscriptionPlan.Free.value,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
