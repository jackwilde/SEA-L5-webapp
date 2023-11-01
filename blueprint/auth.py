from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash)
from flask_login import (login_user, login_required, logout_user, current_user,
                         LoginManager)
import crud
from validation import validate_sign_up, validate_password
from models import User

auth = Blueprint("auth", __name__)

# Login Manager config
login_manager = LoginManager()
login_manager.login_view = "auth.sign_in"


@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    elif request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        user = validate_password(email=email, password=password)
        if user:
            flash(message="Sign in successful!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
        else:
            flash(message="Email or password incorrect", category="error")
        return render_template("sign-in.html")
    else:
        return render_template("sign-in.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email").lower()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        error = validate_sign_up(first_name, last_name, email, password1,
                                 password2)
        if error:
            flash(message=error, category="error")
        else:
            user = crud.create_user(first_name=first_name, last_name=last_name,
                                    email=email, password=password1)
            login_user(user, remember=True)

            return redirect(url_for("views.home"))

    return render_template("sign-up.html",
                           user=current_user)


@auth.route("/sign-out")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("auth.sign_in"))
