from pydantic import BaseModel

class Register(BaseModel):
    name:str
    email:str
    mobileNumber:str
    password:str
    address:str

class Login(BaseModel):
    email:str
    password:str

class LoginView(BaseModel):
    id:int
    email:str
    name:str