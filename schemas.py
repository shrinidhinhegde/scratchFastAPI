from pydantic import BaseModel


class Student(BaseModel):
    name: str
    email: str
    department: str

    class Config:
        orm_mode = True


class Department(BaseModel):
    name: str

    class Config:
        orm_mode = True
