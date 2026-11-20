from fastapi import FastAPI

from piazza_app.database import Base, engine
from piazza_app import models
from piazza_app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
