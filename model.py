import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class books(db.Model):
    __tablename__="books"
    ISBN_number = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    publication_year = db.Column(db.Integer, nullable = False)

    def _init_(self, number, name, author, year):
        self.ISBN_number = number
        self.name = name
        self.author = author
        self.publication_year = year