from pydantic import BaseModel

class Register(BaseModel):
    name:str
    email:str
    phoneNumber:str
    password:str
    address:str