import json
import sqlite3

from models import Customer


def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        """)

        # Initialize an empty list to hold all customer representations
        customers = []
        dataset = db_cursor.fetchall()

        # Iterate all rows of data returned from database
        for row in dataset:

            # Create an customer instance from the current row
            customer = Customer(row['id'], row['name'], row['address'], row['email'],
                            row['password'])

            customers.append(customer.__dict__)

    return json.dumps(customers)


def get_customers_by_email(email):

    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], "", row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)


def get_single_customer(id):
    # Open a connection to the database
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['name'], data['address'], data['email'],
                        data['password'])
        customer.id = data['id']

        return json.dumps(customer.__dict__)


def update_customer(id, new_customer):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Customer
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?
        WHERE id = ?
        """, (new_customer['name'], new_customer['address'],
              new_customer['email'], new_customer['password'],
              id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_customer(id):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Customer WHERE id = ?
        """, (id, ))
