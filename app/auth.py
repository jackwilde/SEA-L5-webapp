from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, abort)
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.validation import validate_email, check_password_strength
from app.models import User
from app.models import db
from app.views import views

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(message="Sign in successful!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash(message="Incorrect password", category="error")
        else:
            flash(message="Email does not exist", category="error")

        return render_template("sign-in.html")
    else:
        return render_template("sign-in.html",
                               user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email").lower()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash(message=f"Account already exists for {email}",
                  category="error")
        elif not first_name:
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
            db.session.add(new_user)
            db.session.commit()

            flash(message="Account created!",
                  category="success")

            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)


            return redirect(url_for("views.home"))
            # return redirect(url_for("auth.sign_in"))

    return render_template("sign-up.html",
                           user=current_user)


@auth.route("/sign-out")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("auth.sign_in"))

