# Cloud File Storage (Python)

Unified interface for saving files to the local filesystem, Cloudinary, or AWS S3.

## Install
```bash
pip install pillow boto3 cloudinary
```

## Usage
```python
from cloud_storage import create_storage

storage = create_storage("local")
file_id, url = storage.save_meme(image_bytes, filename="photo.jpg")

cloud_storage = create_storage("cloudinary")
cloud_storage.save_meme(image_bytes)
```

Environment variables:
- `CLOUDINARY_URL` (when using Cloudinary)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET` (for S3)
