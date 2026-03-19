from sqlalchemy import Column, String, Text, BigInteger, Enum, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AuditStatus(str, enum.Enum):
    PENDING = "pending"
    AUTO_PASSED = "auto_passed"
    AUTO_FAILED = "auto_failed"
    MANUAL_REVIEWING = "manual_reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"


class AppVersion(Base):
    __tablename__ = "app_versions"

    id = Column(String(32), primary_key=True, index=True)
    app_id = Column(String(32), ForeignKey("applications.id"), index=True)
    version = Column(String(20), nullable=False)
    changelog = Column(Text)

    file_url = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_hash = Column(String(64), nullable=False)

    dependencies = Column(JSON, default=list)
    compatibility = Column(JSON)
    metadata = Column(JSON)

    audit_status = Column(Enum(AuditStatus), default=AuditStatus.PENDING, index=True)
    audit_result = Column(JSON)
    reviewer_id = Column(String(32))
    reviewed_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)

    # Relationships
    application = relationship("Application", back_populates="versions")
    audit_logs = relationship("AuditLog", back_populates="version")
