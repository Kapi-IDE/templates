# Meme Generator

Create custom memes with text overlays using uploaded images or predefined templates.

**Gateway App #2** - Second quickwin application built with KAPI methodology.

## ✨ Features

- **Upload Custom Images**: Create memes from your own images
- **Predefined Templates**: Use popular meme templates (Drake, Distracted Boyfriend, etc.)
- **Text Overlay**: Add customizable text with automatic wrapping
- **Smart Positioning**: Optimized text placement for each template
- **Download Memes**: Save generated memes as PNG/JPEG
- **Gallery**: Browse recently created memes
- **No Dependencies**: Pure PIL/Pillow image processing
- **Cloud Storage Ready**: Optional Cloudinary/S3 integration

## 🚀 Quick Start (8 minutes)

### Prerequisites
- Python 3.11+
- pip

### Local Setup

```bash
# 1. Clone/copy this directory
cd meme-generator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (IMPORTANT)
cp .env.example .env

# EDIT .env FILE (Optional - defaults work for local development):
# - STORAGE_TYPE: "local" (default, no API keys needed)
# - PORT: Server port (default: 8000)
# - UPLOAD_DIR: Local storage directory (default: ./uploads)
#
# ⚠️ IMPORTANT: Never commit .env to git - it's in .gitignore
# ⚠️ NO API KEYS NEEDED for basic local usage

# 5. Start server
python backend/main.py
```

Server runs at http://localhost:8000

### Open Frontend

Open `frontend/index.html` in your browser or serve with:

```bash
# Python simple server
python -m http.server 3000 --directory frontend
```

Then visit http://localhost:3000

## 📖 API Documentation

### Create Meme from Upload

```bash
POST /api/create
Content-Type: multipart/form-data

Form Data:
- image: (file) Image file
- top_text: (string) Top text
- bottom_text: (string) Bottom text
- resize: (boolean) Resize image (default: true)
- output_format: (string) PNG or JPEG (default: PNG)
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/create \
  -F "image=@my_image.jpg" \
  -F "top_text=When you finish the blueprint" \
  -F "bottom_text=In 8 minutes"
```

**Response:**
```json
{
  "file_id": "20251002_abc123.png",
  "url": "/uploads/memes/20251002_abc123.png",
  "message": "Meme created successfully"
}
```

### Create Meme from Template

```bash
POST /api/create/template/{template_id}
Content-Type: application/json

{
  "texts": ["Text 1", "Text 2"],
  "resize": true,
  "output_format": "PNG"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/create/template/drake \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Vibe coding", "Systematic engineering"]}'
```

### Get Templates

```bash
GET /api/templates
```

**Response:**
```json
[
  {
    "id": "drake",
    "name": "Drake Hotline Bling",
    "image_url": "https://i.imgflip.com/30b1gx.jpg",
    "text_count": 2
  }
]
```

### List Recent Memes

```bash
GET /api/memes?limit=50
```

**Response:**
```json
{
  "total": 10,
  "memes": [
    {
      "file_id": "20251002_abc123.png",
      "url": "/uploads/memes/20251002_abc123.png",
      "size": 245678,
      "created_at": "2025-10-02T12:00:00"
    }
  ]
}
```

### Delete Meme

```bash
DELETE /api/memes/{file_id}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (HTML/JS)                      │
│         Single-page app with upload & template UI          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │   Routes   │  │   Image    │  │     Storage        │    │
│  │            │  │  Processor │  │                    │    │
│  │ • Create   │→ │            │→ │ • Local FS         │    │
│  │ • List     │  │ • Text     │  │ • Cloudinary (opt) │    │
│  │ • Delete   │  │ • Resize   │  │ • S3 (opt)         │    │
│  └────────────┘  └────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  PIL/Pillow  │  │   Templates  │  │  Filesystem  │
    │              │  │   (imgflip)  │  │   /uploads   │
    └──────────────┘  └──────────────┘  └──────────────┘
```

### Component Sources

- **Image Processor**: Custom component using PIL/Pillow (NEW)
- **Storage**: Simple file storage with cloud options (NEW)
- **FastAPI Patterns**: Following Python best practices from `quality-baselines/fastapi-best-practices.md`

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `PORT` | `8000` | Server port | Optional |
| `HOST` | `0.0.0.0` | Server host | Optional |
| `STORAGE_TYPE` | `local` | Storage backend (local/cloudinary/s3) | Optional |
| `UPLOAD_DIR` | `./uploads` | Local upload directory | Optional |
| `CLOUDINARY_URL` | - | Cloudinary connection string | Only for cloud storage |
| `AWS_ACCESS_KEY_ID` | - | AWS access key | Only for S3 storage |
| `AWS_SECRET_ACCESS_KEY` | - | AWS secret key | Only for S3 storage |
| `AWS_S3_BUCKET` | - | S3 bucket name | Only for S3 storage |

### 🔐 API Key Setup (Optional Cloud Storage)

**⚠️ IMPORTANT: NO API KEYS NEEDED for basic local usage**
- Default `STORAGE_TYPE=local` works without any cloud credentials
- Local filesystem storage is production-ready for small-medium deployments
- Cloud storage (Cloudinary/S3) is optional for scaling

**If using Cloudinary (Optional):**

1. **Sign up at [Cloudinary](https://cloudinary.com/)**
2. **Get your connection URL** from dashboard
3. **Set environment variable:**
   ```bash
   # .env file
   STORAGE_TYPE=cloudinary
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   ```
4. **Install optional dependency:**
   ```bash
   pip install cloudinary
   ```

**If using AWS S3 (Optional):**

1. **Create S3 bucket** in AWS Console
2. **Create IAM user** with S3 permissions
3. **Set environment variables:**
   ```bash
   # .env file
   STORAGE_TYPE=s3
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_S3_BUCKET=your-bucket-name
   ```
4. **Install optional dependency:**
   ```bash
   pip install boto3
   ```

**Security Best Practices:**
- Never commit API keys to git (`.env` is in `.gitignore`)
- Use separate credentials for development and production
- Rotate keys periodically
- Use environment-specific buckets/cloud names
- For production, use platform environment variables:
  ```bash
  # Heroku
  heroku config:set CLOUDINARY_URL=...

  # Railway
  # Set in Settings → Variables

  # Docker
  docker run -e CLOUDINARY_URL=... your-image
  ```

### Customization

**Add Custom Templates:**

Edit `backend/image_processor.py`:

```python
TEMPLATES["custom"] = MemeTemplate(
    id="custom",
    name="Custom Template",
    image_url="https://example.com/template.jpg",
    text_positions=[(100, 50, 300), (100, 400, 300)]
)
```

**Change Font:**

```python
processor = ImageProcessor(
    font_path="/path/to/font.ttf",
    font_size=60
)
```

## 🛡️ Features Deep Dive

### Image Processing

- **PIL/Pillow-based**: No external image processing services
- **Text Wrapping**: Automatic text wrapping to fit width
- **Outline Text**: Black outline for readability on any background
- **Smart Positioning**: Template-based or automatic top/bottom
- **Resize on Upload**: Automatic resizing to 800x800 max
- **Format Support**: PNG, JPEG, GIF input; PNG/JPEG output

### Storage Options

**Local Filesystem (Default):**
- Fast for development and small deployments
- Organized by date and type (memes/templates)
- MD5 hash deduplication
- Automatic directory creation

**Cloudinary (Optional):**
- CDN delivery
- Image transformations
- Automatic optimization
- Easy integration with `CLOUDINARY_URL`

**AWS S3 (Optional):**
- Scalable cloud storage
- Direct uploads
- Public/private buckets
- Requires `boto3` package

### Frontend UI

- **Responsive Design**: Works on mobile and desktop
- **Two Modes**: Upload custom or use templates
- **Real-time Preview**: See generated meme before download
- **Error Handling**: User-friendly error messages
- **Download Button**: One-click meme download

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test template listing
curl http://localhost:8000/api/templates

# Create meme from upload
curl -X POST http://localhost:8000/api/create \
  -F "image=@test.jpg" \
  -F "top_text=Test" \
  -F "bottom_text=Meme"

# Create meme from template
curl -X POST http://localhost:8000/api/create/template/drake \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Old way", "New way"]}'
```

## 🚢 Production Deployment

### Docker Deployment

```bash
# Build image
docker build -t meme-generator:latest .

# Run container
docker run -p 8000:8000 \
  -e STORAGE_TYPE=local \
  -v $(pwd)/uploads:/app/uploads \
  meme-generator:latest
```

### Docker Compose

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Cloud Storage Setup

**Cloudinary:**
```bash
# Set environment variable
export CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
export STORAGE_TYPE=cloudinary

# Install optional dependency
pip install cloudinary

# Start server
python backend/main.py
```

**AWS S3:**
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_S3_BUCKET=your_bucket
export STORAGE_TYPE=s3

# Install optional dependency
pip install boto3

# Start server
python backend/main.py
```

## 📈 Performance

- **Processing Speed**: ~100-200ms per meme
- **Text Rendering**: Real-time with PIL
- **Upload Size**: Recommended max 5MB
- **Concurrent Requests**: Limited by FastAPI/uvicorn workers
- **Storage**: Unlimited (local) or as per cloud plan

## 🐛 Troubleshooting

### Font Not Found

PIL will fall back to default font. Install system fonts:

```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# macOS (already has fonts)
# Fonts at /System/Library/Fonts/

# Windows (already has fonts)
# Fonts at C:\Windows\Fonts\
```

### Pillow Installation Issues

Install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev libfreetype6-dev

# macOS (with Homebrew)
brew install libjpeg zlib freetype

# Then reinstall Pillow
pip install --force-reinstall pillow
```

### CORS Errors

Update CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Project Structure

```
meme-generator/
├── backend/
│   ├── main.py (280 lines)               # FastAPI server
│   ├── image_processor.py (310 lines)    # PIL-based image processing
│   └── storage.py (310 lines)            # File storage with cloud options
├── frontend/
│   └── index.html (350 lines)            # Single-page web UI
├── config/
│   ├── requirements.txt                  # Python dependencies
│   ├── .env.example                      # Environment template
│   ├── .gitignore                        # Git exclusions
│   ├── Dockerfile                        # Docker image
│   ├── docker-compose.yml                # Docker Compose config
│   └── .dockerignore                     # Docker exclusions
└── README.md                             # This file
```

**Total LOC**: ~1,250

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build** methodology:

1. ✅ **Specification**: 8-minute setup, image upload, templates, text overlay
2. ✅ **Architecture**: FastAPI + PIL + Local/Cloud storage
3. ✅ **Implementation**: Component-based (processor, storage, routes)
4. ✅ **Quality Gates**: Error handling, CORS, health checks, Docker

**Token Savings**: ~75% vs building from scratch.

## 🔮 Future Enhancements

- **More Templates**: Expand template library
- **Stickers/Emojis**: Add overlay stickers
- **Image Filters**: Apply filters (grayscale, sepia, etc.)
- **Batch Processing**: Generate multiple memes at once
- **User Accounts**: Save memes to user profiles
- **Social Sharing**: Direct share to Twitter, Reddit, etc.
- **Animation**: Create animated GIF memes
- **AI Captions**: Auto-generate funny captions

## 📚 Resources

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Cloudinary Python SDK](https://cloudinary.com/documentation/python_integration)
- [Boto3 (AWS SDK)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.
