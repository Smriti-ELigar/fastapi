# Python has a specific type of error called ProductNotFoundError instead of just rasing a generic Exception. This is a custom exception class that inherits from the built-in Exception class. It is used to indicate that a product with a specific ID was not found in the database. The class has an __init__ method that takes a product_id as an argument and constructs an error message indicating that the product with that ID was not found. This custom exception can be raised in the code when a product is not found, allowing for more specific error handling and clearer communication of the issue to the user or developer.
class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} not found, http status code 404"
        super().__init__(self.message)
        #"Call the Exception (parent)constructor and give it my error message."
#This allows Python's normal exception machinery to know what message belongs to your exception.

class InvalidProductDataError(Exception):
    def __init__(self, message: str = "Invalid product data provided, http status code 400"):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    def __init__(self, errors: list):
        self.errors = errors
        self.message = "Validation error occurred, http status code 422"
        super().__init__(self.message)

class ProductAlreadyExistsError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} already exists, http status code 409"
        super().__init__(self.message)

class DatabaseConnectionError(Exception):
    def __init__(self, message: str = "Database connection error occurred, http status code 500"):
        self.message = message
        super().__init__(self.message)



# Because ProductNotFoundError inherits from Exception, Python knows that it is an exception and allows you to do:
# raise ProductNotFoundError(...)


# (Exception) — Inherits from Python's built-in Exception class, making it a custom exception
# __init__ — Constructor/initialization method (called when creating an instance)
# self — Reference to the instance itself
# product_id: int — Parameter with type hint; expects an integer
# self.product_id — Creates an instance variable storing the product ID
# = product_id — Assigns the parameter value to the instance variable
# self.message — Instance variable storing the error message
# super() — Calls the parent class (Exception)
# .__init__(...) — Invokes the parent's constructor
# self.message — Passes the error message to the parent Exception class



# Why do we have __init__?

# You wrote:

# def __init__(self, product_id: int):

# This is the constructor of your exception.

# You're saying:

# "Whenever someone creates a ProductNotFoundError, I want them to give me the product ID."

# For example:

# error = ProductNotFoundError(123)

# Here:

# product_id = 123