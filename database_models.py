from sqlalchemy import Column, Integer, String, Float
# how sqlachemy will know that this prdoct class is supposed to be linked with table or db is coz of this base class. this base class is from sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# this declarative_base() is a function that returns a new base class  which we use to inherit from when creating our own classes
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    quantity = Column(Integer, nullable=False)

# this base is from sqlalchemy. 