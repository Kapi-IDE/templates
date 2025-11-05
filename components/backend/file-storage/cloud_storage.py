"""
Simple File Storage Component

Supports both local filesystem and cloud storage (Cloudinary/S3).
For MVP: Uses local filesystem with optional cloud upload.

Environment Variables:
    STORAGE_TYPE: "local" or "cloudinary" or "s3"
    UPLOAD_DIR: Local storage directory (default: "./uploads")
    CLOUDINARY_URL: Cloudinary connection string (optional)
    AWS_ACCESS_KEY_ID: AWS access key (optional)
    AWS_SECRET_ACCESS_KEY: AWS secret key (optional)
    AWS_S3_BUCKET: S3 bucket name (optional)
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import hashlib


class LocalStorage:
    """Simple local filesystem storage"""

    def __init__(self, upload_dir: str = "./uploads"):
        """Initialize local storage

        Args:
            upload_dir: Directory to store uploaded files
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories by date
        self.memes_dir = self.upload_dir / "memes"
        self.templates_dir = self.upload_dir / "templates"
        self.memes_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)

    def _generate_filename(self, original_filename: str, content: bytes) -> str:
        """Generate unique filename

        Args:
            original_filename: Original file name
            content: File content bytes

        Returns:
            Unique filename
        """
        # Use hash of content for deduplication
        content_hash = hashlib.md5(content).hexdigest()[:8]

        # Get file extension
        ext = Path(original_filename).suffix.lower() or ".png"

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        return f"{timestamp}_{content_hash}_{unique_id}{ext}"

    def save_meme(
        self,
        content: bytes,
        filename: Optional[str] = None
    ) -> Tuple[str, str]:
        """Save meme to storage

        Args:
            content: Image bytes
            filename: Original filename (optional)

        Returns:
            Tuple of (file_id, public_url)
        """
        # Generate unique filename
        if filename is None:
            filename = "meme.png"

        unique_filename = self._generate_filename(filename, content)
        file_path = self.memes_dir / unique_filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        # Generate public URL (relative path)
        public_url = f"/uploads/memes/{unique_filename}"

        return unique_filename, public_url

    def save_template(
        self,
        content: bytes,
        filename: str
    ) -> Tuple[str, str]:
        """Save template image to storage

        Args:
            content: Image bytes
            filename: Original filename

        Returns:
            Tuple of (file_id, public_url)
        """
        unique_filename = self._generate_filename(filename, content)
        file_path = self.templates_dir / unique_filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        # Generate public URL
        public_url = f"/uploads/templates/{unique_filename}"

        return unique_filename, public_url

    def get_meme(self, file_id: str) -> Optional[bytes]:
        """Retrieve meme by file ID

        Args:
            file_id: File identifier

        Returns:
            Image bytes or None if not found
        """
        file_path = self.memes_dir / file_id

        if not file_path.exists():
            return None

        with open(file_path, "rb") as f:
            return f.read()

    def delete_meme(self, file_id: str) -> bool:
        """Delete meme by file ID

        Args:
            file_id: File identifier

        Returns:
            True if deleted, False if not found
        """
        file_path = self.memes_dir / file_id

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def list_memes(self, limit: int = 50) -> list:
        """List recent memes

        Args:
            limit: Maximum number of results

        Returns:
            List of file info dicts
        """
        files = []

        for file_path in sorted(
            self.memes_dir.iterdir(),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]:
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "file_id": file_path.name,
                    "url": f"/uploads/memes/{file_path.name}",
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                })

        return files


class CloudinaryStorage:
    """Cloudinary cloud storage (optional)"""

    def __init__(self, cloudinary_url: Optional[str] = None):
        """Initialize Cloudinary storage

        Args:
            cloudinary_url: Cloudinary connection URL

        Raises:
            ImportError: If cloudinary package not installed
        """
        try:
            import cloudinary
            import cloudinary.uploader
            self.cloudinary = cloudinary
            self.uploader = cloudinary.uploader
        except ImportError:
            raise ImportError(
                "Cloudinary package not installed. "
                "Run: pip install cloudinary"
            )

        # Configure Cloudinary
        url = cloudinary_url or os.getenv("CLOUDINARY_URL")
        if url:
            cloudinary.config(cloudinary_url=url)

    def save_meme(
        self,
        content: bytes,
        filename: Optional[str] = None
    ) -> Tuple[str, str]:
        """Save meme to Cloudinary

        Args:
            content: Image bytes
            filename: Original filename (optional)

        Returns:
            Tuple of (public_id, public_url)
        """
        result = self.uploader.upload(
            content,
            folder="memes",
            resource_type="image"
        )

        return result["public_id"], result["secure_url"]

    def delete_meme(self, public_id: str) -> bool:
        """Delete meme from Cloudinary

        Args:
            public_id: Cloudinary public ID

        Returns:
            True if deleted successfully
        """
        result = self.uploader.destroy(public_id)
        return result.get("result") == "ok"


class S3Storage:
    """AWS S3 cloud storage (optional)"""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None
    ):
        """Initialize S3 storage

        Args:
            bucket_name: S3 bucket name
            aws_access_key: AWS access key ID
            aws_secret_key: AWS secret access key

        Raises:
            ImportError: If boto3 package not installed
        """
        try:
            import boto3
            self.boto3 = boto3
        except ImportError:
            raise ImportError(
                "boto3 package not installed. "
                "Run: pip install boto3"
            )

        self.bucket_name = bucket_name or os.getenv("AWS_S3_BUCKET")

        # Initialize S3 client
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key or os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=aws_secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def save_meme(
        self,
        content: bytes,
        filename: Optional[str] = None
    ) -> Tuple[str, str]:
        """Save meme to S3

        Args:
            content: Image bytes
            filename: Original filename (optional)

        Returns:
            Tuple of (object_key, public_url)
        """
        # Generate unique key
        unique_id = str(uuid.uuid4())
        object_key = f"memes/{unique_id}.png"

        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=object_key,
            Body=content,
            ContentType="image/png"
        )

        # Generate public URL
        public_url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_key}"

        return object_key, public_url

    def delete_meme(self, object_key: str) -> bool:
        """Delete meme from S3

        Args:
            object_key: S3 object key

        Returns:
            True if deleted successfully
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except Exception:
            return False


def create_storage(storage_type: Optional[str] = None):
    """Factory function to create storage instance

    Args:
        storage_type: "local", "cloudinary", or "s3" (defaults to env var or "local")

    Returns:
        Storage instance
    """
    storage_type = storage_type or os.getenv("STORAGE_TYPE", "local")

    if storage_type == "cloudinary":
        return CloudinaryStorage()
    elif storage_type == "s3":
        return S3Storage()
    else:
        return LocalStorage()


# Example usage
if __name__ == "__main__":
    # Create local storage
    storage = create_storage("local")

    print(f"Storage initialized: {type(storage).__name__}")
    print(f"Upload directory: {storage.upload_dir if hasattr(storage, 'upload_dir') else 'N/A'}")

    # Example save
    # file_id, url = storage.save_meme(image_bytes, "my_meme.png")
    # print(f"Saved: {file_id} -> {url}")
