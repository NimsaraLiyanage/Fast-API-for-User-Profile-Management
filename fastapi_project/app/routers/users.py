from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, models, schemas, database
from pathlib import Path

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def get_users(db: Session = Depends(database.get_db)):
    return crud.get_users(db)


@router.put("/users/{username}", response_model=schemas.User)
def update_user_endpoint(username: str, user_update: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    updated_user = crud.update_user(db, username, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{username}")
def delete_user_endpoint(username: str, db: Session = Depends(database.get_db)):
    result = crud.delete_user(db, username)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/users/{user_id}/upload_profile_picture")
def upload_profile_picture(user_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    file_ext = Path(file.filename).suffix
    if file_ext not in [".jpg", ".png"]:
        raise HTTPException(status_code=400, detail="Only .jpg and .png files are allowed")

    file_location = f"static/profile_pics/{user_id}{file_ext}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.profile_picture = file_location
        db.commit()
        db.refresh(user)

    return {"filename": file_location}
