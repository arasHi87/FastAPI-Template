from typing import Optional

import schemas
from deps import get_current_user, get_db
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
    name="user:create_user",
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


GET_USER = {
    200: {
        "description": "User found",
        "content": {"json": {"id": 1, "name": "m3ow87", "email": "m3ow87@gmail.com"}},
    },
    404: {
        "description": "User not found",
        "content": {"json": {"detail": "User not found"}},
    },
}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=GET_USER,
    response_model=schemas.UserWithoutPassword,
    name="user:get_user",
)
async def get_user(
    current_user: schemas.User = Depends(get_current_user),
):
    return current_user


UPDATE_USER = {
    200: {
        "description": "User updated successfully",
        "content": {"json": {"id": 1, "name": "m3ow87", "email": "m3ow87@gmail.com"}},
    },
    400: {
        "description": "Email already exists or wrong password",
        "content": {"json": ["Email already exists", "Wrong password"]},
    },
    404: {
        "description": "User not found",
        "content": {"json": {"detail": "User not found"}},
    },
}


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    responses=UPDATE_USER,
    response_model=schemas.UserWithoutPassword,
    name="user:update_user",
)
async def update_user(
    payload: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    # check if email already exists
    mail_check: Optional[User] = await user_repo.get_by_email(db, payload.email)
    if mail_check is not None and mail_check.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    # update user
    user = await user_repo.update(db, payload, current_user)
    return user


DELETE_USER = {
    200: {
        "description": "User deleted successfully",
        "content": {"json": {"detail": "OK"}},
    },
    404: {
        "description": "User not found",
        "content": {"json": {"detail": "User not found"}},
    },
}


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses=DELETE_USER,
    response_model=schemas.Msg,
    name="user:delete_user",
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # check if user exists
    user: Optional[User] = await user_repo.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # delete user
    await user_repo.delete(db, user)
    return schemas.Msg(detail="OK")
