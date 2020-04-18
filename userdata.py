from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class userdata(db.Model):
    __tablename__=userdata
    username=db.column(db.String, primary_key=True)
    password=db.column(db.String, nullable=False)
    time=db.column(db.datetime, nullable=False)

    def _init_(self, username, password, time):
        self.username = username
        self.Password = password
        self.time = time