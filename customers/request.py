CUSTOMERS = [
    {
        "id": 1,
        "name": "Sara McSarison",
        "address": "1234 Street Rd"
    },
    {
        "id": 2,
        "name": "Dara McDarison",
        "address": "1234 Street Rd"
    },
    {
        "id": 3,
        "name": "Tina McTinason",
        "address": "1234 Street Rd"
    }
]


def get_all_customers():
    return CUSTOMERS

def get_single_customer(id):
    requested_customer = None

    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer
