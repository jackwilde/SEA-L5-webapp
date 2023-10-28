from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from models import User


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


@app.post("/sign-up")
async def sign_up(request: Request,
                  first_name: str = Form(default=None),
                  last_name: str = Form(default=None),
                  email: str = Form(default=None),
                  password1: str = Form(default=None),
                  password2: str = Form(default=None)):

    if password1 != password2:
        error = "Password do not match"
        return templates.TemplateResponse(
            "sign-up.html", {"request": request, "error": error})
    else:
        # TODO test pydantic to see if user friendly errors can be processed
        # TODO check if pydantic can stop null values
        # TODO check what happens if there are multiple errors
        try:
            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password1)
            print(user)
        except ValidationError as e:
            # reason = e.errors()[0]["ctx"]["reason"]
            # # print(e.errors()[0]["loc"][0])
            # print(reason)
            print(e.errors())
            # return RedirectResponse("/sign-up", status_code=303, )
            error = f"shits gone bad"


            return templates.TemplateResponse(
                "sign-up.html", {"request": request, "error": error})

    # return RedirectResponse("/", status_code=303)
