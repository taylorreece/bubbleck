from flask import Blueprint
from mat import user

routes_user = Blueprint('routes_user', __name__)

@routes_user.route("/login")
def route_login():
	return 'whatever'
