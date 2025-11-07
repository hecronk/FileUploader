from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError
from sqlalchemy.orm import Session

from src.core.database.db import get_db
from src.core.database.models import User
from src.core.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(security_scopes: SecurityScopes, token: str = Security(oauth2_scheme), db: Session = Depends(get_db),):
    try:
        payload = await decode_access_token(token)
        user_scopes = payload.get("scopes", [])
        # check required scopes
        for scope in security_scopes.scopes:
            if scope not in user_scopes:
                raise HTTPException(status_code=403, detail="Not enough permissions")

        user = db.query(User).filter_by(uuid=payload.get("sub")).first()

        if user:
            return user
        else:
            raise JWTError
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
