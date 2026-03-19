from sqlalchemy import Column, String, Enum, Integer, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AuditType(str, enum.Enum):
    SECURITY_SCAN = "security_scan"
    METADATA_CHECK = "metadata_check"
    FUNCTION_TEST = "function_test"
    DEPENDENCY_CHECK = "dependency_check"


class AuditLogStatus(str, enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(32), primary_key=True, index=True)
    version_id = Column(String(32), ForeignKey("app_versions.id"), index=True)
    audit_type = Column(Enum(AuditType), nullable=False)
    status = Column(Enum(AuditLogStatus), nullable=False)
    details = Column(JSON)
    duration_ms = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    version = relationship("AppVersion", back_populates="audit_logs")
