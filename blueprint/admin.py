from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from validation import validate_sign_up, validate_password
import crud

admin = Blueprint("admin", __name__)


@admin.route("/users", methods=["GET", "POST"])
@login_required
def admin_users():
    if not current_user.admin:
        return render_template("error_pages/403.html"), 403
    elif request.method == "POST":
        # If Add new user clicked
        if request.form.get("form_id") == "add-user":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email").lower()
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            is_admin = request.form.get("admin")
            if is_admin == "True":
                is_admin = True
            else:
                is_admin = False
            request.form.get("admin")
            error = validate_sign_up(
                first_name, last_name, email, password1, password2
            )
            if error:
                flash(message=error, category="error")
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
            if is_admin == "True":
                is_admin = True
            else:
                is_admin = False
            if current_user.id == user_id and is_admin != current_user.admin:
                flash(message="You cannot remove admin from yourself",
                      category="error")
                return redirect(url_for("admin.admin_users"))
            else:
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
        else:
            print(request.form.get("form_id"))
            return redirect(url_for("admin.admin_users"))
    else:
        all_users = crud.get_all_users()
        return render_template("admin_users.html", all_users=all_users,
                               current_user=current_user)


@admin.route("/training")
@login_required
def admin_training():
    if not current_user.admin:
        return render_template("error_pages/403.html"), 403
    return render_template("admin_training.html", user=current_user)


@admin.route("/categories")
@login_required
def admin_categories():
    if not current_user.admin:
        return render_template("error_pages/403.html"), 403
    all_categories = crud.get_training_categories()
    return render_template("admin_categories.html", user=current_user,
                           all_categories=all_categories)
