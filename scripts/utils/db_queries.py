from scripts.utils.db_utils import get_db_connection

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
            # result = cursor.execute(f'SELECT employee_id FROM employees WHERE employees.email = {params["email"]};')
            return True
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def create_employee_query(email, name, dept, role_id):
    query = """
        INSERT INTO public."employees" (email, name, dept_id, role_id)
        VALUES (%s, %s, %s, %s) RETURNING employee_id
    """
    return execute_query(query, (email, name, dept, role_id), fetch_one=True, commit=True)

def read_employee_query(employee_id):
    query = "SELECT * FROM employees WHERE employee_id = %s"
    return execute_query(query, (employee_id,), fetch_one=True)

def read_employee_query_by_department(employee_id, dept_id):
    query = "SELECT * FROM employees WHERE employee_id = %s AND dept_id = %s"
    return execute_query(query, (employee_id, dept_id), fetch_one=True)

def update_employee_query(employee_id, email, name, dept, role_id):
    query = """
        UPDATE employees SET email = %s, name = %s, dept_id = %s, role_id = %s WHERE employee_id = %s
    """
    return execute_query(query, (email, name, dept, role_id, employee_id), commit=True)

def delete_employee_query(employee_id):
    query = "DELETE FROM employees WHERE employee_id = %s"
    return execute_query(query, (employee_id,), commit=True)

def select_department_employees_query(dept_id):
    query = "SELECT employee_id FROM employees WHERE dept_id = %s"
    return execute_query(query, (dept_id,), fetch_all=True)
