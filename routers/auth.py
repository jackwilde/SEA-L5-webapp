from fastapi import APIRouter
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import Annotated
from validation import validate_sign_up
from models import User
from database import get_db
import crud

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/test")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return crud.get_user_by_email(db, email="")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


@router.post("/sign-in")
async def sign_in(email: str = Form("email"),
                  password: str = Form("password")):
    # TODO check user email and password are correct

    return RedirectResponse("/", status_code=303)


@router.get("/sign-up", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})


@router.post(path="/sign-up", response_class=RedirectResponse)
async def sign_up(db: Annotated[Session, Depends(get_db)],
                  request: Request,
                  first_name: str = Form(default=None),
                  last_name: str = Form(default=None),
                  email: str = Form(default=None),
                  password1: str = Form(default=None),
                  password2: str = Form(default=None)):

    email = email.lower()
    error = validate_sign_up(db=db, first_name=first_name, last_name=last_name,
                             email=email, password1=password1,
                             password2=password2)


    # If any errors detected then display to user
    if error:
        return templates.TemplateResponse(
            "sign-up.html", {"request": request, "error": error})
    # Else create user account
    else:
        user = User(first_name=first_name, last_name=last_name,
                    email=email, password=password1)
        crud.create_user(db=db, user=user)
        # TODO Login user
        return RedirectResponse("/", status_code=303)
