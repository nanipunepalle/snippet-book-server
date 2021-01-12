from flask import Flask
from flask_mongoengine import MongoEngine
import json
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)


import Models.UserLogin
import Routes.AuthRoute
# from hello import urls_blueprint;
# app.register_blueprint(urls_blueprint)

if __name__ == "__main__":
    app.run(debug=True)