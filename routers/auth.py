from fastapi import APIRouter, HTTPException
from fastapi import Request, Form, Depends, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from werkzeug.security import check_password_hash
from fastapi_users import jwt
from datetime import timedelta, datetime
from typing import Annotated, Optional
from validation import validate_sign_up, validate_password
from models import User
from database import get_db
import crud

SECRET_KEY = "191c2dced7280e474a756aab1e84de9b3595a6a8f619740c460d73fb69d9a38f"
ALGORITHM = "HS256"
templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["auth"])

class LoginForm():
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Annotated[dict, Depends(get_current_user)]

def authenticate_user(username: str, password: str,
                      db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_email(email=username, db=db)
    if not user:
        return False
    if not check_password_hash(pwhash=user.password, password=password):
        return False
    return user


def create_access_token(username:str, user_id: int, expires_delta: timedelta):
    data = {"sub": username, "id": user_id}
    expires = datetime.now() + expires_delta
    data.update({"exp": expires})
    return jwt.generate_jwt(data=data, secret=SECRET_KEY, algorithm=ALGORITHM)



# async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
#     payload = jwt.decode_jwt(encoded_jwt=token, secret=SECRET_KEY,
#                              algorithms=[ALGORITHM])
#     username: str = payload.get("sub")
#     user_id: int = payload.get("id")
#     if username is None or user_id is None:
#         return HTTPException(status_code=401,
#                             detail="Could not validate user")
#     return {'username': username, "id": user_id}


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Annotated[Session, Depends(get_db)]):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/sign-up",
                                    status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(
            response=response, form_data=form, db=db)
        if not validate_user_cookie:
            return templates.TemplateResponse("sign-in.html", {"request": request})
        return response
    except HTTPException:
        return templates.TemplateResponse("sign-in.html", {"request": request})


@router.get("/test")
async def read_items(user: Annotated[dict, Depends(get_current_user)],
                     db: Annotated[Session, Depends(get_db)]):
    if user is None:
        return RedirectResponse("/", status_code=401)
    else:
        return user


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


@router.post("/sign-in")
async def sign_in(request: Request,
                  db: Annotated[Session, Depends(get_db)],
                  email: str = Form("email"),
                  password: str = Form("password")):
    result = validate_password(db, email, password)
    if result["status"] == "success":
        # Do the login here
        pass
        return
    else:
        return templates.TemplateResponse("sign-in.html",
                                          {"request": request,
                                           "error": result["message"]})


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


# This might not be needed for gui
@router.post(path="/token")
async def login_for_access_token(response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db=db, password=form_data.password,
                             username=form_data.username)
    if not user:
        return "Failed Authentication"
    else:
        token = create_access_token(user.email, user.id,
                                    expires_delta=timedelta(hours=1))
        response.set_cookie(key="access_token", value=token, httponly=True)
        return True
