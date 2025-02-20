from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    profile_picture = Column(String(255), nullable=True)
    occupation = Column(String(100))

    addresses = relationship("Address", back_populates="owner", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_line_one = Column(String(255))
    address_line_two = Column(String(255), nullable=True)
    city = Column(String(100))
    country = Column(String(100))

    owner = relationship("User", back_populates="addresses")
