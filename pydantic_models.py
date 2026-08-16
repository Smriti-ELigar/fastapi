from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=255, description="Product name (1-255 chars)")
    price: float = Field(..., gt=0, description="Product price (must be > 0)")
    description: str = Field(default="", max_length=500, description="Product description (max 500 chars)")
    quantity: int = Field(..., ge=0, description="Product quantity (must be >= 0)")

#no need of the constructor init method as pydantic automatically generates it for us.
# Field() adds validation:
# ... means required field
# min_length=1, max_length=255: name must be 1-255 chars
# gt=0: price must be greater than 0
# ge=0: quantity must be greater than or equal to 0