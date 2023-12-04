from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
import crud

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def training():
    if request.method == "POST":
        if request.form.get("form_id") == "add_training":
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
            return redirect(url_for("views.training"))
        else:
            course_name = request.form.get("course_name")
            course_category = request.form.get("category")
            date_completed = request.form.get("date_completed")
            certification = request.form.get("certification")
            training_id = request.form.get("training_id")
            if certification == "True":
                certification = True
            else:
                certification = False
            # Check existing training record belongs to current user
            training_record = crud.get_training_by_id(training_id)
            if training_record.user_id == current_user.id:
                crud.update_training(training_id=training_id,
                                     course_name=course_name,
                                     course_category=course_category,
                                     date_completed=date_completed,
                                     certification=certification)
                return redirect(url_for("views.training"))
            else:
                return abort(403)
    else:
        user_training = crud.get_training_by_user(current_user)
        return render_template("training.html",
                               training=user_training,
                               all_categories=crud.get_training_categories(),
                               user=current_user)
