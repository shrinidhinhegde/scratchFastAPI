from pydantic import BaseModel


class Success(BaseModel):
    message: str

    class Config:
        orm_mode = True


class Student(BaseModel):
    id: int
    name: str
    email: str
    department: str

    class Config:
        orm_mode = True


class Department(BaseModel):
    id: int
    name: str
    total_students: int

    class Config:
        orm_mode = True
