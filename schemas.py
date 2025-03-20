from pydantic import BaseModel,field_validator,Field
import re
from models import AccountTypeEnum 
from typing import List

class Register(BaseModel):
    name:str
    email:str
    mobileNumber:str
    password:str
    address:str

    @field_validator('name')
    def nameRegex(cls,name):
        if not re.fullmatch(r"^[a-zA-Z]+(?: [a-zA-Z]+)*$",name.strip()):
            raise ValueError('Invalid name format')
        return name
    @field_validator('email')
    def emailRegex(cls,email):
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',email.strip()):
            raise ValueError('Invalid email format')
        return email
    
    @field_validator('mobileNumber')
    def mobileNumberRegex(cls,mobileNumber):
        if not re.fullmatch(r"^(?:\+91|91)?[6-9]\d{9}$",mobileNumber):
            raise ValueError('Enter a valid mobile number with country code (e.g., +91XXXXXXXXXX).')
        return mobileNumber
    
    @field_validator('password')
    def passwordRegex(cls,password):
        if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$",password):
            raise ValueError('Password must be 6-20 characters long with at least one uppercase, one lowercase, one digit, and one special character (@$!%*#?&).')
        return password
    
class Login(BaseModel):
    email:str
    password:str

class UserSchema(BaseModel):
    id: int
    email: str
    name: str

class LoginView(BaseModel):
    access_token: str
    user:UserSchema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class NewAccount(BaseModel):
    branchName: str = Field(..., min_length=3, max_length=50, description="Branch name must be between 3 to 50 characters.")
    accountNumber: str = Field(..., pattern=r"^\d{10,16}$", description="Account number must be between 10 to 16 digits.")
    ifscCode: str = Field(..., pattern=r"^[A-Z]{4}0[A-Z0-9]{6}$", description="Invalid IFSC code format.")
    bankAddress: str = Field(..., min_length=5, max_length=100, description="Bank address must be between 10 to 100 characters.")
    accountType: AccountTypeEnum
    userId:int

    @field_validator("ifscCode")
    def validate_ifsc_code(cls, v):
        if not v.isalnum() or len(v) != 11:
            raise ValueError("IFSC code must be 11 alphanumeric characters.")
        return v

class UpdateAccount(BaseModel):
    branchName: str = Field(..., min_length=3, max_length=50, description="Branch name must be between 3 to 50 characters.")
    accountNumber: str = Field(..., pattern=r"^\d{10,16}$", description="Account number must be between 10 to 16 digits.")
    ifscCode: str = Field(..., pattern=r"^[A-Z]{4}0[A-Z0-9]{6}$", description="Invalid IFSC code format.")
    bankAddress: str = Field(..., min_length=5, max_length=100, description="Bank address must be between 10 to 100 characters.")
    accountType: AccountTypeEnum

    @field_validator("ifscCode")
    def validate_ifsc_code(cls, v):
        if not v.isalnum() or len(v) != 11:
            raise ValueError("IFSC code must be 11 alphanumeric characters.")
        return v
    
class ViewUser(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class ViewAccount(BaseModel):
    branchName: str
    accountNumber: str
    bankAddress: str
    accountType: AccountTypeEnum

    class Config:
        from_attributes = True

class ViewUserAccount(BaseModel):
    user: ViewUser
    accountDetail: List[ViewAccount]