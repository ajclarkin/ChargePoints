from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func
# from datetime import date

# This next section is required for getting the API data
import json
from urllib.request import urlopen



username = "ajc"

app = Flask(__name__)
app.config['SECRET_KEY'] = b'3#UZ#lD0AL0yvvtzaqouLCms5zyOq&De$FeY78BC'

# This is where the database stuff is
from models import *


def CheckChargePointStatus(point, connector):
    url = 'https://map.chargeplacescotland.org/status?bayNo=' + str(point) + '&connectorId=' + str(connector)
    with urlopen(url) as response:
        for line in response:
            ret = json.loads(line)
            status = ret["status"]
    
        if status == "Available":
            return 1
        else:
            return 0



@app.route("/")
def Index():
    points = ChargePoints.query.order_by(ChargePoints.name).all()
    
    for i in points:
        i.status = CheckChargePointStatus(i.point, i.connector)

    return render_template("statusList.html", points=points)
