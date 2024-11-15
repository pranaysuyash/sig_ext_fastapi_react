# # # # # # # # # # # # # backend/app/main.py
# # # # # # # # # # # # from fastapi import FastAPI
# # # # # # # # # # # # from app.routers import auth, extraction
# # # # # # # # # # # # from app.database import Base, engine
# # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # from app.config import settings

# # # # # # # # # # # # app = FastAPI(
# # # # # # # # # # # #     title="Signature Extraction App",
# # # # # # # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # # # # # # #     version="1.0.0"
# # # # # # # # # # # # )

# # # # # # # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # # # # # # Configure CORS
# # # # # # # # # # # # origins = [
# # # # # # # # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # # # # # # # #     "http://localhost:5173",  # Your actual frontend port
# # # # # # # # # # # #     # Add your production frontend URL here
# # # # # # # # # # # # ]

# # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # #     allow_origins=origins,  # Updated origins
# # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # )

# # # # # # # # # # # # # Include routers
# # # # # # # # # # # # app.include_router(auth.router)
# # # # # # # # # # # # app.include_router(extraction.router)

# # # # # # # # # # # # @app.get("/")
# # # # # # # # # # # # def read_root():
# # # # # # # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}


# # # # # # # # # # # # backend/app/main.py
# # # # # # # # # # # from fastapi import FastAPI
# # # # # # # # # # # from app.routers import auth, extraction
# # # # # # # # # # # from app.database import Base, engine
# # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # from app.config import settings

# # # # # # # # # # # app = FastAPI(
# # # # # # # # # # #     title="Signature Extraction App",
# # # # # # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # # # # # #     version="1.0.0"
# # # # # # # # # # # )

# # # # # # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # # # # # Configure CORS with updated origins
# # # # # # # # # # # origins = [
# # # # # # # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # # # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # # # # # # #     # Add your production frontend URL here
# # # # # # # # # # # ]

# # # # # # # # # # # app.add_middleware(
# # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # #     allow_origins=origins,
# # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # )

# # # # # # # # # # # # Include routers
# # # # # # # # # # # app.include_router(auth.router)
# # # # # # # # # # # app.include_router(extraction.router)

# # # # # # # # # # # @app.get("/")
# # # # # # # # # # # def read_root():
# # # # # # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}

# # # # # # # # # # # backend/app/main.py
# # # # # # # # # # from fastapi import FastAPI
# # # # # # # # # # from app.routers import auth, extraction
# # # # # # # # # # from app.database import Base, engine
# # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # from app.config import settings

# # # # # # # # # # app = FastAPI(
# # # # # # # # # #     title="Signature Extraction App",
# # # # # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # # # # #     version="1.0.0"
# # # # # # # # # # )

# # # # # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # # # # Configure CORS with updated origins
# # # # # # # # # # origins = [
# # # # # # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # # # # # #     # Add your production frontend URL here
# # # # # # # # # # ]

# # # # # # # # # # app.add_middleware(
# # # # # # # # # #     CORSMiddleware,
# # # # # # # # # #     allow_origins=origins,
# # # # # # # # # #     allow_credentials=True,
# # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # )

# # # # # # # # # # # Include routers
# # # # # # # # # # app.include_router(auth.router)
# # # # # # # # # # app.include_router(extraction.router)

# # # # # # # # # # @app.get("/")
# # # # # # # # # # def read_root():
# # # # # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}

# # # # # # # # # from fastapi import FastAPI
# # # # # # # # # from app.routers import auth, extraction
# # # # # # # # # from app.database import Base, engine
# # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # from app.config import settings

# # # # # # # # # # Create the database tables
# # # # # # # # # Base.metadata.create_all(bind=engine)

# # # # # # # # # app = FastAPI(
# # # # # # # # #     title="Signature Extraction App",
# # # # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # # # #     version="1.0.0"
# # # # # # # # # )

# # # # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # # # Configure CORS with updated origins
# # # # # # # # # origins = [
# # # # # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # # # # #     # Add your production frontend URL here
# # # # # # # # # ]

# # # # # # # # # app.add_middleware(
# # # # # # # # #     CORSMiddleware,
# # # # # # # # #     allow_origins=origins,
# # # # # # # # #     allow_credentials=True,
# # # # # # # # #     allow_methods=["*"],
# # # # # # # # #     allow_headers=["*"],
# # # # # # # # # )

# # # # # # # # # # Include routers
# # # # # # # # # app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# # # # # # # # # app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# # # # # # # # # @app.get("/")
# # # # # # # # # def read_root():
# # # # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}

# # # # # # # # from fastapi import FastAPI
# # # # # # # # from app.routers import auth, extraction
# # # # # # # # from app.database import Base, engine
# # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # from app.config import settings

# # # # # # # # # Create the database tables
# # # # # # # # Base.metadata.create_all(bind=engine)

# # # # # # # # app = FastAPI(
# # # # # # # #     title="Signature Extraction App",
# # # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # # #     version="1.0.0"
# # # # # # # # )

# # # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # # Configure CORS with updated origins
# # # # # # # # origins = [
# # # # # # # #     "http://localhost:8000",  # React frontend during development
# # # # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # # # #     # Add your production frontend URL here
# # # # # # # # ]

# # # # # # # # app.add_middleware(
# # # # # # # #     CORSMiddleware,
# # # # # # # #     allow_origins=origins,
# # # # # # # #     allow_credentials=True,
# # # # # # # #     allow_methods=["*"],
# # # # # # # #     allow_headers=["*"],
# # # # # # # # )

# # # # # # # # # Include routers
# # # # # # # # app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# # # # # # # # app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# # # # # # # # @app.get("/")
# # # # # # # # def read_root():
# # # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}


# # # # # # # from fastapi import FastAPI
# # # # # # # from app.routers import auth, extraction
# # # # # # # from app.database import Base, engine
# # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # from app.config import settings

# # # # # # # # Create the database tables
# # # # # # # Base.metadata.create_all(bind=engine)

# # # # # # # app = FastAPI(
# # # # # # #     title="Signature Extraction App",
# # # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # # #     version="1.0.0"
# # # # # # # )

# # # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # # Configure CORS with updated origins
# # # # # # # origins = [
# # # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # # #     # Add your production frontend URL here
# # # # # # # ]

# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=origins,
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )

# # # # # # # # Include routers
# # # # # # # app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# # # # # # # app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# # # # # # # @app.get("/")
# # # # # # # def read_root():
# # # # # # #     return {"message": "Welcome to the Signature Extraction App API"}
# # # # # # from fastapi import FastAPI
# # # # # # from app.routers import auth, extraction
# # # # # # from app.database import Base, engine
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # from app.config import settings

# # # # # # # Create the database tables
# # # # # # Base.metadata.create_all(bind=engine)

# # # # # # app = FastAPI(
# # # # # #     title="Signature Extraction App",
# # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # #     version="1.0.0"
# # # # # # )

# # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # Configure CORS with updated origins
# # # # # # origins = [
# # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # #     # Add your production frontend URL here
# # # # # # ]

# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=origins,
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # # Include routers
# # # # # # app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# # # # # # app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# # # # # # @app.get("/")
# # # # # # def read_root():
# # # # # #     return {"message": "Welcome to the Signature Extraction App API"}


# # # # # # from fastapi import FastAPI
# # # # # # from app.routers import auth_router, extraction_router
# # # # # # from app.database import Base, engine
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # from app.config import settings

# # # # # # # Create the database tables
# # # # # # Base.metadata.create_all(bind=engine)

# # # # # # app = FastAPI(
# # # # # #     title="Signature Extraction App",
# # # # # #     description="API for user authentication and signature extraction from images.",
# # # # # #     version="1.0.0"
# # # # # # )

# # # # # # # Mount static files (for serving uploaded images and signatures)
# # # # # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # # # # # Configure CORS with updated origins
# # # # # # origins = [
# # # # # #     "http://localhost:3000",  # React frontend during development
# # # # # #     "http://localhost:5173",  # Vite frontend port
# # # # # #     # Add your production frontend URL here
# # # # # # ]

# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=origins,
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )


# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Add your frontend URL
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )
# # # # # # # Include routers
# # # # # # app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# # # # # # app.include_router(extraction_router, prefix="/extraction", tags=["Extraction"])

# # # # # # @app.get("/")
# # # # # # def read_root():
# # # # # #     return {"message": "Welcome to the Signature Extraction App API"}



# # # # # from fastapi import FastAPI
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from app.routers import auth, extraction
# # # # # from app.database import Base, engine

# # # # # # Create database tables
# # # # # Base.metadata.create_all(bind=engine)

# # # # # app = FastAPI(title="Signature Extractor API")

# # # # # # Configure CORS
# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Add your Vite dev server URL
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # Include routers
# # # # # app.include_router(auth.router)
# # # # # app.include_router(extraction.router)

# # # # # @app.get("/health")
# # # # # async def health_check():
# # # # #     return {"status": "healthy"}

# # # # from fastapi import FastAPI
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from app.routers import auth, extraction
# # # # from app.database import Base, engine

# # # # # Create database tables
# # # # Base.metadata.create_all(bind=engine)

# # # # app = FastAPI(title="Signature Extractor API")

# # # # # Configure CORS
# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Add your Vite dev server URL
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )

# # # # # Include routers
# # # # app.include_router(auth.router)
# # # # app.include_router(extraction.router)

# # # # @app.get("/health")
# # # # async def health_check():
# # # #     return {"status": "healthy"}

# # # from fastapi import FastAPI
# # # from fastapi.middleware.cors import CORSMiddleware
# # # import logging

# # # from app.routers import auth, extraction
# # # from app.database import Base, engine

# # # # Configure logging
# # # logging.basicConfig(
# # #     level=logging.DEBUG,
# # #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# # # )

# # # # Create database tables
# # # Base.metadata.create_all(bind=engine)

# # # app = FastAPI(title="Signature Extractor API")

# # # # Configure CORS
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # Include routers
# # # app.include_router(auth.router)
# # # app.include_router(extraction.router)

# # # @app.get("/health")
# # # async def health_check():
# # #     return {"status": "healthy"}

# # from fastapi import FastAPI, HTTPException, Depends, status
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # from app.routers import auth, extraction
# # from app.database import Base, engine
# # from app.config import settings
# # import os
# # import logging
# # import sys

# # # Create the database tables
# # Base.metadata.create_all(bind=engine)

# # # Set up logging
# # logging.basicConfig(
# #     level=logging.DEBUG,
# #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #     handlers=[
# #         logging.StreamHandler(sys.stdout),
# #         logging.FileHandler('app.log')
# #     ]
# # )

# # logger = logging.getLogger(__name__)

# # app = FastAPI(
# #     title="Signature Extraction App",
# #     description="API for user authentication and signature extraction from images.",
# #     version="1.0.0"
# # )

# # # Ensure uploads directory exists
# # UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
# # os.makedirs(UPLOADS_DIR, exist_ok=True)
# # logger.info(f"Uploads directory configured at: {UPLOADS_DIR}")

# # # Mount static files (for serving uploaded images and signatures)
# # try:
# #     app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
# #     logger.info("Successfully mounted uploads directory")
# # except Exception as e:
# #     logger.error(f"Failed to mount uploads directory: {str(e)}")
# #     raise

# # # Configure CORS with all necessary origins
# # origins = [
# #     "http://localhost:3000",
# #     "http://localhost:5173",
# #     "http://127.0.0.1:8000",
# #     "http://localhost:8000",
# #     "http://127.0.0.1:5173",
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Health check endpoint
# # @app.get("/health")
# # async def health_check():
# #     return {
# #         "status": "healthy",
# #         "uploads_dir": UPLOADS_DIR,
# #         "uploads_dir_exists": os.path.exists(UPLOADS_DIR)
# #     }

# # # Include routers
# # app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# # app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# # @app.get("/")
# # async def read_root():
# #     return {"message": "Welcome to the Signature Extraction App API"}

# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from app.routers import auth, extraction
# from app.database import Base, engine
# from app.config import settings
# import os
# import logging
# import sys

# # Create the database tables
# Base.metadata.create_all(bind=engine)

# # Set up logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(sys.stdout),
#         logging.FileHandler('app.log')
#     ]
# )

# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Signature Extraction App",
#     description="API for user authentication and signature extraction from images.",
#     version="1.0.0"
# )

# # Ensure uploads directory exists
# UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
# os.makedirs(UPLOADS_DIR, exist_ok=True)
# logger.info(f"Uploads directory configured at: {UPLOADS_DIR}")

# # Mount static files (for serving uploaded images and signatures)
# try:
#     app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
#     logger.info("Successfully mounted uploads directory")
# except Exception as e:
#     logger.error(f"Failed to mount uploads directory: {str(e)}")
#     raise

# # Configure CORS with all necessary origins
# origins = [
#     "http://localhost:3000",
#     "http://localhost:5173",
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
#     "http://127.0.0.1:5173",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Health check endpoint
# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "uploads_dir": UPLOADS_DIR,
#         "uploads_dir_exists": os.path.exists(UPLOADS_DIR)
#     }

# # Include routers
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the Signature Extraction App API"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, extraction
from app.database import Base, engine
import os
import logging
import sys

# Create the database tables
Base.metadata.create_all(bind=engine)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
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
    "http://127.0.0.1:8000",
    "http://localhost:8000",
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
