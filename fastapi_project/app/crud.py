from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas
import os


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists. Please choose a different username.")

    try:
        db_user = models.User(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            occupation=user.occupation,
            profile_picture=user.profile_picture
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        for addr in user.addresses:
            db_address = models.Address(
                user_id=db_user.id,
                address_line_one=addr.address_line_one,
                address_line_two=addr.address_line_two,
                city=addr.city,
                country=addr.country
            )
            db.add(db_address)
            db.commit()

        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating user. Username might already exist.")


def get_users(db: Session):
    return db.query(models.User).all()


def update_user(db: Session, username: str, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None

    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.occupation = user_update.occupation
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        if user.profile_picture and os.path.exists(user.profile_picture):
            os.remove(user.profile_picture)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return None
