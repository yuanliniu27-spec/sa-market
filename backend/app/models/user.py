from sqlalchemy import Column, String, Boolean, Enum, TIMESTAMP, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(32), primary_key=True, index=True)
    open_id = Column(String(32), index=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(255))
    email = Column(String(100), index=True)
    mobile = Column(String(20))

    department_ids = Column(JSON, default=list)
    role = Column(Enum(UserRole), default=UserRole.DEVELOPER, index=True)

    is_active = Column(Boolean, default=True, index=True)
    last_login_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    installations = relationship("Installation", back_populates="user")
    reviews = relationship("Review", back_populates="user")
