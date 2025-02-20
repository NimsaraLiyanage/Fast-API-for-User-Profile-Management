from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()


@router.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address_update: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    """ Update an existing address """
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    address.address_line_one = address_update.address_line_one
    address.address_line_two = address_update.address_line_two
    address.city = address_update.city
    address.country = address_update.country
    db.commit()
    db.refresh(address)
    return address


@router.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(database.get_db)):
    """ Delete an address by ID """
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()
    return {"message": "Address deleted successfully"}
