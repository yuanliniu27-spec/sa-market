from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import hashlib
from typing import BinaryIO


class StorageService:
    """MinIO storage service for file uploads"""

    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket()

    def _ensure_bucket(self):
        """Create bucket if not exists"""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(
        self,
        file_path: str,
        app_id: str,
        filename: str
    ) -> str:
        """Upload file to MinIO and return URL"""
        object_name = f"applications/{app_id}/{filename}"

        try:
            self.client.fput_object(
                self.bucket,
                object_name,
                file_path
            )

            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=7 * 24 * 60 * 60  # 7 days
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    def upload_fileobj(
        self,
        file_obj: BinaryIO,
        app_id: str,
        filename: str,
        file_size: int
    ) -> str:
        """Upload file object to MinIO"""
        object_name = f"applications/{app_id}/{filename}"

        try:
            self.client.put_object(
                self.bucket,
                object_name,
                file_obj,
                file_size
            )

            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=7 * 24 * 60 * 60
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    def delete_file(self, object_name: str) -> bool:
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket, object_name)
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False

    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
