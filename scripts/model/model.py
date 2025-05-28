from pydantic import BaseModel, EmailStr

class EmployeeCreate(BaseModel):
    email: EmailStr
    name: str
    dept_id: int
    role_id: int
    current_user_role_id: int
    current_user_dept_id: int

class EmployeeRead(BaseModel):
    employee_id: int
    email: EmailStr
    name: str
    dept_id: int
    role_id: int
    current_user_role_id: int
    current_user_dept_id: int

class EmployeeUpdate(BaseModel):
    email: EmailStr
    name: str
    dept_id: int
    role_id: int
    current_user_role_id: int
    current_user_dept_id: int
