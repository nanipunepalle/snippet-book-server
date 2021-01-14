import json
import jwt
from flask import Flask, request, jsonify
from mongoengine.queryset.visitor import Q 
from datetime import datetime

from app import app
from app import db

from Models.UserLogin import UserLogins
from Models.UserDetails import UserDetails
from Models.SnippetPost import SnippetPost


@app.route('/api/user/add_snippet', methods=["POST"])
def add_snippet():
    req_data = json.loads(request.data)
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    print(user['name'])
    if user:
        try:
            currentTime = datetime.now()
            snippet = SnippetPost(
                desc=req_data['desc'],
                user_id=str(user.id),
                user_name=user['name'],
                code=req_data['code'],
                language=req_data['lang'],
                frameworks=req_data['frameworks'],
                posted_on=currentTime,
                access_type=req_data['type'])
            snippet.save()
            return {"message": "success"}, 200
        except Exception as e:
            return {"message": e}, 201
    else:
        return {"message": "not found"}, 202


@app.route('/api/get_public_posts', methods=["GET"])
def get_public_posts():
   posts = SnippetPost.objects(access_type="public")
   return jsonify(posts),200

@app.route('/api/get_all_posts', methods=["GET"])
def get_all_posts():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    if user :
        posts = SnippetPost.objects(Q(access_type="public") | Q(user_id=str(user.id)))
        return jsonify(posts), 200
    else:
        return {"message": "not found"}, 201

@app.route('/api/get_your_posts', methods=["GET"])
def get_your_posts():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    if user :
        posts = SnippetPost.objects(user_id=str(user.id))
        return jsonify(posts), 200
    else:
        return {"message": "not found"}, 201