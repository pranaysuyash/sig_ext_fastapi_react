# # # # # # # backend/app/utils.py
# # # # # # import logging
# # # # # # from datetime import datetime, timedelta
# # # # # # from typing import Optional
# # # # # # from jose import JWTError, jwt
# # # # # # from app.config import settings
# # # # # # from fastapi import Depends, HTTPException, status
# # # # # # from fastapi.security import OAuth2PasswordBearer
# # # # # # from sqlalchemy.orm import Session
# # # # # # from app.database import get_db
# # # # # # from app.models.user import User
# # # # # # from passlib.context import CryptContext

# # # # # # # Initialize logger
# # # # # # logger = logging.getLogger(__name__)

# # # # # # # OAuth2 scheme setup
# # # # # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # # # # # Password hashing context
# # # # # # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # # # # # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# # # # # #     to_encode = data.copy()
# # # # # #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
# # # # # #     to_encode.update({"exp": expire})
# # # # # #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
# # # # # #     return encoded_jwt

# # # # # # # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# # # # # # #     credentials_exception = HTTPException(
# # # # # # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # #         detail="Could not validate credentials",
# # # # # # #         headers={"WWW-Authenticate": "Bearer"},
# # # # # # #     )
# # # # # # #     try:
# # # # # # #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# # # # # # #         user_id: str = payload.get("sub")
# # # # # # #         if user_id is None:
# # # # # # #             raise credentials_exception
# # # # # # #     except JWTError as e:
# # # # # # #         logger.error(f"JWT decoding error: {e}")
# # # # # # #         raise credentials_exception
# # # # # # #     user = db.query(User).filter(User.id == user_id).first()
# # # # # # #     if user is None:
# # # # # # #         raise credentials_exception
# # # # # # #     return user

# # # # # # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# # # # # #     logger.info(f"Token received for authentication: {token}")
# # # # # #     credentials_exception = HTTPException(
# # # # # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # #         detail="Could not validate credentials",
# # # # # #         headers={"WWW-Authenticate": "Bearer"},
# # # # # #     )
# # # # # #     try:
# # # # # #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# # # # # #         user_id: str = payload.get("sub")
# # # # # #         if user_id is None:
# # # # # #             raise credentials_exception
# # # # # #     except JWTError as e:
# # # # # #         logger.error(f"JWT decoding error: {e}")
# # # # # #         raise credentials_exception
# # # # # #     user = db.query(User).filter(User.id == user_id).first()
# # # # # #     if user is None:
# # # # # #         raise credentials_exception
# # # # # #     return user


# # # # # # def get_password_hash(password):
# # # # # #     return pwd_context.hash(password)

# # # # # # def verify_password(plain_password, hashed_password):
# # # # # #     return pwd_context.verify(plain_password, hashed_password)



# # # # # # backend/app/utils.py
# # # # # import logging
# # # # # from datetime import datetime, timedelta
# # # # # from typing import Optional
# # # # # from jose import JWTError, jwt
# # # # # from app.config import settings
# # # # # from fastapi import Depends, HTTPException, status
# # # # # from fastapi.security import OAuth2PasswordBearer
# # # # # from sqlalchemy.orm import Session
# # # # # from app.database import get_db
# # # # # from app.models.user import User
# # # # # from passlib.context import CryptContext

# # # # # # Initialize logger
# # # # # logger = logging.getLogger(__name__)

# # # # # # OAuth2 scheme setup
# # # # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # # # # Password hashing context
# # # # # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # # # # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# # # # #     to_encode = data.copy()
# # # # #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
# # # # #     to_encode.update({"exp": expire})
# # # # #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
# # # # #     logger.info(f"Token created for user: {data.get('sub')}")
# # # # #     return encoded_jwt

# # # # # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# # # # #     logger.info(f"Token received for authentication: {token}")
# # # # #     credentials_exception = HTTPException(
# # # # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # # # #         detail="Could not validate credentials",
# # # # #         headers={"WWW-Authenticate": "Bearer"},
# # # # #     )
# # # # #     try:
# # # # #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# # # # #         user_id: str = payload.get("sub")
# # # # #         exp_time: int = payload.get("exp")
# # # # #         logger.info(f"Decoded token payload: {payload}")
# # # # #         if user_id is None or exp_time < int(datetime.utcnow().timestamp()):
# # # # #             logger.error("Token is either missing user_id or is expired.")
# # # # #             raise credentials_exception
# # # # #     except JWTError as e:
# # # # #         logger.error(f"JWT decoding error: {e}")
# # # # #         raise credentials_exception
# # # # #     user = db.query(User).filter(User.id == user_id).first()
# # # # #     if user is None:
# # # # #         logger.error("User not found for the given token.")
# # # # #         raise credentials_exception
# # # # #     return user


# # # # # def get_password_hash(password):
# # # # #     return pwd_context.hash(password)

# # # # # def verify_password(plain_password, hashed_password):
# # # # #     return pwd_context.verify(plain_password, hashed_password)

# # # # # backend/app/utils.py
# # # # import logging
# # # # from datetime import datetime, timedelta
# # # # from typing import Optional
# # # # from jose import JWTError, jwt
# # # # from app.config import settings
# # # # from fastapi import Depends, HTTPException, status
# # # # from fastapi.security import OAuth2PasswordBearer
# # # # from sqlalchemy.orm import Session
# # # # from app.database import get_db
# # # # from app.models.user import User
# # # # from passlib.context import CryptContext

# # # # # Initialize logger
# # # # logger = logging.getLogger(__name__)

# # # # # OAuth2 scheme setup
# # # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # # # Password hashing context
# # # # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # # # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# # # #     to_encode = data.copy()
# # # #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
# # # #     to_encode.update({"exp": expire})
# # # #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
# # # #     logger.info(f"Token created for user: {data.get('sub')}")
# # # #     return encoded_jwt

# # # # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# # # #     logger.info(f"Token received for authentication: {token}")
# # # #     credentials_exception = HTTPException(
# # # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # # #         detail="Could not validate credentials",
# # # #         headers={"WWW-Authenticate": "Bearer"},
# # # #     )
# # # #     try:
# # # #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# # # #         user_id: str = payload.get("sub")
# # # #         exp_time: int = payload.get("exp")
# # # #         logger.info(f"Decoded token payload: {payload}")
# # # #         if user_id is None or exp_time < int(datetime.utcnow().timestamp()):
# # # #             logger.error("Token is either missing user_id or is expired.")
# # # #             raise credentials_exception
# # # #     except JWTError as e:
# # # #         logger.error(f"JWT decoding error: {e}")
# # # #         raise credentials_exception
# # # #     user = db.query(User).filter(User.id == user_id).first()
# # # #     if user is None:
# # # #         logger.error("User not found for the given token.")
# # # #         raise credentials_exception
# # # #     return user

# # # # def get_password_hash(password):
# # # #     return pwd_context.hash(password)

# # # # def verify_password(plain_password, hashed_password):
# # # #     return pwd_context.verify(plain_password, hashed_password)


# # # # backend/app/utils.py
# # # import logging
# # # from datetime import datetime, timedelta
# # # from typing import Optional
# # # from jose import JWTError, jwt
# # # from app.config import settings
# # # from fastapi import Depends, HTTPException, status
# # # from fastapi.security import OAuth2PasswordBearer
# # # from sqlalchemy.orm import Session
# # # from app.database import get_db
# # # from app.models.user import User
# # # from passlib.context import CryptContext

# # # # Initialize logger
# # # logger = logging.getLogger(__name__)

# # # # OAuth2 scheme setup
# # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # # Password hashing context
# # # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# # #     to_encode = data.copy()
# # #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
# # #     to_encode.update({"exp": expire})
# # #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
# # #     logger.info(f"Token created for user: {data.get('sub')}")
# # #     return encoded_jwt

# # # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# # #     logger.info(f"Token received for authentication: {token}")
# # #     credentials_exception = HTTPException(
# # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # #         detail="Could not validate credentials",
# # #         headers={"WWW-Authenticate": "Bearer"},
# # #     )
# # #     try:
# # #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# # #         user_id: str = payload.get("sub")
# # #         exp_time: int = payload.get("exp")
# # #         logger.info(f"Decoded token payload: {payload}")
# # #         if user_id is None or exp_time < int(datetime.utcnow().timestamp()):
# # #             logger.error("Token is either missing user_id or is expired.")
# # #             raise credentials_exception
# # #     except JWTError as e:
# # #         logger.error(f"JWT decoding error: {e}")
# # #         raise credentials_exception
# # #     user = db.query(User).filter(User.id == user_id).first()
# # #     if user is None:
# # #         logger.error("User not found for the given token.")
# # #         raise credentials_exception
# # #     return user

# # # def get_password_hash(password):
# # #     return pwd_context.hash(password)

# # # def verify_password(plain_password, hashed_password):
# # #     return pwd_context.verify(plain_password, hashed_password)

# # import cv2
# # import numpy as np
# # from PIL import Image
# # import logging
# # from datetime import datetime, timedelta
# # from typing import Optional
# # from jose import JWTError, jwt
# # from app.config import settings
# # from fastapi import Depends, HTTPException, status
# # from fastapi.security import OAuth2PasswordBearer
# # from sqlalchemy.orm import Session
# # from app.database import get_db
# # from app.models.user import User
# # from passlib.context import CryptContext

# # # Initialize logger
# # logger = logging.getLogger(__name__)

# # # OAuth2 scheme setup
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # Password hashing context
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# #     to_encode = data.copy()
# #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
# #     to_encode.update({"exp": expire})
# #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
# #     logger.info(f"Token created for user: {data.get('sub')}")
# #     return encoded_jwt

# # def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# #     logger.info(f"Token received for authentication: {token}")
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# #         user_id: str = payload.get("sub")
# #         exp_time: int = payload.get("exp")
# #         logger.info(f"Decoded token payload: {payload}")
# #         if user_id is None or exp_time < int(datetime.utcnow().timestamp()):
# #             logger.error("Token is either missing user_id or is expired.")
# #             raise credentials_exception
# #     except JWTError as e:
# #         logger.error(f"JWT decoding error: {e}")
# #         raise credentials_exception
# #     user = db.query(User).filter(User.id == user_id).first()
# #     if user is None:
# #         logger.error("User not found for the given token.")
# #         raise credentials_exception
# #     return user

# # def get_password_hash(password):
# #     return pwd_context.hash(password)

# # def verify_password(plain_password, hashed_password):
# #     return pwd_context.verify(plain_password, hashed_password)

# # def save_image(file, temp_dir):
# #     file_path = temp_dir / file.filename
# #     with open(file_path, "wb") as buffer:
# #         buffer.write(file.file.read())
    
# #     # Convert transparent areas to white if the image is RGBA
# #     img = Image.open(file_path)
# #     if img.mode == 'RGBA':
# #         background = Image.new("RGB", img.size, (255, 255, 255))
# #         background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
# #         background.save(file_path)
    
# #     return file_path

# # def process_signature(sig, color, threshold):
# #     sig_gray = cv2.cvtColor(sig, cv2.COLOR_BGR2GRAY)
# #     ret, alpha_mask = cv2.threshold(sig_gray, threshold, 255, cv2.THRESH_BINARY_INV)
# #     color_bgr = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
# #     color_mask = np.zeros_like(sig, dtype=np.uint8)
# #     for i in range(3):
# #         color_mask[:, :, i] = color_bgr[i]

# #     sig_color = cv2.addWeighted(sig, 1, color_mask, 0.5, 0)
# #     b, g, r = cv2.split(sig_color[..., :3])
# #     new = [b, g, r, alpha_mask]
    
# #     png = cv2.merge(new)
# #     return png


# import cv2
# import numpy as np
# from PIL import Image
# import logging
# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from app.config import settings
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.user import User
# from passlib.context import CryptContext

# # Initialize logger
# logger = logging.getLogger(__name__)

# # OAuth2 scheme setup
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Authentication Functions
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     """
#     Create a JWT access token.
#     """
#     try:
#         to_encode = data.copy()
#         expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#         logger.info(f"Token created for user: {data.get('sub')}")
#         return encoded_jwt
#     except Exception as e:
#         logger.error(f"Error creating access token: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Could not create access token"
#         )

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Validate JWT token and return current user.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#         user_id: str = payload.get("sub")
#         exp_time: int = payload.get("exp")
        
#         if user_id is None:
#             logger.error("Token missing user_id")
#             raise credentials_exception
            
#         if exp_time < int(datetime.utcnow().timestamp()):
#             logger.error("Token has expired")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token has expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
            
#     except JWTError as e:
#         logger.error(f"JWT decoding error: {e}")
#         raise credentials_exception
        
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         logger.error("User not found for the given token")
#         raise credentials_exception
        
#     return user

# def get_password_hash(password: str) -> str:
#     """
#     Hash a password using bcrypt.
#     """
#     try:
#         return pwd_context.hash(password)
#     except Exception as e:
#         logger.error(f"Error hashing password: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error processing password"
#         )

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify a password against a hash.
#     """
#     try:
#         return pwd_context.verify(plain_password, hashed_password)
#     except Exception as e:
#         logger.error(f"Error verifying password: {e}")
#         return False

# # Image Processing Functions
# def save_image(file, temp_dir) -> str:
#     """
#     Save an uploaded image and convert transparent areas to white if RGBA.
#     """
#     try:
#         file_path = temp_dir / file.filename
#         with open(file_path, "wb") as buffer:
#             buffer.write(file.file.read())
        
#         # Convert transparent areas to white if the image is RGBA
#         img = Image.open(file_path)
#         if img.mode == 'RGBA':
#             background = Image.new("RGB", img.size, (255, 255, 255))
#             background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
#             background.save(file_path)
        
#         logger.info(f"Image saved successfully at {file_path}")
#         return file_path
#     except Exception as e:
#         logger.error(f"Error saving image: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error saving image"
#         )

# def process_signature(sig, color: str, threshold: int) -> np.ndarray:
#     """
#     Process a signature image with color and threshold.
#     """
#     try:
#         # Convert to grayscale and create alpha mask
#         sig_gray = cv2.cvtColor(sig, cv2.COLOR_BGR2GRAY)
#         ret, alpha_mask = cv2.threshold(sig_gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
#         # Convert hex color to BGR
#         color_bgr = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
        
#         # Create color mask
#         color_mask = np.zeros_like(sig, dtype=np.uint8)
#         for i in range(3):
#             color_mask[:, :, i] = color_bgr[i]

#         # Apply color
#         sig_color = cv2.addWeighted(sig, 1, color_mask, 0.5, 0)
        
#         # Create PNG with alpha channel
#         b, g, r = cv2.split(sig_color[..., :3])
#         png = cv2.merge([b, g, r, alpha_mask])
        
#         logger.info("Signature processed successfully")
#         return png
#     except Exception as e:
#         logger.error(f"Error processing signature: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error processing signature"
#         )

import cv2
import numpy as np
from PIL import Image
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from passlib.context import CryptContext
from app.config import settings

# Initialize logger
logger = logging.getLogger(__name__)

# OAuth2 scheme setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        logger.debug(f"Created token for user ID: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        # Check token expiration
        exp = payload.get("exp")
        if exp is None or exp < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
        
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User not found for ID: {user_id}")
        raise credentials_exception
        
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password"
        )

def save_image(file, temp_dir) -> str:
    """Save an uploaded image and convert transparent areas to white if RGBA."""
    try:
        file_path = temp_dir / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Convert transparent areas to white if the image is RGBA
        img = Image.open(file_path)
        if img.mode == 'RGBA':
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            background.save(file_path)
        
        logger.info(f"Image saved successfully at {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving image"
        )

def process_signature(sig, color: str, threshold: int) -> np.ndarray:
    """Process a signature image with color and threshold."""
    try:
        # Convert to grayscale and create alpha mask
        sig_gray = cv2.cvtColor(sig, cv2.COLOR_BGR2GRAY)
        ret, alpha_mask = cv2.threshold(sig_gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
        # Convert hex color to BGR
        color_bgr = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
        
        # Create color mask
        color_mask = np.zeros_like(sig, dtype=np.uint8)
        for i in range(3):
            color_mask[:, :, i] = color_bgr[i]

        # Apply color
        sig_color = cv2.addWeighted(sig, 1, color_mask, 0.5, 0)
        
        # Create PNG with alpha channel
        b, g, r = cv2.split(sig_color[..., :3])
        png = cv2.merge([b, g, r, alpha_mask])
        
        logger.info("Signature processed successfully")
        return png
    except Exception as e:
        logger.error(f"Error processing signature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing signature"
        )