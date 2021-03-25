import json
import jwt
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from datetime import datetime

from app import app
from app import db

from Models.UserLogin import UserLogins
from Models.UserDetails import UserDetails

bcrypt = Bcrypt(app)

@app.route('/api2',methods=["GET"])
def sample_func():
    print("server working")
    return "server working"

# route to signup
@app.route('/api/signup', methods=["POST"])
@cross_origin(supports_credentials=True,cross_origin=True)
def user_signup():
    req_data = json.loads(request.data)
    user = UserLogins.objects(email=req_data['email']).first()
    if user:
        return {"message": "User already exists, Please signin"}, 202
    else:
        try:
            hashed_password = bcrypt.generate_password_hash(req_data['password'],app.config["BCRYPT_SALT_ROUNDS"])
            signup_time = datetime.now()
            user = UserLogins(
            name=req_data['name'],
            email=req_data['email'],
            password=hashed_password,
            signup_time=signup_time)
            user.save()
            token = jwt.encode({'public_id':str(user.id)},app.config["SECRET_KEY"])
            user_token = [token]
            UserLogins.objects(email=user.email).update(token=user_token)
            user_details = UserDetails(
                name = req_data['name'],
                email = req_data['email'],
                user_id = str(user.id),
                verified = False
            )
            user_details.save()
            return {"token": token,"user": user_details} , 200 
        except Exception as e:
            return {'error': e} , 400


# route to signin
@app.route('/api/signin', methods=["POST"])
def user_signin():
    req_data = json.loads(request.data)
    user = UserLogins.objects(email=req_data['email']).first()
    if user:
        if bcrypt.check_password_hash( user.password,req_data['password'].encode('utf-8')):
            token = jwt.encode({'public_id':str(user.id)},app.config["SECRET_KEY"])
            user_token = [token]
            UserLogins.objects(email=user.email).update(push__token=token)
            user_details = UserDetails.objects(email=user.email)
            return {"token":token,"user": user_details}, 200
        else:
            return {"message": "invalid password"}, 201
    return {"message": "User not found"}, 202


# route to get the current user based on token
@app.route('/api/user/me', methods=["GET"])
def get_user():
    token = request.headers.get('Authorization').replace('Bearer ','')
    data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'],token__in=[token]).first()
    if user:
        userDetails = UserDetails.objects(email=user.email).first()
        return jsonify(userDetails),200
    else:
        return {"message": "user_not_found"}, 401

# route to user logout

@app.route('/api/user/logout', methods=["GET"])
def user_logout():
    token = request.headers.get('Authorization').replace('Bearer ','')
    print(token)
    data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'],token__in=[token]).first()
    if user:
        UserLogins.objects(email=user.email).update(pull__token = token)
        return {"message": "success"} , 200
    else:
        return {"message": "not found"}, 401