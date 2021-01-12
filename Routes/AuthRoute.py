import json
import jwt
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from datetime import datetime

from app import app
from app import db

from Models.UserLogin import UserLogin

bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# route to signup
@app.route('/api/signup', methods=["POST"])
@cross_origin(supports_credentials=True,cross_origin=True)
def user_signup():
    req_data = json.loads(request.data)
    user = UserLogin.objects(email=req_data['email']).first()
    if user:
        return {"message": "User already exists, Please signin"}, 202
    else:
        try:
            hashed_password = bcrypt.generate_password_hash(req_data['password'],app.config["BCRYPT_SALT_ROUNDS"])
            signup_time = datetime.now()
            user = UserLogin(
            name=req_data['name'],
            email=req_data['email'],
            password=hashed_password,
            signup_time=signup_time)
            user.save()
            token = jwt.encode({'public_id':str(user.id)},app.config["SECRET_KEY"])
            user_token = [token]
            UserLogin.objects(email=user.email).update(token=user_token)
            return {"token": token} , 200 
        except Exception as e:
            return {'error': e} , 400


# route to signin
@app.route('/api/signin', methods=["POST"])
def user_signin():
    user = UserLogin.objects(email=request.form.get('email')).first()
    if user:
        if bcrypt.check_password_hash( user.password,request.form.get('password').encode('utf-8')):
            return {"message":"success"}, 200
        else:
            return {"message": "invalid password"}, 201
    return {"message": "User not found"}, 202