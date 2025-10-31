# # # # # # # # # # # # # backend/app/routers/auth.py
# # # # # # # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # # # # # # from sqlalchemy.orm import Session
# # # # # # # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import these schemas
# # # # # # # # # # # # from app.schemas.token import Token
# # # # # # # # # # # # from app.schemas.auth import LoginRequest  # Ensure this import is correct
# # # # # # # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # # # # # # from app.database import get_db
# # # # # # # # # # # # from app.utils import create_access_token
# # # # # # # # # # # # from datetime import timedelta
# # # # # # # # # # # # from app.config import settings

# # # # # # # # # # # # router = APIRouter(
# # # # # # # # # # # #     prefix="/auth",
# # # # # # # # # # # #     tags=["Authentication"]
# # # # # # # # # # # # )

# # # # # # # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # # # # # # #     db_user = create_user(db, user)
# # # # # # # # # # # #     if not db_user:
# # # # # # # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # # # # # # #     return db_user

# # # # # # # # # # # # @router.post("/login", response_model=Token)
# # # # # # # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # # # # # # #     if not user:
# # # # # # # # # # # #         raise HTTPException(
# # # # # # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # # # # # #             detail="Invalid credentials",
# # # # # # # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # # # # # # #         )
# # # # # # # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # # # # # # #     access_token = create_access_token(
# # # # # # # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # # # # # # #     )
# # # # # # # # # # # #     return {"access_token": access_token, "token_type": "bearer"}


# # # # # # # # # # # # backend/app/routers/auth.py
# # # # # # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # # # # # from sqlalchemy.orm import Session
# # # # # # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # # # # # # from app.schemas.token import Token
# # # # # # # # # # # from app.schemas.auth import LoginRequest
# # # # # # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # # # # # from app.database import get_db
# # # # # # # # # # # from app.utils import create_access_token
# # # # # # # # # # # from datetime import timedelta
# # # # # # # # # # # from app.config import settings

# # # # # # # # # # # router = APIRouter(
# # # # # # # # # # #     prefix="/auth",
# # # # # # # # # # #     tags=["Authentication"]
# # # # # # # # # # # )

# # # # # # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # # # # # #     db_user = create_user(db, user)
# # # # # # # # # # #     if not db_user:
# # # # # # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # # # # # #     return db_user

# # # # # # # # # # # @router.post("/login", response_model=Token)
# # # # # # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # # # # # #     if not user:
# # # # # # # # # # #         raise HTTPException(
# # # # # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # # # # #             detail="Invalid credentials",
# # # # # # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # # # # # #         )
# # # # # # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # # # # # #     access_token = create_access_token(
# # # # # # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # # # # # #     )
# # # # # # # # # # #     return {"access_token": access_token, "token_type": "bearer"}


# # # # # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # # # # from sqlalchemy.orm import Session
# # # # # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # # # # # from app.schemas.token import Token
# # # # # # # # # # from app.schemas.auth import LoginRequest
# # # # # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # # # # from app.database import get_db
# # # # # # # # # # from app.utils import create_access_token
# # # # # # # # # # from datetime import timedelta
# # # # # # # # # # from app.config import settings

# # # # # # # # # # router = APIRouter(
# # # # # # # # # #     prefix="/auth",
# # # # # # # # # #     tags=["Authentication"]
# # # # # # # # # # )

# # # # # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # # # # #     db_user = create_user(db, user)
# # # # # # # # # #     if not db_user:
# # # # # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # # # # #     return db_user

# # # # # # # # # # @router.post("/login", response_model=Token)
# # # # # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # # # # #     if not user:
# # # # # # # # # #         raise HTTPException(
# # # # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # # # #             detail="Invalid credentials",
# # # # # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # # # # #         )
# # # # # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # # # # #     access_token = create_access_token(
# # # # # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # # # # #     )
# # # # # # # # # #     return {"access_token": access_token, "token_type": "bearer"}

# # # # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # # # from sqlalchemy.orm import Session
# # # # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # # # # from app.schemas.token import Token
# # # # # # # # # from app.schemas.auth import LoginRequest
# # # # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # # # from app.database import get_db
# # # # # # # # # from app.utils import create_access_token
# # # # # # # # # from datetime import timedelta
# # # # # # # # # from app.config import settings

# # # # # # # # # router = APIRouter(
# # # # # # # # #     prefix="/auth",
# # # # # # # # #     tags=["Authentication"]
# # # # # # # # # )

# # # # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # # # #     db_user = create_user(db, user)
# # # # # # # # #     if not db_user:
# # # # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # # # #     return db_user

# # # # # # # # # @router.post("/login", response_model=Token)
# # # # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # # # #     if not user:
# # # # # # # # #         raise HTTPException(
# # # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # # #             detail="Invalid credentials",
# # # # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # # # #         )
# # # # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # # # #     access_token = create_access_token(
# # # # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # # # #     )
# # # # # # # # #     return {"access_token": access_token, "token_type": "bearer"}


# # # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # # from sqlalchemy.orm import Session
# # # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # # # from app.schemas.token import Token
# # # # # # # # from app.schemas.auth import LoginRequest
# # # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # # from app.database import get_db
# # # # # # # # from app.utils import create_access_token
# # # # # # # # from datetime import timedelta
# # # # # # # # from app.config import settings

# # # # # # # # router = APIRouter(
# # # # # # # #     prefix="/auth",
# # # # # # # #     tags=["Authentication"]
# # # # # # # # )

# # # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # # #     db_user = create_user(db, user)
# # # # # # # #     if not db_user:
# # # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # # #     return db_user

# # # # # # # # @router.post("/login", response_model=Token)
# # # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # # #     if not user:
# # # # # # # #         raise HTTPException(
# # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # #             detail="Invalid credentials",
# # # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # # #         )
# # # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # # #     access_token = create_access_token(
# # # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # # #     )
# # # # # # # #     return {"access_token": access_token, "token_type": "bearer"}


# # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # from sqlalchemy.orm import Session
# # # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # # from app.schemas.token import Token
# # # # # # # from app.schemas.auth import LoginRequest
# # # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # # from app.database import get_db
# # # # # # # from app.utils import create_access_token
# # # # # # # from datetime import timedelta
# # # # # # # from app.config import settings

# # # # # # # router = APIRouter(
# # # # # # #     prefix="/auth",
# # # # # # #     tags=["Authentication"]
# # # # # # # )

# # # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # # #     db_user = create_user(db, user)
# # # # # # #     if not db_user:
# # # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # # #     return db_user

# # # # # # # @router.post("/login", response_model=Token)
# # # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # # #     if not user:
# # # # # # #         raise HTTPException(
# # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # #             detail="Invalid credentials",
# # # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # # #         )
# # # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # # #     access_token = create_access_token(
# # # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # # #     )
# # # # # # #     return {"access_token": access_token, "token_type": "bearer"}


# # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # from sqlalchemy.orm import Session
# # # # # # from app.schemas.user import UserCreate, UserResponse  # Import schemas for user creation
# # # # # # from app.schemas.token import Token
# # # # # # from app.schemas.auth import LoginRequest
# # # # # # from app.crud.user import authenticate_user, create_user
# # # # # # from app.database import get_db
# # # # # # from app.utils import create_access_token
# # # # # # from datetime import timedelta
# # # # # # from app.config import settings

# # # # # # router = APIRouter(
# # # # # #     prefix="/auth",
# # # # # #     tags=["Authentication"]
# # # # # # )

# # # # # # @router.post("/register", response_model=UserResponse)
# # # # # # def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # # #     db_user = create_user(db, user)
# # # # # #     if not db_user:
# # # # # #         raise HTTPException(status_code=400, detail="Email already registered")
# # # # # #     return db_user

# # # # # # @router.post("/login", response_model=Token)
# # # # # # def login(form_data: LoginRequest, db: Session = Depends(get_db)):
# # # # # #     user = authenticate_user(db, form_data.email, form_data.password)
# # # # # #     if not user:
# # # # # #         raise HTTPException(
# # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # #             detail="Invalid credentials",
# # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # #         )
# # # # # #     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # #     access_token = create_access_token(
# # # # # #         data={"sub": str(user.id)}, expires_delta=access_token_expires
# # # # # #     )
# # # # # #     return {"access_token": access_token, "token_type": "bearer"}

# # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # from fastapi.security import OAuth2PasswordRequestForm
# # # # # from sqlalchemy.orm import Session
# # # # # from datetime import timedelta
# # # # # from app.database import get_db
# # # # # from app.schemas.user import UserCreate, UserResponse
# # # # # from app.schemas.token import Token
# # # # # from app.crud.user import authenticate_user, create_user
# # # # # from app.utils import create_access_token
# # # # # from app.config import settings
# # # # # import logging

# # # # # # Set up logging
# # # # # logger = logging.getLogger(__name__)

# # # # # router = APIRouter(
# # # # #     prefix="/auth",
# # # # #     tags=["Authentication"]
# # # # # )

# # # # # @router.post("/register", response_model=UserResponse)
# # # # # async def register(user: UserCreate, db: Session = Depends(get_db)):
# # # # #     try:
# # # # #         db_user = create_user(db, user)
# # # # #         return db_user
# # # # #     except HTTPException as he:
# # # # #         raise he
# # # # #     except Exception as e:
# # # # #         logger.error(f"Registration error: {str(e)}")
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #             detail="Internal server error during registration"
# # # # #         )

# # # # # @router.post("/login", response_model=Token)
# # # # # async def login(
# # # # #     form_data: OAuth2PasswordRequestForm = Depends(),
# # # # #     db: Session = Depends(get_db)
# # # # # ):
# # # # #     try:
# # # # #         user = authenticate_user(db, form_data.username, form_data.password)
# # # # #         if not user:
# # # # #             raise HTTPException(
# # # # #                 status_code=status.HTTP_401_UNAUTHORIZED,
# # # # #                 detail="Incorrect email or password",
# # # # #                 headers={"WWW-Authenticate": "Bearer"},
# # # # #             )
        
# # # # #         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # #         access_token = create_access_token(
# # # # #             data={"sub": str(user.id)},
# # # # #             expires_delta=access_token_expires
# # # # #         )
        
# # # # #         return {
# # # # #             "access_token": access_token,
# # # # #             "token_type": "bearer"
# # # # #         }
# # # # #     except HTTPException as he:
# # # # #         raise he
# # # # #     except Exception as e:
# # # # #         logger.error(f"Login error: {str(e)}")
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #             detail="Internal server error during login"
# # # # #         )


# # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # from fastapi.security import OAuth2PasswordRequestForm
# # # # from sqlalchemy.orm import Session
# # # # from datetime import timedelta
# # # # from app.database import get_db
# # # # from app.schemas.user import UserCreate, UserResponse
# # # # from app.schemas.token import Token
# # # # from app.crud.user import authenticate_user, create_user
# # # # from app.utils import create_access_token
# # # # from app.config import settings
# # # # import logging

# # # # logger = logging.getLogger(__name__)

# # # # router = APIRouter(
# # # #     prefix="/auth",
# # # #     tags=["Authentication"]
# # # # )

# # # # @router.post("/login", response_model=Token)
# # # # async def login(
# # # #     form_data: OAuth2PasswordRequestForm = Depends(),
# # # #     db: Session = Depends(get_db)
# # # # ):
# # # #     try:
# # # #         # Log incoming request data (excluding password)
# # # #         logger.info(f"Login attempt for user: {form_data.username}")
        
# # # #         user = authenticate_user(db, form_data.username, form_data.password)
# # # #         if not user:
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_401_UNAUTHORIZED,
# # # #                 detail="Incorrect email or password",
# # # #                 headers={"WWW-Authenticate": "Bearer"},
# # # #             )
            
# # # #         access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # # #         access_token = create_access_token(
# # # #             data={"sub": str(user.id)},
# # # #             expires_delta=access_token_expires
# # # #         )
        
# # # #         return {
# # # #             "access_token": access_token,
# # # #             "token_type": "bearer"
# # # #         }
# # # #     except HTTPException:
# # # #         raise
# # # #     except Exception as e:
# # # #         logger.error(f"Login error: {str(e)}")
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #             detail="Internal server error during login"
# # # #         )

# # # # @router.post("/register", response_model=UserResponse)
# # # # async def register(user: UserCreate, db: Session = Depends(get_db)):
# # # #     try:
# # # #         # Log registration attempt (excluding password)
# # # #         logger.info(f"Registration attempt for email: {user.email}")
        
# # # #         db_user = create_user(db, user)
# # # #         return db_user
# # # #     except HTTPException as he:
# # # #         raise he
# # # #     except Exception as e:
# # # #         logger.error(f"Registration error: {str(e)}")
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #             detail="Internal server error during registration"
# # # #         )


# # # from fastapi import APIRouter, Depends, HTTPException, status
# # # from fastapi.security import OAuth2PasswordRequestForm
# # # from sqlalchemy.orm import Session
# # # from datetime import timedelta
# # # from app.database import get_db
# # # from app.schemas.user import UserCreate, UserResponse
# # # from app.schemas.token import Token
# # # from app.crud.user import authenticate_user, create_user
# # # from app.utils import create_access_token
# # # from app.config import settings
# # # import logging

# # # logger = logging.getLogger(__name__)

# # # router = APIRouter(
# # #     prefix="/auth",
# # #     tags=["Authentication"]
# # # )

# # # @router.post("/login", response_model=Token)
# # # async def login(
# # #     form_data: OAuth2PasswordRequestForm = Depends(),
# # #     db: Session = Depends(get_db)
# # # ):
# # #     try:
# # #         # Log incoming request data (excluding password)
# # #         logger.info(f"Login attempt for user: {form_data.username}")
        
# # #         user = authenticate_user(db, form_data.username, form_data.password)
# # #         if not user:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_401_UNAUTHORIZED,
# # #                 detail="Incorrect email or password",
# # #                 headers={"WWW-Authenticate": "Bearer"},
# # #             )
            
# # #         access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# # #         access_token = create_access_token(
# # #             data={"sub": str(user.id)},
# # #             expires_delta=access_token_expires
# # #         )
        
# # #         return {
# # #             "access_token": access_token,
# # #             "token_type": "bearer"
# # #         }
# # #     except HTTPException:
# # #         raise
# # #     except Exception as e:
# # #         logger.error(f"Login error: {str(e)}")
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=str(e)
# # #         )

# # # @router.post("/register", response_model=UserResponse)
# # # async def register(
# # #     user: UserCreate,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     try:
# # #         # Log registration attempt (excluding password)
# # #         logger.info(f"Registration attempt for email: {user.email}")
        
# # #         db_user = create_user(db, user)
# # #         return db_user
# # #     except HTTPException:
# # #         raise
# # #     except Exception as e:
# # #         logger.error(f"Registration error: {str(e)}")
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=str(e)
# # #         )

# # from fastapi import APIRouter, Depends, HTTPException, status
# # from fastapi.security import OAuth2PasswordRequestForm
# # from sqlalchemy.orm import Session
# # from datetime import timedelta
# # import logging

# # from app.database import get_db
# # from app.schemas.user import UserCreate, UserResponse
# # from app.schemas.token import Token
# # from app.crud.user import authenticate_user, create_user
# # from app.utils import create_access_token
# # from app.config import settings

# # logger = logging.getLogger(__name__)
# # router = APIRouter(prefix="/auth", tags=["Authentication"])

# # @router.post("/register", response_model=UserResponse)
# # async def register(user: UserCreate, db: Session = Depends(get_db)):
# #     """Register a new user."""
# #     try:
# #         logger.info(f"Registration attempt for email: {user.email}")
# #         db_user = create_user(db, user)
# #         return db_user
# #     except HTTPException as he:
# #         raise he
# #     except Exception as e:
# #         logger.error(f"Registration error: {str(e)}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=str(e)
# #         )

# # @router.post("/login", response_model=Token)
# # async def login(
# #     form_data: OAuth2PasswordRequestForm = Depends(),
# #     db: Session = Depends(get_db)
# # ):
# #     """Login and return access token."""
# #     try:
# #         logger.info(f"Login attempt for user: {form_data.username}")
# #         user = authenticate_user(db, form_data.username, form_data.password)
        
# #         if not user:
# #             logger.warning(f"Failed login attempt for user: {form_data.username}")
# #             raise HTTPException(
# #                 status_code=status.HTTP_401_UNAUTHORIZED,
# #                 detail="Incorrect email or password",
# #                 headers={"WWW-Authenticate": "Bearer"},
# #             )
        
# #         # Create access token
# #         access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
# #         access_token = create_access_token(
# #             data={"sub": str(user.id), "username": user.email},
# #             expires_delta=access_token_expires
# #         )
        
# #         logger.info(f"Successful login for user: {user.email}")
# #         return {
# #             "access_token": access_token,
# #             "token_type": "bearer"
# #         }
        
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         logger.error(f"Login error: {str(e)}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail="Internal server error during login"
# #         )


# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from datetime import timedelta
# import logging
# import traceback

# from app.database import get_db
# from app.schemas.user import UserCreate, UserResponse
# from app.schemas.token import Token
# from app.crud.user import authenticate_user, create_user
# from app.utils import create_access_token
# from app.config import settings

# logger = logging.getLogger(__name__)
# router = APIRouter(prefix="/auth", tags=["Authentication"])

# @router.post("/login", response_model=Token)
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """Login and return access token."""
#     try:
#         logger.info(f"Login attempt with username: {form_data.username}")
#         logger.debug(f"Form data received: {form_data.__dict__}")
        
#         # Try to authenticate user
#         user = authenticate_user(db, form_data.username, form_data.password)
#         logger.debug(f"Authentication result: {user is not None}")
        
#         if not user:
#             logger.warning(f"Failed login attempt for user: {form_data.username}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect email or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         # Create access token
#         try:
#             access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#             logger.debug(f"Creating token with expiry: {access_token_expires}")
            
#             access_token = create_access_token(
#                 data={"sub": str(user.id)},
#                 expires_delta=access_token_expires
#             )
#             logger.info(f"Successfully created token for user: {user.email}")
            
#             return {
#                 "access_token": access_token,
#                 "token_type": "bearer"
#             }
#         except Exception as token_error:
#             logger.error(f"Token creation error: {str(token_error)}")
#             logger.error(traceback.format_exc())
#             raise
            
#     except HTTPException as he:
#         logger.warning(f"HTTP exception during login: {str(he)}")
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error during login: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )

# @router.post("/register", response_model=UserResponse)
# async def register(user: UserCreate, db: Session = Depends(get_db)):
#     """Register a new user."""
#     try:
#         logger.info(f"Registration attempt for email: {user.email}")
#         db_user = create_user(db, user)
#         return db_user
#     except HTTPException as he:
#         logger.warning(f"HTTP exception during registration: {str(he)}")
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error during registration: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.schemas.token import Token
from backend.app.crud.user import authenticate_user, create_user
from backend.app.database import get_db
from backend.app.utils import create_access_token
from datetime import timedelta
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
    except HTTPException:
        # Propagate explicit HTTP errors (e.g. unique constraint failures surfaced by crud layer)
        raise
    except Exception as exc:
        logger.error("Registration error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration",
        ) from exc

    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        logger.info(f"User {user.email} successfully logged in")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Preserve intentional HTTP responses (401, etc.)
        raise
    except Exception as exc:
        logger.error("Login error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login",
        ) from exc
