from fastapi import APIRouter,Depends   
from sqlalchemy.orm import Session
from schemas import Register
from database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/register')
def register(request:Register,db:Session=Depends(get_db)):
    pass