from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, abort)
from jinja2 import TemplateNotFound
from flask_login import login_required, current_user
from app.models import User
from app.models import db


views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html",
                           user=current_user)