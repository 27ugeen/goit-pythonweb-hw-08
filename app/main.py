from fastapi import FastAPI
from app.routers import contacts
from app.db import engine
from app.models import Base

app = FastAPI()
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

Base.metadata.create_all(bind=engine)