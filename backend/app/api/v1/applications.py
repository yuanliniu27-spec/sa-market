from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.application import Application, AppType, AppStatus
from app.schemas.application import ApplicationInDB, ApplicationList
import uuid

router = APIRouter()


@router.get("/", response_model=ApplicationList)
async def list_applications(
    type: Optional[AppType] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("latest", regex="^(popular|latest|rating)$"),
    db: Session = Depends(get_db)
):
    """Get applications list with filters"""
    query = db.query(Application).filter(Application.status == AppStatus.APPROVED)

    # Filters
    if type:
        query = query.filter(Application.type == type)
    if category:
        query = query.filter(Application.category == category)
    if search:
        query = query.filter(
            (Application.name.ilike(f"%{search}%")) |
            (Application.description.ilike(f"%{search}%"))
        )

    # Sorting
    if sort_by == "popular":
        query = query.order_by(Application.install_count.desc())
    elif sort_by == "rating":
        query = query.order_by(Application.rating_avg.desc())
    else:  # latest
        query = query.order_by(Application.created_at.desc())

    # Pagination
    total = query.count()
    offset = (page - 1) * page_size
    apps = query.offset(offset).limit(page_size).all()

    return {
        "data": apps,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{app_id}", response_model=ApplicationInDB)
async def get_application(
    app_id: str,
    db: Session = Depends(get_db)
):
    """Get application details"""
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.post("/", response_model=ApplicationInDB)
async def create_application(
    name: str,
    display_name: str,
    description: str,
    category: str,
    type: AppType,
    publisher_id: str = "test_user",  # TODO: Get from auth
    publisher_name: str = "Test User",
    db: Session = Depends(get_db)
):
    """Create new application"""
    app = Application(
        id=str(uuid.uuid4())[:32],
        name=name,
        display_name=display_name,
        description=description,
        category=category,
        type=type,
        publisher_id=publisher_id,
        publisher_name=publisher_name,
        status=AppStatus.PENDING
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app
