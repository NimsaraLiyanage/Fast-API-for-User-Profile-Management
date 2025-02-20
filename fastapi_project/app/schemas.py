from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class AddressBase(BaseModel):
    address_line_one: str
    address_line_two: Optional[str] = None
    city: str
    country: str


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    occupation: str


class UserCreate(UserBase):
    profile_picture: Optional[HttpUrl] = None
    addresses: List[AddressCreate]


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None
    addresses: Optional[List[AddressCreate]] = None


class User(UserBase):
    id: int
    profile_picture: Optional[str]
    addresses: List[Address] = []

    class Config:
        orm_mode = True
