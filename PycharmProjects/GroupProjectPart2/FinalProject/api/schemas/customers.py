from pydantic import BaseModel

class CustomerSchema(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
