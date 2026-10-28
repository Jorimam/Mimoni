from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from ..database import get_db
from ..models import users as model_users
from ..schemas import users as schema_users
from ..security import hash_password


router = APIRouter(prefix="/users", tags=["users"])

CONFLICT_MSG = "Username or email already in use"


def get_user_or_404(user_id: int, db: Session) -> model_users.User:
    user = db.get(model_users.User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


@router.post(
    "/register",
    response_model=schema_users.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_in: schema_users.UserCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(model_users.User)
        .filter(
            or_(
                model_users.User.username == user_in.username,
                model_users.User.email == user_in.email,
            )
        )
        .first()
    )
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, CONFLICT_MSG)

    data = user_in.model_dump(exclude={"password"})
    new_user = model_users.User(**data, hashed_password=hash_password(user_in.password))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:  # two requests raced past the check
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, CONFLICT_MSG)
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schema_users.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


@router.patch("/{user_id}", response_model=schema_users.UserResponse)
def update_user(
    user_id: int, user_in: schema_users.UserUpdate, db: Session = Depends(get_db)
):
    user = get_user_or_404(user_id, db)
    changes = user_in.model_dump(exclude_unset=True)

    if "username" in changes or "email" in changes:
        clash = (
            db.query(model_users.User)
            .filter(
                model_users.User.id != user_id,
                or_(
                    model_users.User.username == changes.get("username"),
                    model_users.User.email == changes.get("email"),
                ),
            )
            .first()
        )
        if clash:
            raise HTTPException(status.HTTP_409_CONFLICT, CONFLICT_MSG)

    for field, value in changes.items():
        setattr(user, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, CONFLICT_MSG)
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)