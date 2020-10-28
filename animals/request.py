from models.customer import Customer
from models.location import Location
import locations
import sqlite3
import json

from models import Animal

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennels.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'], row['id'])

            # Create a Location instance from the current row
            location = Location(row['location_id'], row['location_name'], row['location_address'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__


            # Add the dictionary representation of the animal to the list
            animals.append(animal.as_dict())

        # Use `json` package to properly serialize list as JSON
        return json.dumps(animals)

# Function with a single parameter
def get_single_animal(id, query = {}):
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        if query is False:
            db_cursor.execute("""
            SELECT
                animal.id,
                animal.name,
                animal.breed,
                animal.status,
                animal.customer_id,
                animal.location_id
            FROM animal
            WHERE animal.id = ?
            """, ( id, ))
        elif query['_expand']:
            expand = query['_expand']
            if 'customer' in expand and 'location' in expand:
                db_cursor.execute("""
                SELECT
                    a.id,
                    a.name,
                    a.breed,
                    a.status,
                    a.customer_id,
                    a.location_id,
                    l.name location_name,
                    l.address location_address,
                    c.name customer_name
                FROM Animal a
                JOIN Location l
                    ON l.id = a.location_id
                join Customer c
                    on c.id = a.customer_id
                where a.id = ?
                """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        try:
            animal = Animal( 
            data['name'],
            data['breed'],
            data['status'],
            data['location_id'],
            data['customer_id'],
            data['id']
        )
        except ValueError:
            return False
        
        try:
            # Create a Location and Customer instance from the current row
            location = Location(data['location_id'], data['location_name'], data['location_address'])
            customer = Customer(data['customer_id'], data['customer_name'])
            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__
        except ValueError:
            # user didn't ask for location or customer ignore error
            pass


        return json.dumps(animal.as_dict())

def create_animal(new_animal):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['treatment'], new_animal['locationId'],
              new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)

def update_animal(id, new_animal):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['treatment'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_animal(id):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))
