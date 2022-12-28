
import os


from flask import Flask, jsonify
from flask_smorest import Api

from app.blocklist import BLOCKLIST
from app.resources.item import blp as ItemBlueprint
from app.resources.store import blp as StoreBlueprint
from app.resources.tag import blp as TagBlueprint
from app.resources.user import blp as UserBlueprint
from app.db import db


from flask_jwt_extended import JWTManager


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

    # used for signing the jwt
    # JWT extended is not working. or may be depricated
    # app.config['JWT_EXTENDED_KEY'] = "test"
    app.config['JWT_SECRET_KEY'] = "195060783362593048056456918259598665565"
    jwt = JWTManager(app)

    # add token in block list
    @jwt.token_in_blocklist_loader
    def checks_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # return error message when revoked token is used
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"desciption":"Token has been revoked", "error":"token_revoked"}
            ),
            401
        )
    
    # add claims to a jwt token/ more inforamtion for an api
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):

        # look in databse see weather user is admin or not
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}


    # called when token is invalid
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message": "Signature verification failed", "error": "invalid_token"}),
            401
        )

    # called when token is expired
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired", "error": "expired_token"}),
            401
        )

    # called when token is missing
    @jwt.unauthorized_loader
    def expired_token_callback(error):
        return(
            jsonify({"description": "Request does not contain an access token", "error": "authorization_required"}),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_paylod):
        return{
            jsonify(
                {
                    "description":"Token is not fresh",
                    "error":"fresh_token_required"
                }
            )
        }

    

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app