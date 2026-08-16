# need to do configuration for the database connection. so we will create a file called database.py and put the database connection code in it. then we will import the database connection in main.py and use it to fetch the products from the database.
# first a session needs to be opened when wanting to connect to a db or a server
# so we will create a object for session which will be used in the main.py file to connect to the database. 
# sessionmaker is a factory/class for creating new Session objects. The sessionmaker function takes the engine as an argument and returns a new Session object. The Session object is used to interact with the database. The Session object is used to create, read, update, and delete records in the database.

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .exceptions import DatabaseConnectionError

load_dotenv()
db_url = os.getenv("db_url")
# this is the database url. it is a string that specifies the database type, the database name, and the database location. sqlite is a lightweight database that is easy to set up and use. it is a good choice for small projects or for testing purposes. the database name is products.db and it is located in the current directory. the database url is passed to the create_engine function which creates a new engine object that is used to connect to the database.
# engine is the one that tells which db we connecting to and how we connecting to.
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_database_health():
    db = SessionLocal()
    try:
        # Try to execute a simple query to verify connection. will return 1 i.e true. 
        # "I am giving you a raw SQL statement. Treat this string as SQL."
        db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        raise DatabaseConnectionError(f"Database connection error: {str(e)}") #message is passed to the DatabaseConnectionError class which is defined in the exceptions.py file. this class inherits from the built-in Exception class and is used to indicate that a database connection error has occurred. the message is passed to the parent Exception class which is used to display the error message.
    finally:
        db.close()