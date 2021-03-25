from flask import Flask
from flask_mongoengine import MongoEngine
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
CORS(app, resources={r"/api2/*": {"origins": "*"}})


import Models.UserLogin
import Models.UserDetails
import Models.SnippetPost
import Routes.AuthRoute
import Routes.PostRoute
import Models.PostLikes
# from hello import urls_blueprint;
# app.register_blueprint(urls_blueprint)

if __name__ == "__main__":
    app.run(debug=True)