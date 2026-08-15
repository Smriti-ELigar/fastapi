from fastapi import FastAPI
# from models import Product
from pydantic_models import Product
import database_models
from database import SessionLocal, engine


app = FastAPI()

# we need to tell sqlalc that it is responsible for creating the tables in the database. so we will import the Base class from database_models.py and call the create_all() method on it. this will create the tables in the database. we will pass the engine object to the create_all() method. this will tell sqlalc which db to create the tables in.
# so this base class not only used for inheritance in the database_models.py but to get the metadata (id, name etc) and use that to create the tables in the database. so we will call the create_all() method on the metadata of the base class and pass the engine object to it. this will create the tables in the database.
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return ("uu cann doo itt bitchhh")

#database isnt up yet. so to actually fetch the products, the products are only not there. so for now we'll just ceate a dictonary by specifying the values.
#or better way to do it is by creating a file called products.py or models.py.
# products = [
#     Product(1, "Product 1", 10.0, "Description of Product 1", 100),
#     Product(2, "Product 2", 20.0, "Description of Product 2", 200),
#     Product(3, "Product 3", 30.0, "Description of Product 3", 300)
# ]

#u need to speficify the variabes here when using the pydantic model as it automatically generates the init method for us. so we need to specify the variables here when creating the instance of the class.
products = [
    Product(id=1, name="Product 1", price=10.0, description="Description of Product 1", quantity=100),
    Product(id=2, name="Product 2", price=20.0, description="Description of Product 2", quantity=200),
    Product(id=3, name="Product 3", price=30.0, description="Description of Product 3", quantity=300)
]


@app.get("/products")
def get_products():
    # u need to have a database connection and query the database to get the products. for now we are just returning the products list.
    db = SessionLocal()
    return products #u call the instance

# this is the endpoint to get a product by its id. The product_id is passed as a path parameter in the URL. The product_id is an integer. The function get_product takes the product_id as an argument and returns the product with the given id.
# this is a decorator that tells FastAPI that this function is a GET request and the URL path is /products/{product_id}. 
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}

# this is the endpoint to create a new product.we are creating a method called create_product of type post. from client side the product details need to be sent in the request body in JSON format. The product is of type Product which is a pydantic model. The product is appended to the products list and returned as a response.
@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    # enumerate is used to get the index of the product in the products list. The index is used to update the product in the products list. The updated_product is returned as a response.
    for i, product in enumerate(products):
        if product.id == product_id:
            updated_product.id = product_id  # Force the ID to match the path parameter
            # products[i] means we are accessing the product at the index in the products list. The updated_product is assigned to the product at the index in the products list. The updated_product is returned as a response.
            products[i] = updated_product
            return updated_product
    return {"error": "Product not found"}

@app.delete("/products/{product_id}")
# when thinking of what arguements to use, think which attributes are required to delete a product. The product_id is required to delete a product. The product_id is passed as a path parameter in the URL. The function delete_product takes the product_id as an argument and deletes the product with the given id.
def delete_product(product_id: int):
    for i, product in enumerate(products):
        if product.id == product_id:
            # del is used to delete the product from the products list. The product is deleted from the products list and a success message is returned as a response.
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}