from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
