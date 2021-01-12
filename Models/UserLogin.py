import json
from flask import Flask, request, jsonify

from app import app
from app import db

# from flask import Blueprint

class UserLogin(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    token = db.ListField()
    signup_time = db.DateTimeField(required=True)
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
