import schemas
from deps import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils import create_access_token

router = APIRouter()
user_repo = UserRepository(User)

USER_AUTH = {
    200: {
        "description": "User authenticated successfully",
        "content": {"json": {"access_token": "token", "token_type": "bearer"}},
    },
    401: {
        "description": "Incorrect email or password",
        "content": {"json": {"detail": "Incorrect email or password"}},
    },
}


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses=USER_AUTH,
    response_model=schemas.AuthToken,
    name="auth:user_auth",
)
async def user_auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await user_repo.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    claims = {"id": user.id, "name": user.name, "email": user.email}
    return schemas.AuthToken(
        access_token=create_access_token(claims), token_type="bearer"
    )  # nosec
