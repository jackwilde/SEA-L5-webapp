from flask import (Blueprint, render_template, redirect, url_for, request,
                   flash, abort)
from flask_login import login_required, current_user
from validation import (validate_sign_up, convert_to_int, check_date_is_past,
                        validate_user_info, validate_training)
import crud

admin = Blueprint("admin", __name__)

ALL_CATEGORIES = crud.ALL_CATEGORIES


def check_admin(user):
    if not user.admin:
        abort(403)


@admin.route("/users", methods=["GET", "POST"])
@login_required
def admin_users():
    check_admin(current_user)
    if request.method == "POST":
        # If Add new user clicked
        if request.form.get("form_id") == "add-user":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email").lower()
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            is_admin = request.form.get("admin")
            request.form.get("admin")
            result = validate_sign_up(
                first_name, last_name, email, password1, password2
            )
            if result != 0:
                flash(message=result, category="error")
            else:
                crud.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                    admin=is_admin
                )
            return redirect(url_for("admin.admin_users"))
        # If Add edit user clicked
        elif request.form.get("form_id").startswith("edit"):
            user_id = int(request.form.get("user_id"))
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email").lower()
            is_admin = request.form.get("admin")
            if current_user.id == user_id and is_admin != current_user.admin:
                flash(message="You cannot remove admin from yourself",
                      category="error")
                return redirect(url_for("admin.admin_users"))
            else:
                result = validate_user_info(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                if result != 0:
                    flash(message=result,
                          category="error")
                    return redirect(url_for("admin.admin_users"))
                crud.update_user(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    admin=is_admin
                )
                return redirect(url_for("admin.admin_users"))
        # If Add delete user clicked
        elif request.form.get("form_id").startswith("delete"):
            user_to_delete = int(request.form.get("user_id"))
            if current_user.id == user_to_delete:
                flash(message="Admin users cannot delete themselves",
                      category="error")
            else:
                crud.delete_user(user_id=user_to_delete)
            return redirect(url_for("admin.admin_users"))
        # If Add view user clicked
        elif request.form.get("form_id").startswith("view"):
            user_id = request.form.get("user_id")
            return redirect(url_for("admin.admin_training", user=user_id))
        else:
            print(request.form.get("form_id"))
            return redirect(url_for("admin.admin_users"))
    else:
        all_users = crud.get_all_users()
        return render_template("admin_users.html", all_users=all_users,
                               current_user=current_user,
                               all_categories=ALL_CATEGORIES)


@admin.route("/training", methods=["GET", "POST"])
@login_required
def admin_training():
    check_admin(current_user)
    user_id = request.args.get("user")
    if request.method == "POST":
        if request.form.get("form_id").startswith("delete"):
            crud.delete_training(request.form.get("training_id"))
        # If post with edit form
        if request.form.get("form_id").startswith("edit"):
            training_id = request.form.get("training_id")
            course_name = request.form.get("course_name")
            course_category = request.form.get("category")
            date_completed = request.form.get("date_completed")
            certification = request.form.get("certification")
            # Validate training form
            result = validate_training(
                course_name=course_name,
                date_completed=date_completed
            )
            if result != 0:
                flash(message=result, category="error")
            else:
                crud.update_training(
                    training_id=training_id,
                    course_name=course_name,
                    course_category=course_category,
                    date_completed=date_completed,
                    certification=certification
                )
        # If post with add user
        elif request.form.get("form_id").startswith("add") and user_id:
            course_name = request.form.get("course_name")
            course_category = request.form.get("category")
            date_completed = request.form.get("date_completed")
            certification = request.form.get("certification")
            # Validate training form
            result = validate_training(
                course_name=course_name,
                date_completed=date_completed
            )
            if result != 0:
                flash(message=result, category="error")
            else:
                crud.create_training(user_id=user_id,
                                     course_name=course_name,
                                     course_category=course_category,
                                     date_completed=date_completed,
                                     certification=certification)
        # Check whether to return all users or specific user
        if user_id:
            return redirect(url_for("admin.admin_training", user=user_id))
        else:
            return redirect(url_for("admin.admin_training"))
    # If a user id set then show training for that user
    elif user_id:
        user_id = int(user_id)
        user = crud.get_user_by_id(user_id)
        user_training = crud.get_training_by_user(user)
        return render_template("admin_training.html", training=user_training,
                               all_categories=ALL_CATEGORIES, user=user)
    # Otherwise show all training
    else:
        all_training = crud.get_all_training()
        return render_template("admin_training.html", training=all_training,
                               all_categories=ALL_CATEGORIES)


@admin.route("/category", methods=["GET", "POST"])
@login_required
def admin_categories():
    check_admin(current_user)
    category_id = request.args.get("id")
    category_id = convert_to_int(category_id)
    if not category_id:
        abort(404)
    category = crud.get_training_category(category_id)
    if not category:
        abort(404)
    if request.method == "POST":
        # Delete training
        if request.form.get("form_id").startswith("delete"):
            crud.delete_training(request.form.get("training_id"))
        if request.form.get("form_id").startswith("edit"):
            training_id = request.form.get("training_id")
            course_name = request.form.get("course_name")
            course_category = request.form.get("category")
            date_completed = request.form.get("date_completed")
            certification = request.form.get("certification")
            # Validate training form
            result = validate_training(
                course_name=course_name,
                date_completed=date_completed
            )
            if result != 0:
                flash(message=result, category="error")
            else:
                crud.update_training(
                    training_id=training_id,
                    course_name=course_name,
                    course_category=course_category,
                    date_completed=date_completed,
                    certification=certification
                )
        return redirect(url_for("admin.admin_categories", id=category_id))
    else:
        training = crud.get_training_by_category(category_id)
        return render_template("admin_category.html",
                               category=category.category_name,
                               training=training,
                               all_categories=ALL_CATEGORIES)
