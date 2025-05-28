from fastapi import APIRouter
from scripts.constants.api import Endpoints
from scripts.handlers.handler import *
from scripts.constants.app_constants import AppConstants
from scripts.model.model import *
from scripts.handlers.handler import employee_handler

router = APIRouter()

@router.post(Endpoints.api_create_emp)
def create_employee_api(employee: EmployeeCreate):

    if employee.current_user_role_id == 1:  # Admin
        response = employee_handler.create_employee(employee.email, employee.name, employee.dept_id, employee.role_id)

    elif employee.current_user_role_id == 2 and employee.role_id == 3 and employee.dept_id == employee.current_user_dept_id:
        response = employee_handler.create_employee(employee.email, employee.name, employee.dept_id, employee.role_id)

    else:
        raise HTTPException(status_code=403, detail=AppConstants.ACCESS_DENIED)

    if response:
        return {"message": AppConstants.EMPLOYEE_CREATED, "employee_id": response}
    else:
        raise HTTPException(status_code=500, detail=AppConstants.DATABASE_ERROR)


@router.get(Endpoints.api_read_emp)
def read_employee_api(
    employee_id: int,
    current_user_role_id: int,
    current_user_dept_id: int,
    current_user_id: int
):
    if current_user_role_id == 1:  # Admin
        response = employee_handler.read_employee(employee_id)

    elif current_user_role_id == 2:  # Manager
        employee_to_read = employee_handler.read_employee(employee_id)
        if current_user_role_id > employee_to_read[4]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AppConstants.ACCESS_DENIED
            )
        response = employee_handler.read_employee_by_department(employee_id, current_user_dept_id)

    elif current_user_role_id == 3 and current_user_id == employee_id:  # Employee can only read their own data
        response = employee_handler.read_employee(employee_id)

    else:
        raise HTTPException(status_code=403, detail=AppConstants.ACCESS_DENIED)

    if response:
        return {"message": AppConstants.SUCCESS_MESSAGE, "data": response}
    else:
        raise HTTPException(status_code=404, detail=AppConstants.EMPLOYEE_NOT_FOUND)


@router.put(Endpoints.api_update_emp)
def update_employee_api(employee_id: int, employee: EmployeeUpdate):

    if employee.current_user_role_id == 1:  # Admin
        response = employee_handler.update_employee(employee_id, employee.email, employee.name, employee.dept_id, employee.role_id)

    elif employee.current_user_role_id == 2 and employee.dept_id == employee.current_user_dept_id:  # Manager
        response = employee_handler.update_employee(employee_id, employee.email, employee.name, employee.dept_id, employee.role_id)

    else:
        raise HTTPException(status_code=403, detail=AppConstants.ACCESS_DENIED)

    if response:
        return {"message": AppConstants.EMPLOYEE_UPDATED}
    else:
        raise HTTPException(status_code=404, detail=AppConstants.EMPLOYEE_NOT_FOUND)


@router.delete(Endpoints.api_delete_emp)
def delete_employee_api(employee_id: int, user: EmployeeRead):

    if user.current_user_role_id == 1:  # Admin
        response = employee_handler.delete_employee(employee_id)

    elif user.current_user_role_id == 2:  # Manager
        department_employees = select_department_employees_query(
            user.current_user_dept_id)  # Fetch employees in manager's dept

        if any(emp[0] == employee_id for emp in department_employees):
            response = employee_handler.delete_employee(employee_id)
        else:
            raise HTTPException(status_code=403, detail="You can only delete employees in your department.")

    else:
        raise HTTPException(status_code=403, detail=AppConstants.ACCESS_DENIED)

    if response:
        return {"message": AppConstants.EMPLOYEE_DELETED}
    else:
        raise HTTPException(status_code=404, detail=AppConstants.EMPLOYEE_NOT_FOUND)
