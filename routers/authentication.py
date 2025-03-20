from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from tokenUser import create_access_token
from schemas import Register, Login, LoginView
from database import get_db
from models import User
import re

router = APIRouter(tags=['Authentication'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=Register)
def register(request: Register, db: Session = Depends(get_db)):
    
    try:
        if not all([request.name, request.email, request.mobileNumber, request.password, request.address]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'All fields are required'})

        if db.query(User).filter(User.email == request.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'User with this email already exists'})

        hashed_password = hash_password(request.password)
        
        new_user = User(name=request.name, email=request.email, mobileNumber=request.mobileNumber, password=hashed_password, address=request.address)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_data = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "mobileNumber": new_user.mobileNumber,
            "address": new_user.address,
        }
        return JSONResponse(content={'user': user_data, 'message': 'User registered successfully'})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"error":str(e)})


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginView)
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Invalid email or password'})

    access_token = create_access_token(data={'sub': str(user.id)})

    return {'access_token': access_token, 'user': user}

# ---------------------------------- Admin Login ----------------------------------

@router.post('/admin-login', status_code=status.HTTP_200_OK, response_model=LoginView)
def adminLogin(request: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email, User.userType == 'ADMIN').first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Invalid admin credentials'})

    access_token = create_access_token(data={'sub': str(user.id)})

    return {"access_token": access_token, 'user': user}
