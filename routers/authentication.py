from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas import Register,Login,LoginView
from database import get_db
from models import User
import re

router = APIRouter(tags=['Authentication'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

@router.post('/register',status_code=201,response_model=Register)
def register(request:Register,db:Session=Depends(get_db)):
    if not request.name:
        raise HTTPException(detail={'error': 'Please enter name'},status_code=status.HTTP_404_NOT_FOUND)
    if not request.email:
        raise HTTPException(detail={'error': 'Please enter email'},status_code=status.HTTP_404_NOT_FOUND)
    if not request.mobileNumber:
        raise HTTPException(detail={'error': 'Please enter mobile number'},status_code=status.HTTP_404_NOT_FOUND)
    if not request.password:
        raise HTTPException(detail={'error': 'Please enter password'},status_code=status.HTTP_404_NOT_FOUND)
    if not request.address:
        raise HTTPException(detail={'error': 'Please enter address'},status_code=status.HTTP_404_NOT_FOUND)
    NameReg = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"
    if not re.fullmatch(NameReg,request.name.strip()):
        raise HTTPException(detail={'error':'Please enter valid name'},status_code=status.HTTP_404_NOT_FOUND)

    MobileNumberReg = r"^(?:\+91|91)?[6-9]\d{9}$"
    if not re.fullmatch(MobileNumberReg,request.mobileNumber):
        raise HTTPException(detail={'error':'+91 Required Please enter valid phone number'},status_code=status.HTTP_404_NOT_FOUND)

    EmailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if not re.fullmatch(EmailRegex,request.email):
        raise HTTPException(detail={'error':'Please enter valid email'},status_code=status.HTTP_404_NOT_FOUND)

    PasswordReg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(PasswordReg)
    mat = re.search(pat, request.password)
    
    if not mat:
        raise HTTPException(detail={'error': 'Password must be 6-20 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character (@$!%*#?&)'},status_code=status.HTTP_404_NOT_FOUND)
    user = db.query(User).filter(User.email==request.email)
    if user.first():
        raise HTTPException(detail={'error':'User Already Exists With This Email'},status_code=status.HTTP_404_NOT_FOUND)
    HashedPassword = pwd_context.hash(request.password)
    user_create = User(name=request.name,email=request.email,mobileNumber=request.mobileNumber,password=HashedPassword,address=request.address)
    db.add(user_create)
    db.commit()
    db.refresh(user_create)
    user_data = {
        "id": user_create.id,
        "name": user_create.name,
        "email": user_create.email,
        "mobileNumber": user_create.mobileNumber,
        "address": user_create.address,
    }
    return  JSONResponse(content={'user':user_data,'message':'User Register Sucessfully'})

@router.post('/login',status_code=200,response_model=LoginView)
def login(request:Login,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==request.email).first()
    print('user: ', user)
    if not user:
        raise HTTPException(detail={'error':'User not found'},status_code=status.HTTP_404_NOT_FOUND)
    if not verify_password(request.password,user.password):
        raise HTTPException(detail={'error':'Password is not valid'},status_code=status.HTTP_404_NOT_FOUND)
    return user

# -------------------------------------------------- Admin -----------------------------------------------------------------------

@router.post('/admin-login',status_code=200,response_model=LoginView)
def adminLogin(request:Login,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==request.email,User.userType=='ADMIN').first()
    if not user:
        raise HTTPException(detail={'error':'Only Admin Can Login'},status_code=status.HTTP_404_NOT_FOUND)
    if not verify_password(request.password,user.password):
        raise HTTPException(detail={'error':'Password is not valid'},status_code=status.HTTP_404_NOT_FOUND)
    return user