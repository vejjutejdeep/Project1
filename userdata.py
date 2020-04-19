from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class userdata(db.Model):
    __tablename__="userdata"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def _init_(self, username, password, time):
        self.username = username
        self.Password = password
        self.time = time