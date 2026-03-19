from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.version import AppVersion, AuditStatus
from app.models.audit import AuditLog, AuditType, AuditLogStatus
from app.services.audit import SecurityScanner, MetadataValidator
from app.services.storage import StorageService
import uuid
import tempfile
import os

router = APIRouter()


@router.post("/upload")
async def upload_version(
    app_id: str = Form(...),
    version: str = Form(...),
    changelog: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload new version and run audit"""

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        # Calculate file hash
        file_hash = StorageService.calculate_sha256(tmp_path)
        file_size = os.path.getsize(tmp_path)

        # Upload to MinIO
        storage = StorageService()
        file_url = storage.upload_file(tmp_path, app_id, f"{version}.zip")

        # Create version record
        version_id = str(uuid.uuid4())[:32]
        app_version = AppVersion(
            id=version_id,
            app_id=app_id,
            version=version,
            changelog=changelog,
            file_url=file_url,
            file_size=file_size,
            file_hash=file_hash,
            audit_status=AuditStatus.PENDING
        )
        db.add(app_version)
        db.commit()

        # Run automatic audits
        audit_results = []

        # 1. Security Scan
        scanner = SecurityScanner()
        security_result = scanner.scan(tmp_path)
        security_log = AuditLog(
            id=str(uuid.uuid4())[:32],
            version_id=version_id,
            audit_type=AuditType.SECURITY_SCAN,
            status=AuditLogStatus.PASSED if security_result['status'] == 'passed' else AuditLogStatus.FAILED,
            details={"issues": security_result['issues']}
        )
        db.add(security_log)
        audit_results.append(security_result)

        # 2. Metadata Check
        validator = MetadataValidator()
        metadata_result = validator.validate(tmp_path)
        metadata_log = AuditLog(
            id=str(uuid.uuid4())[:32],
            version_id=version_id,
            audit_type=AuditType.METADATA_CHECK,
            status=AuditLogStatus.PASSED if metadata_result['status'] == 'passed' else AuditLogStatus.FAILED,
            details={"issues": metadata_result['issues']}
        )
        db.add(metadata_log)
        audit_results.append(metadata_result)

        # Update version audit status
        all_passed = all(r['status'] == 'passed' for r in audit_results)
        if all_passed:
            app_version.audit_status = AuditStatus.AUTO_PASSED
        else:
            app_version.audit_status = AuditStatus.AUTO_FAILED

        # Store metadata if validation passed
        if metadata_result.get('manifest'):
            app_version.metadata = metadata_result['manifest']

        db.commit()

        return {
            "version_id": version_id,
            "audit_status": app_version.audit_status,
            "audit_results": audit_results
        }

    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.get("/{version_id}/audit")
async def get_audit_status(
    version_id: str,
    db: Session = Depends(get_db)
):
    """Get audit status for a version"""
    version = db.query(AppVersion).filter(AppVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    audit_logs = db.query(AuditLog).filter(AuditLog.version_id == version_id).all()

    return {
        "version_id": version_id,
        "audit_status": version.audit_status,
        "audit_logs": [
            {
                "audit_type": log.audit_type,
                "status": log.status,
                "details": log.details,
                "created_at": log.created_at
            }
            for log in audit_logs
        ]
    }
