from fastapi import FastAPI
import uvicorn
from database import engine
from models import Base

app = FastAPI()

Base.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)