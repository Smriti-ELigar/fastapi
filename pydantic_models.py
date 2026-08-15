from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int

#no need of the constructor init method as pydantic automatically generates it for us.