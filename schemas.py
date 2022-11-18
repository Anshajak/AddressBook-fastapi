from typing import Union
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class AdminCreate(BaseModel):
    email: str
    username: str
    password: str
    is_admin:bool
    is_active:bool

class UserEdit(BaseModel):
    password: str

class AddressCreate(BaseModel):
    latitude: float
    longitude: float
    street: str
    city: str
    state: str
    pincode: str
    addresstype: str
