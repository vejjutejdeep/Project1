import csv
import os

from flask import Flask, render_template, request
from model import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for number, name, author, year in reader:
        book = books(number = number, name = name, author = author, year = year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
