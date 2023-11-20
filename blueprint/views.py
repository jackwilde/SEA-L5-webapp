from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import crud

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html",
                           user=current_user)


@views.route("/training")
@login_required
def training():
    return redirect(url_for("views.view_training"))


@views.route("/training/view", methods=["GET", "POST"])
@login_required
def view_training():
    if request.method == "POST":
        course_name = request.form.get("course_name")
        course_category = request.form.get("category")
        date_completed = request.form.get("date_completed")
        certification = request.form.get("certification")
        training_id = request.form.get("training_id")
        if certification == "True":
            certification = True
        else:
            certification = False
        crud.update_training(training_id=training_id,
                             user_id=current_user.id,
                             course_name=course_name,
                             course_category=course_category,
                             date_completed=date_completed,
                             certification=certification)
        return redirect(url_for("views.view_training"))
    else:
        user_training = crud.get_training_by_user(current_user)
        return render_template("view_training.html",
                               training=user_training,
                               categories=crud.get_training_categories())


@views.route("/training/add", methods=["GET", "POST"])
@login_required
def add_training():
    if request.method == "POST":
        course_name = request.form.get("course_name")
        course_category = request.form.get("category")
        date_completed = request.form.get("date_completed")
        certification = request.form.get("certification")
        if certification == "True":
            certification = True
        else:
            certification = False

        crud.create_training(user_id=current_user.id,
                             course_name=course_name,
                             course_category=course_category,
                             date_completed=date_completed,
                             certification=certification)

        return redirect(url_for("views.view_training"))
    else:
        return render_template("add_training.html",
                               categories=crud.get_training_categories())
