from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import crud

admin = Blueprint("admin", __name__)


@admin.route("/")
@login_required
def admin_dashboard():
    if not current_user.admin:
        return render_template("error_pages/403.html"), 403
    return render_template("admin_dashboard.html", user=current_user)


@admin.route("/users", methods=["GET", "POST"])
@login_required
def admin_users():
    if not current_user.admin:
        return render_template("error_pages/403.html"), 403
    elif request.method == "POST":
        print(request.from_values())
        return redirect(url_for("admin.admin_users"))

    else:
        all_users = crud.get_all_users()
        return render_template("admin_users.html",
                               all_users=all_users, current_user=current_user)


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
    return render_template("admin_categories.html", user=current_user)
