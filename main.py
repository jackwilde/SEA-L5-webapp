from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from validation import validate_sign_up
from ux import display_alert
from sqlalchemy.orm import Session

import crud, models
from database import SessionLocal, engine

# Create DB
models.Base.metadata.create_all(bind=engine)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


@app.post("/sign-in")
async def sign_in(email: str = Form("email"),
                  password: str = Form("password")):
    # TODO check user email and password are correct

    return RedirectResponse("/", status_code=303)


@app.get("/sign-up", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/sign-up", response_class=RedirectResponse)
async def sign_up(request: Request,
                  first_name: str = Form(default=None),
                  last_name: str = Form(default=None),
                  email: str = Form(default=None),
                  password1: str = Form(default=None),
                  password2: str = Form(default=None)):


    error = validate_sign_up(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             password1=password1,
                             password2=password2)
    if error:
        return templates.TemplateResponse(
            "sign-up.html", {"request": request, "error": error})
    else:
        return RedirectResponse("/home", status_code=303)
