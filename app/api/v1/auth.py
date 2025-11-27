from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.core.database import get_db
from app.schemas.user import UserLogin, TokenResponse, UserOut
from app.crud.user import get_user_by_username
from app.auth.jwt import verify_password, create_access_token, decode_token
from app.core.config import settings

router = APIRouter(tags=["Auth"])


async def get_current_user(
    token: str,
    db: AsyncSession
):
    username = decode_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(401, "User not found")

    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, payload.username)
    if not user:
        raise HTTPException(400, "Invalid username or password")

    if not verify_password(payload.password, user.password):
        raise HTTPException(400, "Invalid username or password")

    token = create_access_token(user.username)

    expires_at = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return TokenResponse(
        access_token=token,
        expires_at=expires_at
    )


@router.get("/me", response_model=UserOut)
async def me(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    user = await get_current_user(token, db)
    return user
