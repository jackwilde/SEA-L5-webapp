from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db
from routers import auth

create_db()
# app = FastAPI(openapi_url=None)
app = FastAPI()
app.include_router(auth.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

