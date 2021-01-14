import json
from flask import Flask, request, jsonify

from app import app
from app import db

# from flask import Blueprint

class SnippetPost(db.Document):
    desc = db.StringField(required=True)
    user_id = db.StringField(required=True)
    user_name = db.StringField()
    access_type = db.StringField()
    language = db.StringField()
    frameworks = db.ListField()
    code = db.StringField()
    verified = db.BooleanField()
    posted_on = db.DateTimeField()
    def to_json(self):
        return {"desc": self.desc,
                "access_type": self.access_type,
                "user_id": self.user_id,
                "language": self.language,
                "frameworks": self.frameworks,
                "code": self.code,
                "verified": self.verified,
                "posted_on": self.posted_on}