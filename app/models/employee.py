from pydantic import BaseModel
from typing import Optional
from beanie import Document, Indexed
from fastapi import File, UploadFile

class Employee(BaseModel):
    id: Optional[int]
    name: str
    age: int
    address: str
    employee_code: str

class Test(Document):
    id: int
    name: str
    age: int
    address: str
    employee_code: str

    class Settings:
        name = "test"

class Image(BaseModel):
    id: int
    name: str
    data: bytes