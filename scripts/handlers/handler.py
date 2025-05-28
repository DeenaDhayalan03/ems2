from fastapi import HTTPException, status
from scripts.constants.app_constants import AppConstants
from scripts.utils.db_queries import *

class employee_handler:

    @staticmethod
    def create_employee(email: str, name: str, dept_id: int, role_id: int):
        try:
            employee = create_employee_query(email, name, dept_id, role_id)
            if employee:
                employee_id = execute_query(f"SELECT employee_id FROM employees WHERE employees.email = '{email}';", fetch_one=True)[0]
                return employee_id
            else:
                return None
        except Exception as e:
            if 'employees_email_key' in str(e):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Employee with email: {email} already exists.")
            return None

    @staticmethod
    def read_employee(employee_id: int):
        try:
            employee = read_employee_query(employee_id)
            if employee:
                return employee
            return None
        except Exception as e:
            return None

    @staticmethod
    def read_employee_by_department(employee_id: int, dept_id: int):
        try:
            employee = read_employee_query_by_department(employee_id, dept_id)
            if employee:
                return employee
            return None
        except Exception as e:
            return None

    @staticmethod
    def update_employee(employee_id: int, email: str, name: str, dept_id: int, role_id: int):
        try:
            employee = read_employee_query(employee_id)
            if not employee:
                return None

            update_employee_query(employee_id, email, name, dept_id, role_id)
            return AppConstants.UPDATE_SUCCESS
        except Exception as e:
            return None

    @staticmethod
    def delete_employee(employee_id: int):
        try:
            employee = read_employee_query(employee_id)
            if not employee:
                return None

            delete_employee_query(employee_id)
            return AppConstants.DELETE_SUCCESS
        except Exception as e:
            return None
