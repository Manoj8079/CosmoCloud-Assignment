# app/schemas.py
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str


class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 20,
                "address": {
                    "city": "New York",
                    "country": "USA"
                }
            }
        }

class StudentUpdate(BaseModel):
    name: str
    age: int
    address: Address
