#this is the tradiitonal method without pydantic for data validation.


# a class or blueprint for the products table in the database and the attributes of the products table.
# The attributes/properties are the columns of the products table. The class is used to create a new product and to fetch the products from the database.
class Product:
    id: int
    name: str
    price: float
    description: str
    quantity: int

    # now this init method is used to initialize the attributes of the class. 
    # It is called when a new object of the class is created. 
    # The self parameter is used to refer to the current object of the class. 
    # The self parameter is used to access the attributes and methods of the class. 
    # The self parameter is not required to be passed when calling the init method.
    # It is automatically passed by Python.
    def __init__(self, id: int, name: str, price: float, description: str, quantity: int):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    #so when this instance/object is created, the init method is called and the values of the attributes of the object are initialized. (as the init method is automaticaaly called, it takes the parameters and assigns them as attributes to the object)
    # p1 =Product(1, "Product 1", 10.0, "Description of Product 1", 100)

