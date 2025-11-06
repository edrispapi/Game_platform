"""
User Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, models
from .database import get_db
from shared.auth import create_access_token, verify_token
from datetime import timedelta
import os

router = APIRouter()

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def get_current_user(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    """Get current authenticated user"""
    user_crud = crud.UserCRUD(db)
    user = user_crud.get_user_by_id(token.get("user_id"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user_crud = crud.UserCRUD(db)
    
    # Check if username already exists
    if user_crud.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if user_crud.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    db_user = user_crud.create_user(user)
    return db_user

@router.post("/login", response_model=schemas.UserLoginResponse)
def login_user(login_data: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user_crud = crud.UserCRUD(db)
    session_crud = crud.UserSessionCRUD(db)
    
    # Get user by username or email
    user = user_crud.get_user_by_username_or_email(login_data.username_or_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    
    # Verify password
    if not user_crud.verify_password(user, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    
    # Check if user is active
    if user.status != models.UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is not active"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    # Update last login
    user_crud.update_last_login(user.id)
    
    # Create session if remember_me is True
    if login_data.remember_me:
        device_info = {
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        }
        session_crud.create_session(
            user_id=user.id,
            session_token=access_token,
            device_info=device_info,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    user_crud = crud.UserCRUD(db)
    updated_user = user_crud.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.post("/change-password")
def change_password(
    password_change: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    user_crud = crud.UserCRUD(db)
    
    # Verify current password
    if not user_crud.verify_password(current_user, password_change.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Change password
    success = user_crud.change_password(current_user.id, password_change.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )
    
    return {"message": "Password changed successfully"}

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of users (admin only)"""
    user_crud = crud.UserCRUD(db)
    users = user_crud.get_users(skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user_crud = crud.UserCRUD(db)
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/logout")
def logout_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (deactivate all sessions)"""
    session_crud = crud.UserSessionCRUD(db)
    session_crud.deactivate_all_user_sessions(current_user.id)
    return {"message": "Logged out successfully"}

@router.get("/preferences", response_model=List[schemas.UserPreferenceResponse])
def get_user_preferences(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    preference_crud = crud.UserPreferenceCRUD(db)
    preferences = preference_crud.get_user_preferences(current_user.id)
    return preferences

@router.post("/preferences", response_model=schemas.UserPreferenceResponse)
def create_user_preference(
    preference: schemas.UserPreferenceCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create user preference"""
    preference_crud = crud.UserPreferenceCRUD(db)
    db_preference = preference_crud.create_preference(current_user.id, preference)
    return db_preference

@router.put("/preferences/{preference_key}")
def update_user_preference(
    preference_key: str,
    preference_value: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preference"""
    preference_crud = crud.UserPreferenceCRUD(db)
    updated_preference = preference_crud.update_preference(
        current_user.id, preference_key, preference_value
    )
    if not updated_preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    return updated_preference

@router.get("/sessions", response_model=List[schemas.UserSessionResponse])
def get_user_sessions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user active sessions"""
    session_crud = crud.UserSessionCRUD(db)
    sessions = db.query(models.UserSession).filter(
        models.UserSession.user_id == current_user.id,
        models.UserSession.is_active == True
    ).all()
    return sessions