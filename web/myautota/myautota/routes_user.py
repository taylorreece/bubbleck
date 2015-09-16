from flask import Blueprint

routes_user = Blueprint('routes_user', __name__)

@routes_user.route("/login")
def route_login():
    return "Log in page!"
