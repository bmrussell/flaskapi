import os

from flask import Flask
from flask_smorest import Api
from flask import jsonify
from db import db
from dotenv import load_dotenv

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from flask_jwt_extended import JWTManager
from resources.user import blp as UserBlueprint
from resources.healthcheck import blp as HealthcheckBlueprint

from blocklist import BLOCKLIST
from flask_migrate import Migrate


def create_app(db_url=None):
    env = os.getenv("ENVIRONMENT")          # Get environment from .env
    # Get environment for this environemt from the file pointed to
    load_dotenv(env)

    app = Flask(__name__)

    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    jwt_key = os.getenv("JWT_SECRET_KEY")                                                                   # Default to environment variable
    if jwt_key == None:
        jwt_key_file = os.getenv("JWT_SECRET_KEY_FILE") or f'.{os.sep}secrets{os.sep}jwt_secret_key.txt'    # or secret in docker secrets file or os secrets file
        with open(jwt_key_file) as f:
            jwt_key = f.readline().strip('\n')
    app.config["JWT_SECRET_KEY"] = jwt_key
    jwt = JWTManager(app)

    # Check for logged out tokens
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # Better to use redis here rather than in memory for app restarts
        return jwt_payload["jti"] in BLOCKLIST

    # Called when fresh token is expected but non-fresh received
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}, 401))

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401)

    # Create JWT Claims
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # identity is from the create_access_token() call in login
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}), 401)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(HealthcheckBlueprint)

    return app
