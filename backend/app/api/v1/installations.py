from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.installation import Installation, InstallStatus
from app.models.application import Application
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/install")
async def install_application(
    app_id: str,
    user_id: str = "test_user",  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Install application to user's SalesAgent"""

    # Check if application exists
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # Check if already installed
    existing = db.query(Installation).filter(
        Installation.user_id == user_id,
        Installation.app_id == app_id,
        Installation.status == InstallStatus.ACTIVE
    ).first()

    if existing:
        return {
            "status": "already_installed",
            "installation_id": existing.id
        }

    # Create installation record
    installation = Installation(
        id=str(uuid.uuid4())[:32],
        user_id=user_id,
        app_id=app_id,
        version_id=app.current_version_id,
        status=InstallStatus.ACTIVE
    )
    db.add(installation)

    # Update install count
    app.install_count += 1

    db.commit()
    db.refresh(installation)

    return {
        "status": "success",
        "installation_id": installation.id,
        "installed_at": installation.installed_at
    }


@router.get("/my")
async def get_my_installations(
    user_id: str = "test_user",  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Get user's installed applications"""
    installations = db.query(Installation).filter(
        Installation.user_id == user_id,
        Installation.status == InstallStatus.ACTIVE
    ).all()

    return {
        "installations": [
            {
                "id": inst.id,
                "app_id": inst.app_id,
                "version_id": inst.version_id,
                "installed_at": inst.installed_at
            }
            for inst in installations
        ]
    }


@router.delete("/{installation_id}")
async def uninstall_application(
    installation_id: str,
    db: Session = Depends(get_db)
):
    """Uninstall application"""
    installation = db.query(Installation).filter(Installation.id == installation_id).first()
    if not installation:
        raise HTTPException(status_code=404, detail="Installation not found")

    installation.status = InstallStatus.UNINSTALLED
    db.commit()

    return {"status": "success"}
