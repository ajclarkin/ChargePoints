from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date


username = "ajc"

app = Flask(__name__)
app.config['SECRET_KEY'] = b'3#UZ#lD0AL0yvvtzaqouLCms5zyOq&De$FeY78BC'

# This is where the database stuff is
from models import *




@app.route("/")
def Index():
    points = ChargePoints.query.all()
    return render_template("statusList.html", points=points)
