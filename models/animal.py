class Animal():
    def __init__(self, name, species, status, location_id, customer_id, unique_id):
        self.id = unique_id
        self.name = name
        self.species = species
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id
        self.location = None
        self.customer = None

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.species,
            "treatment": self.status,
            "locationId": self.location_id,
            "customerId": self.customer_id,
            "location": self.location,
            "customer": self.customer
        }

