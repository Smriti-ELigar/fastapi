from fastapi import FastAPI, Depends
# from models import Product
from pydantic_models import Product
import database_models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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

# will run this function once and call it from other functions to open session (dependency injection) and close the session after the function is executed. this will ensure that the session is closed after the function is executed and we don't have to worry about closing the session in every function.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # this gives count of how many times the product is present in the database. if it is 0 then we will add the products to the database. if it is not 0 then we will not add the products to the database.
        count = db.query(database_models.Product).count()

        if count == 0:
            for product in products:
                 # no need to write sql queries, just say add, make sure to add product of database models and not of pydantic models, and need to convert the pydantic object using model dump which will give us a dictionary and then unpack it using ** which will give us the values of the dictionary and then pass it to the Product class of database models which will create a new instance of the Product class and then add it to the database session.
                db.add(database_models.Product(**product.model_dump()))

            db.commit()
    finally:
        db.close()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): # injecting the dependency here.
    return db.query(database_models.Product).all() # session is opened before, now we are querying the database to get all the products and returning it as a response. the session will be closed after the function is executed.

# this is the endpoint to get a product by its id. The product_id is passed as a path parameter in the URL. The product_id is an integer. The function get_product takes the product_id as an argument and returns the product with the given id.
# this is a decorator that tells FastAPI that this function is a GET request and the URL path is /products/{product_id}. 
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        return db_product
    return "Product not found"

# this is the endpoint to create a new product.we are creating a method called create_product of type post. from client side the product details need to be sent in the request body in JSON format. The product is of type Product which is a pydantic model. The product is appended to the products list and returned as a response.
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)): #the product: Product is from pydantic so need to convert into database_model product.
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

# @app.put("/products/{product_id}")
# def update_product(product_id: int, updated_product: Product):
#     # enumerate is used to get the index of the product in the products list. The index is used to update the product in the products list. The updated_product is returned as a response.
#     for i, product in enumerate(products):
#         if product.id == product_id:
#             updated_product.id = product_id  # Force the ID to match the path parameter
#             # products[i] means we are accessing the product at the index in the products list. The updated_product is assigned to the product at the index in the products list. The updated_product is returned as a response.
#             products[i] = updated_product
#             return updated_product
#     return {"error": "Product not found"}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first() # to check if the product exists
    if db_product:
        db_product.name = updated_product.name
        db_product.price = updated_product.price
        db_product.description = updated_product.description
        db_product.quantity = updated_product.quantity   
        db.commit()
    else:
        return "no product found"

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first() # to check if the product exists
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"

# @app.delete("/products/{product_id}")
# # when thinking of what arguements to use, think which attributes are required to delete a product. The product_id is required to delete a product. The product_id is passed as a path parameter in the URL. The function delete_product takes the product_id as an argument and deletes the product with the given id.
# def delete_product(product_id: int):
#     for i, product in enumerate(products):
#         if product.id == product_id:
#             # del is used to delete the product from the products list. The product is deleted from the products list and a success message is returned as a response.
#             del products[i]
#             return {"message": "Product deleted successfully"}
#     return {"error": "Product not found"}