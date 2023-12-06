from flask import Blueprint, render_template
from crud import ALL_CATEGORIES
error_pages = Blueprint("error_pages", __name__)


@error_pages.app_errorhandler(404)
def error_404():
    return render_template("error_pages/404.html",
                           all_categories=ALL_CATEGORIES), 404


@error_pages.app_errorhandler(403)
def error_403():
    return render_template("error_pages/403.html",
                           all_categories=ALL_CATEGORIES), 403
