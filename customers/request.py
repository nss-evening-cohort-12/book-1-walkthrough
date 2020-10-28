import json
import sqlite3

from models import Customer


def get_all_customers():
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        """)

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(
                row['id'],
                row['name'],
                row['address'],
                row['email'],
                row['password']
            )

            customers.append(customer.__dict__)

        return json.dumps(customers)


def get_customers_by_email(query):
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM Customer c
        WHERE c.email = ?
        """, ( query['email'], ))

        data = db_cursor.fetchone()

        
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])
            

        return json.dumps(customer.__dict__)


def create_customer(customer):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Customer
            ( name, address, email, password )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (customer['name'], customer['address'],
              customer['email'], customer['password'], ))

        customer['id'] = db_cursor.lastrowid

        return customer
