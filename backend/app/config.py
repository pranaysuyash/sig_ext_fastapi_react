# # # # # backend/app/config.py

# # # # from pydantic_settings import BaseSettings

# # # # class Settings(BaseSettings):
# # # #     DATABASE_URL: str = "postgresql://pranay:pranay@localhost:5432/signature_extractor"
# # # #     JWT_SECRET: str = "your_jwt_secret_key"  # Replace with your actual secret key or use an environment variable
# # # #     JWT_ALGORITHM: str = "HS256"  # The algorithm used for JWT
# # # #     JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Duration for JWT expiration
# # # #     RAZORPAY_KEY_ID: str = "your_razorpay_key_id"  # Replace with your actual Razorpay key ID
# # # #     RAZORPAY_KEY_SECRET: str = "your_razorpay_key_secret"  # Replace with your actual Razorpay key secret

# # # #     class Config:
# # # #         env_file = ".env"  # Ensure you have an .env file in your project root if needed

# # # # settings = Settings()


# # # # backend/app/config.py

# # # from pydantic_settings import BaseSettings  # Import BaseSettings from pydantic_settings
# # # from pydantic import Field, ValidationError  # Import Field and ValidationError from pydantic

# # # class Settings(BaseSettings):
# # #     DATABASE_URL: str = Field(..., env="DATABASE_URL")
# # #     JWT_SECRET: str = Field(..., env="JWT_SECRET")
# # #     JWT_ALGORITHM: str = "HS256"
# # #     JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
# # #     RAZORPAY_KEY_ID: str = Field(..., env="RAZORPAY_KEY_ID")
# # #     RAZORPAY_KEY_SECRET: str = Field(..., env="RAZORPAY_KEY_SECRET")

# # #     class Config:
# # #         env_file = ".env"  # Use an .env file for local development

# # # # Instantiate the settings, which automatically validates all required fields
# # # try:
# # #     settings = Settings()
# # # except ValidationError as e:
# # #     print("Configuration validation error:", e)
# # #     raise e


# # from pydantic_settings import BaseSettings  # Import BaseSettings from pydantic_settings
# # from pydantic import Field, ValidationError  # Import Field and ValidationError from pydantic

# # class Settings(BaseSettings):
# #     DATABASE_HOSTNAME: str = 'localhost'
# #     DATABASE_PORT: str = '5432'
# #     DATABASE_PASSWORD: str = 'pranay'  # Update with your PostgreSQL password
# #     DATABASE_NAME: str = 'signature_extractor'  # Update with your database name
# #     DATABASE_USERNAME: str = 'pranay'  # Update with your PostgreSQL username
# #     SECRET_KEY: str = 'your_secret_key'  # Replace with a strong secret key
# #     ALGORITHM: str = 'HS256'
# #     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
# #     JWT_SECRET: str = 'your_jwt_secret'  # Replace with a strong JWT secret
# #     JWT_ALGORITHM: str = 'HS256'

# # settings = Settings()


# from pydantic_settings import BaseSettings
# from pydantic import Field, ValidationError

# class Settings(BaseSettings):
#     # Database settings
#     DATABASE_HOSTNAME: str = 'localhost'
#     DATABASE_PORT: str = '5432'
#     DATABASE_PASSWORD: str = 'pranay'
#     DATABASE_NAME: str = 'signature_extractor'
#     DATABASE_USERNAME: str = 'pranay'
    
#     # Constructed DATABASE_URL
#     @property
#     def DATABASE_URL(self) -> str:
#         return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
#     # JWT Settings
#     JWT_SECRET: str = Field("your-secret-key", env="JWT_SECRET")
#     JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
#     JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
#     # Optional: Razorpay settings (if you're using them)
#     RAZORPAY_KEY_ID: str | None = None
#     RAZORPAY_KEY_SECRET: str | None = None

#     class Config:
#         env_file = ".env"
#         case_sensitive = True

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Validate settings after initialization
#         self.validate_settings()

#     def validate_settings(self):
#         """Validate critical settings."""
#         if not self.JWT_SECRET or self.JWT_SECRET == "your-secret-key":
#             raise ValidationError("JWT_SECRET must be set to a secure value")
#         if not self.DATABASE_URL:
#             raise ValidationError("Database configuration is invalid")

# # Create settings instance
# try:
#     settings = Settings()
# except ValidationError as e:
#     print("Configuration validation error:", e)
#     raise

from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError
import logging
import os

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Database settings
    DATABASE_HOSTNAME: str = 'localhost'
    DATABASE_PORT: str = '5432'
    DATABASE_PASSWORD: str = 'pranay'
    DATABASE_NAME: str = 'signature_extractor'
    DATABASE_USERNAME: str = 'pranay'
    
    # Constructed DATABASE_URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    # JWT Settings
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Settings initialized successfully")
        logger.debug(f"Database URL: {self.DATABASE_URL}")
        logger.debug(f"JWT Algorithm: {self.JWT_ALGORITHM}")
        logger.debug(f"JWT Expiry: {self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes")

# Create settings instance with error handling
try:
    settings = Settings()
except ValidationError as e:
    logger.error(f"Settings validation error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error loading settings: {e}")
    raise