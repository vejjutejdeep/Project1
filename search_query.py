from flask import (Flask, flash, redirect, render_template, request, session,url_for, jsonify)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from Reviewdata import *
from userdata import *
import string


def query(info):
    searchque = string.capwords(info)
    searchque="%{}%".format(searchque)
    ISBN = books.query.filter(books.ISBN_number.like(searchque)).all()
    usname = books.query.filter(books.name.like(searchque)).all()
    authorw = books.query.filter(books.author.like(searchque)).all()
    result = list(set(ISBN + usname + authorw))
    return result