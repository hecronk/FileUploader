from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database.db import get_db
from src.core.utils import security

from src.core.database.models import User
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
    found_user = db.query(User).filter_by(
        username=user.username,
    ).first()

    valid_password = await security.verify_password(
        key=user.password,
        stored_hash=found_user.hashed_password
    )

    if not valid_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if security.needs_rehash(found_user.hashed_password):
        found_user.hashed_password = security.get_password_hash(user.password)
        db.commit()

    return {"msg": "User exists", "uuid": str(found_user.uuid)}
