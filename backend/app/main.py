
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

# Set up logging with local timezone timestamps

class LocalTimeFormatter(logging.Formatter):
    """Formatter that renders asctime in the user's local timezone."""

    converter = time.localtime


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

_formatter = LocalTimeFormatter(LOG_FORMAT, DATE_FORMAT)

_stream_handler = logging.StreamHandler(sys.stdout)
_stream_handler.setFormatter(_formatter)

_file_handler = logging.FileHandler("app.log")
_file_handler.setFormatter(_formatter)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[_stream_handler, _file_handler],
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Signature Extraction App",
    description="API for user authentication and signature extraction from images.",
    version="1.0.0"
)

# Ensure uploads directory exists
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "images"))
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
    return {"message": "Welcome to the Signature Extraction App API"}
