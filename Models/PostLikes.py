import json
from flask import Flask, request, jsonify

from app import app
from app import db

class PostLikes(db.Document):
    user_id = db.StringField(required=True)
    post_id = db.StringField(required=True)
    def to_json(self):
        return {"post_id": self.post_id,
                "user_id": self.user_id}