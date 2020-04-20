import os
import datetime

from flask import Flask, session,render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from userdata import *


app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password =request.form.get("password")
        time = datetime.now()
        user = userdata(username = name, password = password, time = time)
        db.session.add(user)
        db.session.commit()
        return render_template("data.html", name=name)

@app.route("/admin")
def userdetails():
    user = userdata.query.order_by(userdata.time).all()
    return render_template("userdetails.html", users = user)

@app.route("/auth", methods=["post"])
def login():
    name = request.form.get("username")
    password = request.form.get("password")
    

