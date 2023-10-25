from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, abort)
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from app.validation import validate_email, check_password_strength
from app.models import User
from app.models import db
from sqlalchemy.exc import IntegrityError

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
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        print(first_name)
        print(last_name)
        print(email)
        print(password1)
        print(password2)

        if not first_name:
            flash(message="First name is required",
                  category="error")
        elif not last_name:
            flash(message="First name is required",
                  category="error")
        elif not validate_email(email):
            flash(message="Email address format is invalid",
                  category="error")
        elif password1 != password2:
            flash(message="Passwords do not match",
                  category="error")
        elif not check_password_strength(password1):
            print("I'm here")
            flash(message="Passwords must be at least 12 characters long and "
                          "contain at least 1 letter, 1 number, 1 special "
                          "character and no spaces.",
                  category="error")
        else:
            password_hash = generate_password_hash(password1)
            new_user = User(first_name=first_name, last_name=last_name,
                            email=email, password=password_hash)
            try:
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError as e:
                # TODO Make this check better
                print("Probably a duplicate email")
            flash(message="Account created!",
                  category="success")
            return redirect(url_for("auth.sign_in"))

    return render_template("sign-up.html")