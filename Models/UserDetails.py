import json
from flask import Flask, request, jsonify

from app import app
from app import db

# from flask import Blueprint

class UserDetails(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True)
    user_id = db.StringField(required=True)
    profile_pic = db.StringField()
    bio = db.StringField()
    verified = db.BooleanField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email,
                "user_id": self.user_id}















# @app.route('/add', methods=['POST'])
# def add_user():
#     user = User(name=request.form.get('name'),
#                 email=request.form.get('email'))
#     try:
#         user.save()
#     except :
#         return "error"
    
#     return user.to_json()

# @app.route('/get', methods=["GET"])
# def get_user():
#     user = User.objects(email="lalith@gmail.com")
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         return user.to_json()