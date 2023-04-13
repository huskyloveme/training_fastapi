from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    name: str
    age: int
    address: Optional[str]
    employee_code: Optional[str]


