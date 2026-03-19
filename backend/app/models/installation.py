from sqlalchemy import Column, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class InstallStatus(str, enum.Enum):
    ACTIVE = "active"
    UNINSTALLED = "uninstalled"


class Installation(Base):
    __tablename__ = "installations"

    id = Column(String(32), primary_key=True, index=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), index=True)
    app_id = Column(String(32), ForeignKey("applications.id"), index=True)
    version_id = Column(String(32))

    salesagent_instance_id = Column(String(64))
    status = Column(Enum(InstallStatus), default=InstallStatus.ACTIVE)
    installed_at = Column(TIMESTAMP, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="installations")
    application = relationship("Application", back_populates="installations")
