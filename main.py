
from fastapi import FastAPI, Body, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./employees.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# ...existing code...

# Salary calculation endpoint
class SalaryRequest(BaseModel):
    gross_salary: float

class SalaryResponse(BaseModel):
    gross_salary: float
    deductions: float
    net_salary: float

@app.post("/salary/{employee_id}", response_model=SalaryResponse)
def calculate_salary(employee_id: int, salary_req: SalaryRequest = Body(...)):
    db = SessionLocal()
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    db.close()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    gross = salary_req.gross_salary
    if employee.country.lower() == "india":
        deductions = gross * 0.10
    elif employee.country.lower() == "united states":
        deductions = gross * 0.12
    else:
        deductions = 0
    net = gross - deductions
    return SalaryResponse(gross_salary=gross, deductions=deductions, net_salary=net)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    salary = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

class EmployeeRead(EmployeeCreate):
    id: int

@app.get("/")
def root():
    return {"message": "Employee API"}

# CRUD endpoints
@app.post("/employees", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate):
    db = SessionLocal()
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    db.close()
    return db_employee

from fastapi import HTTPException

@app.get("/employees/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int):
    db = SessionLocal()
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    db.close()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeRead)
def update_employee(employee_id: int, employee: EmployeeCreate):
    db = SessionLocal()
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        db.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    db.close()
    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    db = SessionLocal()
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        db.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    db.close()
    return {"message": "Employee deleted"}
