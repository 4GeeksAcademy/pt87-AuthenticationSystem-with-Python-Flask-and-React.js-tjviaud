"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import jwt
from datetime import timedelta, datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


SECRET_KEY = "super-secret-key"

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    body = request.json
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        raise APIException("Missing email or password",status_code=400)
    
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        raise APIException("User already exists", status_code=409)
    
    new_user = User(email=email, password=generate_password_hash(password), is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

@api.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.get("email")
    password = body.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
        raise APIException("Bad credentials", status_code=401)
    
    token = create_access_token(identity=str(user.id))

    return jsonify({ "token": token }), 200



@api.route('/token', methods=['GET'])
@jwt_required()
def protected():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)
    return jsonify({"id":user.id, "email": user.email})
