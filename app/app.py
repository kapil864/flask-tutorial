
import os
from flask import Flask
from flask_smorest import Api
from app.resources.item import blp as ItemBlueprint
from app.resources.store import blp as StoreBlueprint
from app.resources.tag import blp as TagBlueprint
from app.db import db
from app.models.item import ItemModel
from app.models.store import StoreModel


def create_app(db_url = None):
    app = Flask(__name__)

    app.config["PRPOPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")  # use the DATABASE_URL environment variable
    app.config["SQLALCHEMT_TRACK_MODIFICATION"] = False

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app