import json
from models import parsed_url
from customers import get_all_customers, get_customers_by_email, create_customer
from employees import get_all_employees, create_employee
from http.server import BaseHTTPRequestHandler, HTTPServer
from locations import get_all_locations, create_location
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, update_animal
from models import ParsedUrl


# Here's a class. It inherits from another class.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_query(self, query_string):
        pairs = query_string.split("&")  # [ '_expand=location', '_expand=customer' ]
        query = {}

        for pair in pairs:
            (key, value) = tuple(pair.split('='))
            if key in query:
                query[key].append(value)
            else:
                query[key] = [value]
        return query

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = ""
        query = {}
        id_int = None
        try:
            id = path_params[2]
        except IndexError:
            pass  # No route parameter exists: /animals
        

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            query = self.parse_query(param)

        if "?" in id:
            # GIVEN: /animals/1?_expand=location&_expand=customer

            param = id.split("?")[1]  # _expand=location&_expand=customer
            id_int = int(id.split("?")[0])  # 1
            query = self.parse_query(param)

        else:
            try:
                id_int = int(id)
            except ValueError:
                pass  # Request had trailing slash: /animals/

        return ParsedUrl(resource, id_int, query)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        if parsed.resource == "animals":
            if parsed.id is not None:
                response = f"{get_single_animal(parsed.id, parsed.query)}"
            else:
                response = f"{get_all_animals()}"
        elif parsed.resource == "customers":
            if len(parsed.query):
                response = f"{get_customers_by_email(parsed.query)}"
            else:
                response = f"{get_all_customers()}"
        elif parsed.resource == "employees": 
            response = f"{get_all_employees()}"
        elif parsed.resource == "locations":
            response = f"{get_all_locations()}"
            
        if response or response is []:
            self._set_headers(200)
        else:
            self._set_headers(404)

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        parsed_url = self.parse_url(self.path)

        # Initialize new animal
        new_object = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if parsed_url.resource == "animals":
            new_object = create_animal(post_body)
        elif parsed_url.resource == "employees":
            new_object = create_employee(post_body)
        elif parsed_url.resource == "customers":
            new_object = create_customer(post_body)
        elif parsed_url.resource == "locations":
            new_object = create_location(post_body)

        if new_object:
            self._set_headers(201)
        else:
            self._set_headers(400)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_object}".encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        parsed_url = self.parse_url(self.path)
    
        success = False

        if parsed_url.resource == "animals":
            success = update_animal(parsed_url.id, post_body)
       
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        
        # Parse the URL
        parsed_url = self.parse_url(self.path)
        success = False

        # Delete a single animal from the list
        if parsed_url.resource == "animals":
            success = delete_animal(parsed_url.id)
        
        if success:
            # Set a 204 response code
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, content-type')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
