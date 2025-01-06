from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.auth import (
    create_access_token,
    get_password_hash,
    authenticate_user,
    oauth2_scheme
)
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole, Student, Teacher
from app.schemas.user import UserCreate, Token, UserInDB

router = APIRouter()


@router.post("/register", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=getattr(UserRole, user.role),
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    print(user.role)
    # 根据不同角色，在不同表中创建数据
    if user.role == "STUDENT":
        db.add(Student(id=db_user.id,
                       username=user.username,
                       full_name=user.full_name,
                       email=user.email,
                       ))
    elif user.role == "TEACHER":
        db.add(Teacher(id=db_user.id,
                       username=user.username,
                       full_name=user.full_name,
                       email=user.email,
                       ))
    db.commit()
    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    print(f"Login attempt for user: {form_data.username}")
    db = next(get_db())
    try:
        if not form_data.username or not form_data.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="用户名或密码不能为空",
            )
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "role": user.role,
            "username": user.username
        }
    finally:
        db.close()

