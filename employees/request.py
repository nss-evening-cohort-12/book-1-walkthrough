import json
from models import Employee
import sqlite3


def get_all_employees():
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        from Employee e
        """)

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])

            employees.append(employee.as_dict())

    return json.dumps(employees)


def create_employee(employee):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id )
        VALUES
            ( ?, ?, ?);
        """, (employee['name'], "",
              employee['locationId'], ))

        id = db_cursor.lastrowid

        employee['id'] = id

        return employee
