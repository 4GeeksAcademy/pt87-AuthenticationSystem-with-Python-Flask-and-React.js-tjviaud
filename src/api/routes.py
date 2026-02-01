"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import jwt
from datetime import timedelta, datetime
from api.models import db, User
from api.utils import APIException
from functools import wraps
from api.routes import api

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
    
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

@api.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.get("email")
    password = body.get("password")

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        raise APIException("Bad credentials", status_code=401)
    
    token = jwt.encode({
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({ "token": token }), 200

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            raise APIException("Missing token", status_code=401)
        
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            raise APIException("Invalid token", status_code=401)
    
        return f(*args, **kwargs)

    return wrapper


@api.route('/private', methods=['GET'])
@token_required
def private():
    return jsonify({ "msg": "You are logged in" }), 200