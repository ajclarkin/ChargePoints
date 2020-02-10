from flask_sqlalchemy import SQLAlchemy
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # added cause it keeos warning me
db = SQLAlchemy(app)


class ChargePoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    point = db.Column(db.Integer)
    connector = db.Column(db.Integer)
    type = db.Column(db.String(30))

    # This allows us to print the output of a query
    def __repr__(self):
        #return f'{self.id} {self.name} {self.point} {self.connector} {self.type}'
        return "{} {} {} {} {}".format(self.id, self.name, self.point, self.connector, self.type)



db.create_all()
