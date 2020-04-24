import os
import datetime

from flask import Flask, session,render_template, request,flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from userdata import *
from model import *


app = Flask(__name__)
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
    return "Project 1: TODO"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password =request.form.get("password")
        time = datetime.now()
        if name == "":
            flash("please enter the deaitls to register.")
            return redirect(url_for("register"))
        queryres = userdata.query.filter_by(username = name).first()
        if queryres is None:
            user = userdata(username = name, password = password, time = time)
            db.session.add(user)
            db.session.commit()
            session["user"] = name
            return redirect(url_for(userhome))
        else:
            flash("The user is already registered")
            return redirect(url_for("register"))

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
        if password == queryres.password and uname == queryres.username:
            session["user"] = uname
            return redirect(url_for("userhome"))
        else :
            flash("The entered passowrd of the account doesnot match.")
            return redirect(url_for("register"))
    else:
        flash("Your logging credentials are invalid.")
        return redirect(url_for("register"))

@app.route("/logout")
def logout():
    session.pop("user",None)
    flash("You are logout.")
    return redirect(url_for("register"))

@app.route("/userhome")
def userhome():
    if "user" in session:
        user = session["user"]
        booksn = books.query.all()
        return render_template("home.html", books = booksn )
    else:
        flash("Login with the credentails.")
        return redirect(url_for("register"))
# This is the function for Book page
@app.route('/book_page/<string:ISBN_number>', methods=["GET"])
def book_page(ISBN_number):
    if (ISBN_number == None):
        flash("Invalid ISBN Number")
        return render_template("book_page.html", books=None)
    else:
        if ISBN_number is None:
            return None
        else:
            book = books.query.filter_by(ISBN_number=ISBN_number).all()
            b = book[0]
            if b is None:
                flash("Invalid ISBN Number")
                return render_template("book_page.html", b=None)
            else:
                return render_template("book_page.html", b=b)
