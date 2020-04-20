import csv
import os

from flask import Flask, render_template, request
from model import *

app = Flask(__name__)
os.environ["DATABASE_URL"] = "postgres://ymjvjqxehzwaub:aadaba6ce5d972237f60a1343ab28645884515fee52b1d9aea95ab421a14537c@ec2-18-210-51-239.compute-1.amazonaws.com:5432/dbuaf71hle517p"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    firstline = True
    f = open("books.csv")
    reader = csv.reader(f)
    for number, name, author, year in reader:
        if firstline:
            firstline = False
            continue
        print(number)
        years = int(year)
        number = str(number)
        book = books(ISBN_number = number, name = name, author = author, publication_year = years)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
