from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))