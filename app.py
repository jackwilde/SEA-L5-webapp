from flask import Flask
from blueprint.auth import auth, login_manager
from blueprint.views import views
from blueprint.error import error_pages
from blueprint.admin import admin

# Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = \
    "96cc123bfcb413560fead3d228c0773b1cde804b7a9ad924272cc545eaee2d1d"
app.register_blueprint(blueprint=auth, url_prefix="/")
app.register_blueprint(blueprint=views, url_prefix="/")
app.register_blueprint(blueprint=admin, url_prefix="/admin")
app.register_blueprint(blueprint=error_pages)

# Enable login manager
login_manager.init_app(app)
