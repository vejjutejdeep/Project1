import os

from flask import Flask, render_template, request
from userdata import *

app = Flask(__name__)
os.environ["DATABASE_URL"] = "postgres://ymjvjqxehzwaub:aadaba6ce5d972237f60a1343ab28645884515fee52b1d9aea95ab421a14537c@ec2-18-210-51-239.compute-1.amazonaws.com:5432/dbuaf71hle517p"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()