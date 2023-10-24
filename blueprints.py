from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

blueprints = Blueprint("blueprints", __name__,
                       template_folder="./templates")

@blueprints.route("/")
def login():
    return render_template("login.html")