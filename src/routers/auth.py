from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database.db import get_db
from src.core.settings.settings import settings
from src.core.utils import security

from src.core.database.models import User
from src.core.utils.security import create_access_token
from src.dependencies.auth import get_current_user
from src.schemas.user import UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter_by(username=user.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=user.username,
        hashed_password= await security.get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg": "User created", "uuid": str(user.uuid)}

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    found_user = db.query(User).filter_by(username=user.username).first()
    if not found_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    valid_password = await security.verify_password(user.password, found_user.hashed_password)
    if not valid_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if await security.needs_rehash(found_user.hashed_password):
        found_user.hashed_password = await security.get_password_hash(user.password)
        db.commit()

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": str(found_user.uuid)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "uuid": str(current_user.uuid)}
