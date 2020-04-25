import os
import datetime

from flask import Flask, session,render_template, request,flash, redirect, url_for
from flask_session import Session
from flask_humanize import Humanize
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from userdata import *
from Reviewdata import *
from operator import and_

app = Flask(__name__)
humanize = Humanize(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
    return "Welcome to BOOKS"

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

@app.route("/auth", methods =["POST"]) 
def auth():
    uname = request.form.get("username")
    password = request.form.get("password")
    queryres = userdata.query.filter_by(username = uname).first()
    if queryres is not None:
        print(password == queryres.password)
        print(uname == queryres.password)
        if password == queryres.password and uname == queryres.username:
            session["user"] = uname
            return redirect(url_for("userhome"))
        else :
            flash("The entered passowrd of the account doesnot match.")
            return render_template("register.html")
    else:
        flash("Your logging credentials are invalid.")
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return render_template("register.html")

@app.route("/userhome")
def userhome():
    if "user" in session:
        user = session["user"]
        return render_template("home.html")
    else:
        flash("Login with the credentails.")
        return render_template("register.html")

@app.route("/review",methods=["GET", "POST"])
def review():
    rev = True
    reviews = Reviewdata.query.order_by(Reviewdata.time).all()
    username  = session["user"] 
    ISBN = "ISBN"
    if request.method=="GET":
        if Reviewdata.query.filter(and_(Reviewdata.username == username, Reviewdata.ISBN==ISBN)).first():
            return render_template("Reviews.html" ,submitted = reviews,review =rev)

        else:
            rev = False
            return render_template("Reviews.html" ,submitted = reviews,review =rev)


    else:
        
        if Reviewdata.query.filter(and_(Reviewdata.username == username, Reviewdata.ISBN==ISBN)).first():
            return render_template("Reviews.html" ,submitted = reviews,review =rev)
   
        else:
            rev = False
            print(request.form)
            Review = request.form.get("review-text")
            Rating = request.form.get("review-rating")
            time = datetime.now()
            addReview= Reviewdata(username = username, ISBN = ISBN,Review = Review,Rating=Rating,time=time)
            db.session.add(addReview)
            db.session.commit()
            return redirect(url_for("review"))