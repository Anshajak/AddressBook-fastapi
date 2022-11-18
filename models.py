from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    token = Column(String, unique=True, index=True)

    address = relationship("Address", back_populates="owner")


class Address(Base):
    __tablename__ = "address"
    owner_id = Column(Integer, ForeignKey("users.id"))

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Numeric(10,7), index=True)
    longitude = Column(Numeric(10,7), index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    pincode = Column(String, index=True)
    addresstype = Column(String, index=True)


    owner = relationship("User", back_populates="address")
