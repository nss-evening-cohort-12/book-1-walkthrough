LOCATIONS = [
    {
        "id": 1,
        "city": "Nashville",
    },
    {
        "id": 2,
        "city": "Charlotte",
    },
    {
        "id": 3,
        "city": "Chattanooga",
    }
]


def get_all_locations():
    return LOCATIONS

def get_single_location(id):
    requested_location = None

    for location in LOCATIONS:
        if location["id"] == id:
            requested_location = location

    return requested_location
