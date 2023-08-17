import requests
import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt, get_jti
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST
from sqlalchemy import or_
from utils import getenv

blp = Blueprint("Users", __name__, description="Operations on users")


def send_simple_message(to, subject, body):
    domain = getenv("MAILGUN_DOMAIN")
    key = getenv("MAILGUN_API_KEY")

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", key),
        data={"from": f"App <mailgun@{domain}>",
              "to": [to],
              "subject": subject,
              "text": body})


@blp.route("/refresh")
class TokenRefresh(MethodView):
    # refresh=True means it needs a refresh token not an acces token
    @jwt_required(refresh=True)
    def post(self):
        # Create a refresh token for non-critial opertions so the user can stay logged in
        # Demand a fresh token on critical stuff like delete account
        current_user = get_jwt_identity()
        # # >> can add jti to blocklist to only issue one refresh token then next call here would fail
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Succesfully logged out."}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            acces_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": acces_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"]
                )).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        send_simple_message(to=user.email, subject="Signed up",
                            body=f"Hi {user.username}. You've signed up.")

        return {"message": "User created successfully."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
