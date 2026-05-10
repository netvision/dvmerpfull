from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import require_capability
from database import get_db
from models import Department, User
from schemas import DepartmentOut, DepartmentCreateIn, DepartmentUpdateIn

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/", response_model=List[DepartmentOut])
def list_departments(
    db: Session = Depends(get_db),
    _user: User = Depends(require_capability("user_management"))
):
    return db.query(Department).order_by(Department.name).all()


@router.post("/", response_model=DepartmentOut, status_code=201)
def create_department(
    body: DepartmentCreateIn,
    db: Session = Depends(get_db),
    _user: User = Depends(require_capability("user_management"))
):
    existing = db.query(Department).filter(Department.name == body.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    
    dept = Department(name=body.name, description=body.description)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.put("/{dept_id}", response_model=DepartmentOut)
def update_department(
    dept_id: int,
    body: DepartmentUpdateIn,
    db: Session = Depends(get_db),
    _user: User = Depends(require_capability("user_management"))
):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    if body.name is not None:
        dept.name = body.name
    if body.description is not None:
        dept.description = body.description
    
    db.commit()
    db.refresh(dept)
    return dept


@router.delete("/{dept_id}", status_code=24)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(require_capability("user_management"))
):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if any staff are linked
    if dept.staff_profiles:
         raise HTTPException(status_code=400, detail="Cannot delete department with linked staff")

    db.delete(dept)
    db.commit()
    return None
