from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(32), primary_key=True, index=True)
    app_id = Column(String(32), ForeignKey("applications.id"), index=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), index=True)
    version_id = Column(String(32))

    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    is_helpful = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
