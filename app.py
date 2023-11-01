from flask import Flask
from blueprint.auth import auth, login_manager
from blueprint.views import views
# from database import db, SQLALCHEMY_DATABASE_URI


# App config
app = Flask(__name__)
app.config["SECRET_KEY"] = \
    "96cc123bfcb413560fead3d228c0773b1cde804b7a9ad924272cc545eaee2d1d"
app.register_blueprint(blueprint=auth, url_prefix="/")
app.register_blueprint(blueprint=views, url_prefix="/")
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
#
# # Database init
# db.init_app(app)


# def create_database():
#     with app.app_context():
#         db.create_all()


login_manager.init_app(app)
