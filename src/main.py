import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import response_schemas
import schemas
from src import database, models
from src.database import get_db

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='Scratch FastAPI')

if __name__ == '__main__':
    load_dotenv()
    env_vars = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_SERVER', 'POSTGRES_PORT', 'POSTGRES_DATABASE']

    try:
        for var in env_vars:
            x = os.environ[var]
    except KeyError as e:
        print(f"Please set the environment variable {e}. Application must contain {env_vars}")
        exit(1)

    uvicorn.run('src.main:app', reload=True, host='0.0.0.0', port=8000)


# Functions

def add_student(student: schemas.Student, db: Session = Depends(get_db)):
    new_stud = models.Student(name=student.name, email=student.email, department=student.department)
    db.add(new_stud)
    db.flush()

    return new_stud


# Routes

@app.get('/student', description='Endpoint to get all students', response_model=List[response_schemas.Student])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@app.post('/student', description='Endpoint to add new student', response_model=response_schemas.Success)
def create_student(student: schemas.Student, db: Session = Depends(get_db)):
    save_point = db.begin_nested()
    add_student(student, db)

    department = db.query(models.Department).filter(models.Department.name == student.department).first()
    if department:
        department.total_students += 1
    else:
        save_point.rollback()
        raise HTTPException(status_code=404, detail='Department not found')

    db.commit()
    return response_schemas.Success(message='Student added successfully')


@app.get('/department', description='Endpoint to get all departments', response_model=List[response_schemas.Department])
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(models.Department).all()
    return departments


@app.post('/department', description='Endpoint to add new department', response_model=response_schemas.Success)
def create_department(department: schemas.Department, db: Session = Depends(get_db)):
    new_dept = models.Department(name=department.name)
    db.add(new_dept)

    db.commit()
    print(new_dept.id)
    return response_schemas.Success(message='Department added successfully')
