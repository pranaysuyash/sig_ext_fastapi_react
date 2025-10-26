# # # # # # # # backend/app/crud/user.py
# # # # # # # from sqlalchemy.orm import Session
# # # # # # # from app.schemas.user import UserCreate
# # # # # # # from app.models.user import User
# # # # # # # from app.utils import get_password_hash, verify_password
# # # # # # # import uuid

# # # # # # # def create_user(db: Session, user: UserCreate):
# # # # # # #     hashed_password = get_password_hash(user.password)
# # # # # # #     db_user = User(email=user.email, hashed_password=hashed_password)
# # # # # # #     db.add(db_user)
# # # # # # #     try:
# # # # # # #         db.commit()
# # # # # # #         db.refresh(db_user)
# # # # # # #         return db_user
# # # # # # #     except:
# # # # # # #         db.rollback()
# # # # # # #         return None

# # # # # # # def authenticate_user(db: Session, email: str, password: str):
# # # # # # #     user = db.query(User).filter(User.email == email).first()
# # # # # # #     if not user or not verify_password(password, user.hashed_password):
# # # # # # #         return False
# # # # # # #     return user


# # # # # # from sqlalchemy.orm import Session
# # # # # # from app.schemas.user import UserCreate
# # # # # # from app.models.user import User
# # # # # # from app.utils import get_password_hash, verify_password
# # # # # # import uuid

# # # # # # def create_user(db: Session, user: UserCreate):
# # # # # #     hashed_password = get_password_hash(user.password)
# # # # # #     db_user = User(email=user.email, hashed_password=hashed_password)
# # # # # #     db.add(db_user)
# # # # # #     try:
# # # # # #         db.commit()
# # # # # #         db.refresh(db_user)
# # # # # #         return db_user
# # # # # #     except:
# # # # # #         db.rollback()
# # # # # #         return None

# # # # # # def authenticate_user(db: Session, email: str, password: str):
# # # # # #     user = db.query(User).filter(User.email == email).first()
# # # # # #     if not user or not verify_password(password, user.hashed_password):
# # # # # #         return False
# # # # # #     return user

# # # # # from sqlalchemy.orm import Session
# # # # # from app.schemas.user import UserCreate
# # # # # from app.models.user import User
# # # # # from app.utils import get_password_hash, verify_password
# # # # # import uuid

# # # # # def create_user(db: Session, user: UserCreate):
# # # # #     hashed_password = get_password_hash(user.password)
# # # # #     db_user = User(email=user.email, hashed_password=hashed_password)
# # # # #     db.add(db_user)
# # # # #     try:
# # # # #         db.commit()
# # # # #         db.refresh(db_user)
# # # # #         return db_user
# # # # #     except:
# # # # #         db.rollback()
# # # # #         return None

# # # # # def authenticate_user(db: Session, email: str, password: str):
# # # # #     user = db.query(User).filter(User.email == email).first()
# # # # #     if not user or not verify_password(password, user.hashed_password):
# # # # #         return False
# # # # #     return user
# # # # from sqlalchemy.orm import Session
# # # # from app.schemas.user import UserCreate
# # # # from app.models.user import User
# # # # from app.utils import get_password_hash, verify_password
# # # # import uuid

# # # # def create_user(db: Session, user: UserCreate):
# # # #     hashed_password = get_password_hash(user.password)
# # # #     db_user = User(email=user.email, hashed_password=hashed_password)
# # # #     db.add(db_user)
# # # #     try:
# # # #         db.commit()
# # # #         db.refresh(db_user)
# # # #         return db_user
# # # #     except:
# # # #         db.rollback()
# # # #         return None

# # # # def authenticate_user(db: Session, email: str, password: str):
# # # #     user = db.query(User).filter(User.email == email).first()
# # # #     if not user or not verify_password(password, user.hashed_password):
# # # #         return False
# # # #     return user

# # # from sqlalchemy.orm import Session
# # # from fastapi import HTTPException, status
# # # from app.models.user import User, SubscriptionPlan
# # # from app.schemas.user import UserCreate
# # # from app.utils import get_password_hash, verify_password

# # # def get_user(db: Session, user_id: str):
# # #     return db.query(User).filter(User.id == user_id).first()

# # # def get_user_by_email(db: Session, email: str):
# # #     return db.query(User).filter(User.email == email).first()

# # # def create_user(db: Session, user: UserCreate):
# # #     # Check if user already exists
# # #     db_user = get_user_by_email(db, email=user.email)
# # #     if db_user:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Email already registered"
# # #         )
        
# # #     # Create new user
# # #     hashed_password = get_password_hash(user.password)
# # #     db_user = User(
# # #         email=user.email,
# # #         hashed_password=hashed_password,
# # #         subscription_plan=SubscriptionPlan.Free
# # #     )
    
# # #     try:
# # #         db.add(db_user)
# # #         db.commit()
# # #         db.refresh(db_user)
# # #         return db_user
# # #     except Exception as e:
# # #         db.rollback()
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=str(e)
# # #         )

# # # def authenticate_user(db: Session, email: str, password: str):
# # #     try:
# # #         user = get_user_by_email(db, email)
# # #         if not user:
# # #             return None
# # #         if not verify_password(password, user.hashed_password):
# # #             return None
# # #         return user
# # #     except Exception as e:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=f"Authentication error: {str(e)}"
# # #         )

# # # def update_user_subscription(db: Session, user_id: str, plan: SubscriptionPlan):
# # #     try:
# # #         user = get_user(db, user_id)
# # #         if not user:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_404_NOT_FOUND,
# # #                 detail="User not found"
# # #             )
        
# # #         user.subscription_plan = plan
# # #         db.commit()
# # #         db.refresh(user)
# # #         return user
# # #     except Exception as e:
# # #         db.rollback()
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=str(e)
# # #         )

# # from sqlalchemy.orm import Session
# # from fastapi import HTTPException, status
# # from app.models.user import User, SubscriptionPlan
# # from app.schemas.user import UserCreate
# # from app.utils import get_password_hash, verify_password
# # import logging

# # logger = logging.getLogger(__name__)

# # def get_user(db: Session, user_id: str):
# #     return db.query(User).filter(User.id == user_id).first()

# # def get_user_by_email(db: Session, email: str):
# #     return db.query(User).filter(User.email == email).first()

# # def create_user(db: Session, user: UserCreate):
# #     # Check if user already exists
# #     if get_user_by_email(db, email=user.email):
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="Email already registered"
# #         )
        
# #     # Create new user
# #     hashed_password = get_password_hash(user.password)
# #     db_user = User(
# #         email=user.email,
# #         hashed_password=hashed_password,
# #         subscription_plan=SubscriptionPlan.Free
# #     )
    
# #     try:
# #         db.add(db_user)
# #         db.commit()
# #         db.refresh(db_user)
# #         logger.info(f"Successfully created user with email: {user.email}")
# #         return db_user
# #     except Exception as e:
# #         db.rollback()
# #         logger.error(f"Error creating user: {str(e)}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=str(e)
# #         )

# # def authenticate_user(db: Session, email: str, password: str):
# #     try:
# #         user = get_user_by_email(db, email)
# #         if not user:
# #             logger.warning(f"Login attempt for non-existent user: {email}")
# #             return False
            
# #         if not verify_password(password, user.hashed_password):
# #             logger.warning(f"Failed password verification for user: {email}")
# #             return False
            
# #         logger.info(f"Successful authentication for user: {email}")
# #         return user
# #     except Exception as e:
# #         logger.error(f"Error during authentication: {str(e)}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail="Authentication error"
# #         )

# # def update_user_subscription(db: Session, user_id: str, plan: SubscriptionPlan):
# #     try:
# #         user = get_user(db, user_id)
# #         if not user:
# #             raise HTTPException(
# #                 status_code=status.HTTP_404_NOT_FOUND,
# #                 detail="User not found"
# #             )
        
# #         user.subscription_plan = plan
# #         db.commit()
# #         db.refresh(user)
# #         logger.info(f"Updated subscription plan for user {user.email} to {plan}")
# #         return user
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         db.rollback()
# #         logger.error(f"Error updating user subscription: {str(e)}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=str(e)
# #         )

# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from app.models.user import User, SubscriptionPlan
# from app.schemas.user import UserCreate
# from app.utils import get_password_hash, verify_password
# import logging
# import traceback

# logger = logging.getLogger(__name__)

# def get_user_by_email(db: Session, email: str):
#     try:
#         logger.debug(f"Attempting to find user with email: {email}")
#         user = db.query(User).filter(User.email == email).first()
#         logger.debug(f"User found: {user is not None}")
#         return user
#     except Exception as e:
#         logger.error(f"Database error while fetching user: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise

# def authenticate_user(db: Session, email: str, password: str):
#     try:
#         logger.debug(f"Starting authentication for email: {email}")
        
#         # Get user
#         user = get_user_by_email(db, email)
#         if not user:
#             logger.warning(f"No user found with email: {email}")
#             return False
            
#         logger.debug("User found, verifying password")
        
#         # Verify password
#         if not verify_password(password, user.hashed_password):
#             logger.warning(f"Invalid password for user: {email}")
#             return False
            
#         logger.info(f"Successfully authenticated user: {email}")
#         return user
        
#     except Exception as e:
#         logger.error(f"Error during authentication: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Authentication error: {str(e)}"
#         )

# def create_user(db: Session, user: UserCreate):
#     try:
#         # Check if user exists
#         existing_user = get_user_by_email(db, email=user.email)
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Email already registered"
#             )
            
#         # Hash password
#         logger.debug(f"Hashing password for new user: {user.email}")
#         hashed_password = get_password_hash(user.password)
        
#         # Create user
#         db_user = User(
#             email=user.email,
#             hashed_password=hashed_password,
#             subscription_plan=SubscriptionPlan.Free
#         )
        
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
        
#         logger.info(f"Successfully created user: {user.email}")
#         return db_user
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error creating user: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creating user: {str(e)}"
#         )

from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.utils.auth import verify_password, get_password_hash
import logging

logger = logging.getLogger(__name__)

def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user."""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"User with email {user.email} already exists")
            return None

        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            subscription_plan='Free'  # Default plan
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Created new user with email: {user.email}")
        return db_user
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise

def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user."""
    try:
        user = get_user_by_email(db, email)
        if not user:
            logger.warning(f"No user found with email: {email}")
            return None
            
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {email}")
            return None
            
        logger.info(f"User authenticated successfully: {email}")
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise