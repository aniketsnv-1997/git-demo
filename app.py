# Third Party Library Imports
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Dependency Imports
from database import db

# Imports from user related Resources
from resources.users.User import Users, SingleUser
from resources.users.Projects import Projects, SingleProject
from resources.users.Rights import Rights, SingleRight
from resources.users.Types import Types, SingleType
from resources.users.Roles import Roles, SingleRole
from resources.users.User import Users, SingleUser

# Imports from donor related Resources
from resources.donors.Donors import Donors, SingleDonor
from resources.donors.References import Reference, SingleReference
from resources.donors.States import State, SingleState
from resources.donors.Country import Country, SingleCountry

from models.users.UsersModel import UsersModel
from security import UserLogin, TokenRefresh

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # This line enables the Flask app to identify errors and exceptions
# related to Flask-JWT and then report them accordingly
app.secret_key = 'aniket'
app.config['JWT_SECRET_KEY'] = 'aniket'
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Used to add some more values to the access JWT token
    # TODO: Generalizing the if condition to a database query to fetch id by username
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

# When JWT token sent by user to server is expired (a JWT token expired after 5 minutes)
@jwt.expired_token_loader()
def expired_token_callback():
    return jsonify({
            "message": "The token has expired",
            "error": "token_expired"
        }), 401

# When JWT token sent by user to server is not a valid token
@jwt.invalid_token_loader()
def invalid_token_callback():
    return jsonify({
        "message": "Identity verification failed",
        "error": "token_invalid"
    })

# When the user does not send any token to the server
@jwt.unauthorized_loader()
def no_token_callback():
    return jsonify({
        "message": "No token provided",
        "error": "no_token_received"
    })

# When the server needs a fresh token
@jwt.needs_fresh_token_loader()
def no_fresh_token_callback():
    return jsonify({
        "message": "Send a fresh token",
        "error": "fresh_token_required"
    })

# When the server gets a revoked token from user, used in case of logouts
@jwt.revoked_token_loader()
def revoked_token_callback():
    return jsonify({
        "message": "You have been logged out from the system",
        "error": "revoked_token"
    })


api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<string:name>')
api.add_resource(Projects, '/projects')
api.add_resource(SingleProject, '/projects/<string:name>')
api.add_resource(Roles, '/roles')
api.add_resource(SingleRole, '/roles/<string:name>')
api.add_resource(Rights, '/rights')
api.add_resource(SingleRight, '/rights/<string:name>')
api.add_resource(Types, '/types')
api.add_resource(SingleType, '/types/<string:name>')
api.add_resource(Country, '/country')
api.add_resource(SingleCountry, '/country/<string:name>')
api.add_resource(Reference, '/references')
api.add_resource(SingleReference, '/references/<string:name>')
api.add_resource(State, '/states')
api.add_resource(SingleState, '/states/<string:name>')
api.add_resource(Donors, '/donors')
api.add_resource(SingleDonor, '/donors/<string:name>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    app.run()
