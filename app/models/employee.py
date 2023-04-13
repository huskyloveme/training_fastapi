from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    id: Optional[int]
    name: str
    age: int
    address: str
    employee_code: str



