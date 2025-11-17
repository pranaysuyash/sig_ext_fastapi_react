
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.routers import auth, extraction
from backend.app.database import Base, engine
import os
import logging
import sys
import time

# Create the database tables
Base.metadata.create_all(bind=engine)

# Set up logging with local timezone timestamps to a user-writable location

class LocalTimeFormatter(logging.Formatter):
    """Formatter that renders asctime in the user's local timezone."""

    converter = time.localtime


def _get_user_data_dir() -> str:
    """Return a user-writable base directory for app data/logs/uploads."""
    app_name = "SignKit"
    if sys.platform == "darwin":
        base = os.path.expanduser(f"~/Library/Application Support/{app_name}")
    elif sys.platform == "win32":
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), app_name)
    else:
        base = os.path.expanduser(f"~/.local/share/{app_name}")
    os.makedirs(base, exist_ok=True)
    return base


USER_DATA_DIR = _get_user_data_dir()
LOG_DIR = os.path.join(USER_DATA_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "app.log")

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

_formatter = LocalTimeFormatter(LOG_FORMAT, DATE_FORMAT)

_stream_handler = logging.StreamHandler(sys.stdout)
_stream_handler.setFormatter(_formatter)

handlers = [_stream_handler]
try:
    _file_handler = logging.FileHandler(LOG_PATH)
    _file_handler.setFormatter(_formatter)
    handlers.append(_file_handler)
except Exception:
    # If file logging fails, continue with stream-only logging
    pass

logging.basicConfig(
    level=logging.DEBUG,
    handlers=handlers,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="SignKit Backend",
    description="API for user authentication and signature extraction from images.",
    version="1.0.0"
)

# Ensure uploads directory exists in a user-writable location
UPLOADS_DIR = os.path.join(USER_DATA_DIR, "uploads", "images")
os.makedirs(UPLOADS_DIR, exist_ok=True)
logger.info(f"Uploads directory configured at: {UPLOADS_DIR}")

# Mount static files (for serving uploaded images and signatures)
try:
    app.mount("/uploads/images", StaticFiles(directory=UPLOADS_DIR), name="uploads")
    logger.info("Successfully mounted uploads directory")
except Exception as e:
    logger.error(f"Failed to mount uploads directory: {str(e)}")
    raise

# Configure CORS with all necessary origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173", 
    "http://127.0.0.1:8001",  # Updated to match consistent port
    "http://localhost:8001",  # Updated to match consistent port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uploads_dir": UPLOADS_DIR,
        "uploads_dir_exists": os.path.exists(UPLOADS_DIR)
    }

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the SignKit API"}
