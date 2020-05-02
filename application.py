import datetime
import os
import string
from operator import and_

from flask import (Flask, flash, redirect, render_template, request, session,url_for, jsonify)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import json
from flask_humanize import Humanize
from model import *
from Reviewdata import *
from userdata import *
import search_query
# from flask.json import jsonify

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
        print(password == queryres.password)
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
        booksn = books.query.all()
        return render_template("home.html", books = booksn)   
    else:
        flash("Login with the credentails.")
        return render_template("register.html")

@app.route("/review/<ISBN>",methods=["GET", "POST"])
def review(ISBN):
    username  = session["user"] 
    print(request.form)
    Review = request.form.get("review-text")
    Rating = request.form.get("review-rating")
    time = datetime.now()
    try:
        addReview= Reviewdata(username = username, ISBN = ISBN,Review = Review,Rating=Rating,time=time)
        db.session.add(addReview)
        db.session.commit()
        return redirect(url_for("book_page",ISBN_number = ISBN))
    except:
        flash("Something went wrong while adding the review ")
        return redirect(url_for("book_page",ISBN_number = ISBN))

@app.route('/book_page/<string:ISBN_number>', methods=["GET"])
def book_page(ISBN_number):
    if (ISBN_number is None or len(ISBN_number) == 0):
        flash("Invalid ISBN Number")
        return render_template("book_page.html", b=None)
    else:
        book = books.query.filter_by(ISBN_number=ISBN_number).all()
        b = book[0]
        if b is None:
            flash("Invalid ISBN Number")
            return render_template("book_page.html", b=None)
        else:
            rev = True
            ISBN = ISBN_number
            reviews = Reviewdata.query.filter(Reviewdata.ISBN == ISBN).all()
            username  = session["user"] 
            
            if Reviewdata.query.filter(and_(Reviewdata.username == username, Reviewdata.ISBN==ISBN)).first():
                 return render_template("book_page.html" ,submitted = reviews,review =rev,b = b)
            else:
                rev = False
                return render_template("book_page.html" ,submitted = reviews,review =rev,b = b)

@app.route("/search", methods = ["POST"])
def search():
    tag=request.form.get("search")
    tag = string.capwords(tag)
    if tag != "":
        searchque="%{}%".format(tag)
        ISBN = books.query.filter(books.ISBN_number.like(searchque)).all()
        usname = books.query.filter(books.name.like(searchque)).all()
        authorw = books.query.filter(books.author.like(searchque)).all()
        result = list(set(ISBN + usname + authorw))
        print(len(result))
        if len(result) == 0:
            flash("The searched book does not exists.")
            return render_template("home.html", books = [])
        else:
            return render_template("home.html", books = result)
    else:
        flash("Fill the search details before the clicking on search")
        return redirect(url_for("userhome"))


@app.route("/api/search", methods = ["POST"])
def apisearch():
    try:
        serach_request = request.get_json()
        if 'query' in serach_request:
            # print(serach_request)
            info = serach_request.get("query")
            if len(info) == 0:
                return jsonify({"result":"no such result found"})
            result = search_query.query(info)
            dbooks = {"books" : []}
            print(len(result))
            for each in result:
                d  = dict()
                d["isbn"] = each.ISBN_number
                d["name"] = each.name
                d["author"] = each.author
                d["year"] = each.publication_year
                dbooks["books"].append(d)
            return jsonify(dbooks)
        return  jsonify({"result":"no such result found"}, 400)
    except:
        return (jsonify({"Error":"Unexpected failure"}),500)