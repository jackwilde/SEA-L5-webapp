from flask import Blueprint, render_template, request, redirect, url_for, abort
from jinja2 import TemplateNotFound

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
@auth.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email)
        print(password)
        return render_template("sign-in.html")
    else:
        return render_template("sign-in.html")


@auth.route("/sign-up", methods=["GET", "POST"])
def create_account():
    return render_template("sign-up.html")