from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kyle/projects/Thesis/SSS.db'
db = SQLAlchemy(app)

class VehicleTypes(db.Model):
    __tablename__ = "vehicle_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Homeowners(db.Model):
    __tablename__ = "homeowners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    plate_number = db.Column(db.String, nullable=False)
    conduction_number = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.String, nullable=False)
    vehicle_type = db.Column(db.Integer, db.ForeignKey("vehicle_types.id"), nullable=False)
    model = db.Column(db.String, nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False)

class Logs(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    image_path = db.Column(db.String, nullable=False)
    entrance = db.Column(db.Boolean, nullable=False)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

