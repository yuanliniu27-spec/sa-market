from sqlalchemy import Column, String, Text, Integer, Float, Enum, TIMESTAMP, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AppStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class AppType(str, enum.Enum):
    AGENT = "agent"
    SKILL = "skill"


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(32), primary_key=True, index=True)
    type = Column(Enum(AppType), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String(255))
    category = Column(String(50), nullable=False, index=True)
    tags = Column(JSON, default=list)

    publisher_id = Column(String(32), nullable=False, index=True)
    publisher_name = Column(String(100), nullable=False)
    publisher_dept = Column(String(100))

    status = Column(Enum(AppStatus), default=AppStatus.PENDING, index=True)
    current_version_id = Column(String(32))

    install_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    versions = relationship("AppVersion", back_populates="application")
    installations = relationship("Installation", back_populates="application")
    reviews = relationship("Review", back_populates="application")
