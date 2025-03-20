from fastapi import FastAPI
import uvicorn
from database import engine
from models import Base
from routers import authentication,admin

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(admin.router)

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)