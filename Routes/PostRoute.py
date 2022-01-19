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
from Models.PostLikes import PostLikes



@app.route('/api2/user/add_snippet', methods=["POST"])
def add_snippet():
    req_data = json.loads(request.data)
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
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
            posts = SnippetPost.objects(Q(access_type="public") | Q(user_id=str(user.id)))
            return {"message": "success","posts": posts}, 200
        except Exception as e:
            return {"message": e}, 201
    else:
        return {"message": "not found"}, 202

@app.route('/api2/user/edit_snippet', methods=["POST"])
def edit_snippet():
    req_data = json.loads(request.data)
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    post = SnippetPost.objects(id=req_data['post_id']).first()
    if user:
        try:
            if data['public_id'] == post['user_id']:
                SnippetPost.objects(id=req_data['post_id']).update(
                    desc=req_data['desc'],
                    code=req_data['code'],
                    language=req_data['lang'],
                    frameworks=req_data['frameworks'],
                    access_type=req_data['type'])
                posts = SnippetPost.objects(Q(access_type="public") | Q(user_id=str(user.id)))
                return {"message": "success","posts": posts}, 200
            else:
                return {"message": "not authorised"}, 202
        except Exception as e:
            return {"message": e}, 201
    else:
        return {"message": "not found"}, 202

@app.route('/api2/user/delete_snippet', methods=["POST"])
def delete_snippet():
    req_data = json.loads(request.data)
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    post = SnippetPost.objects(id=req_data['post_id']).first()
    if user:
        try:
            if data['public_id'] == post['user_id']:
                SnippetPost.objects(id=req_data['post_id']).delete()
                posts = SnippetPost.objects(Q(access_type="public") | Q(user_id=str(user.id)))
                return {"message": "success","posts": posts}, 200
            else:
                return {"message": "not authorised"}, 202
        except Exception as e:
            return {"message": e}, 201
    else:
        return {"message": "not found"}, 202

@app.route('/api2/get_public_posts', methods=["GET"])
def get_public_posts():
   posts = SnippetPost.objects(access_type="public")
   return jsonify(posts),200

@app.route('/api2/get_all_posts', methods=["GET"])
def get_all_posts():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    if user :
        posts = SnippetPost.objects(Q(access_type="public") | Q(user_id=str(user.id)))
        # user_likes = PostLikes.objects(user_id=str(user.id)).filter().values_list('post_id')
        return jsonify(posts), 200
    else:
        return {"message": "not found"}, 201

#
@app.route('/api2/get_your_posts', methods=["GET"])
def get_your_posts():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    if user :
        posts = SnippetPost.objects(user_id=str(user.id))
        return jsonify(posts), 200
    else:
        return {"message": "not found"}, 201

@app.route('/api2/get_liked_posts', methods=["GET"])
def get_liked_posts():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
    if user :
        user_likes = PostLikes.objects(user_id=str(user.id)).filter().values_list('post_id')
        return jsonify(user_likes), 200
    else:
        return {"message": "not found"}, 201

#getting the particular post with it's id
@app.route('/api2/get_post', methods=["GET"])
def get_post():
    post_id = request.args["id"]
    post = SnippetPost.objects(id=post_id)
    if post:
        return jsonify(post), 200
    else:
        return {"message": "not found"}, 201


#adding like impression to the post
@app.route('/api2/post/add_like', methods=["GET"])
def add_like():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    if token and token != 'null':
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        user = UserLogins.objects(id=data['public_id'], token__in=[token]).first()
        post_id = request.args["id"]
        user_like = PostLikes.objects(post_id=post_id,user_id=data['public_id'])
        if user and not user_like:
            like = PostLikes(user_id=data['public_id'],post_id=post_id)
            like.save()
            likes = PostLikes.objects(post_id=post_id)
            like = PostLikes.objects(post_id=post_id,user_id=data['public_id'])
            SnippetPost.objects(id=post_id).update(likes=len(likes))
            post = SnippetPost.objects(id=post_id).first()
            if like:
                post["liked"] = True
            else:
                post["liked"] = False
            return jsonify(post), 200
        else:
            return {"message": "not found"}, 201
    else:
        return {"message": "not found"}, 201