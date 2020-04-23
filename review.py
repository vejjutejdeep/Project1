from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Reviewdata(db.Model):
    __tablename__="Reviews"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    ISBN = db.Column(db.String, nullable=True)
    Review = db.Column(db.String,nullable=False)
    Rating = db.Column(db.Integer,nullable=True)
    time = db.Column(db.DateTime, nullable=False)

    def _init_(self,id, username, ISBN,Review,Rating, time):
        self.id = id
        self.username = username
        self.ISBN = ISBN
        self.Review = Review
        self.Rating = Rating
        self.time = time