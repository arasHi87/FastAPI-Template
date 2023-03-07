import schemas
from deps import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
user_repo = UserRepository(User)

CREATE_USER = {
    201: {
        "description": "User created successfully",
        "content": {"json": {"detail": "OK"}},
    },
    500: {
        "description": "Internal server error",
        "content": {"json": {"detail": "Internal server error"}},
    },
}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_USER,
    response_model=schemas.User,
)
async def create_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    if await user_repo.get_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    # Create user
    user: User = await user_repo.create(db, payload)
    return user
