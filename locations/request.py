import json
import sqlite3

from models import Location

def get_all_locations():
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address
        from location c
        """)

        locations = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__)


    return json.dumps(locations)

def get_location(id):
    with sqlite3.connect("./kennels.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            l.id,
            l.name,
            l.address
        from location l
        """)

        data = db_cursor.fetchall()
        location = Location(data['id'], data['name'], data['address'])
        return location
        


def create_location(location):
    with sqlite3.connect("./kennels.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Customer
            ( name, address )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (location['name'], location['address'],))

        location['id'] = db_cursor.lastrowid

        return location
