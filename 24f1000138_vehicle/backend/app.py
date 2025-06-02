from flask import Flask, render_template, redirect, url_for, request, flash,session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime, timedelta,date
import calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy.sql import func
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)

base_dir=os.path.dirname(os.path.abspath(__file__))
static_dir=os.path.join(base_dir,'static')

class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(30),unique=True, nullable=False)
    password=db.Column(db.String(15),unique=True,nullable=False)
    addr=db.Column(db.String(200), nullable=False)
    pin=db.column(db.String(6), nullable=False)
    admin=db.Column(db.Boolean, nullable=False, default=False)
    scores = db.relationship("Score", backref='user', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(30),unique=True, nullable=False)
    password=db.Column(db.String(15),unique=True,nullable=False)
    admin=db.Column(db.Boolean, nullable=False, default=True)

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    lot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price= db.Column(db.Integer, nullable=False)
    address= db.Column(db.String(200), nullable=False)
    pinc= db.Column(db.String(6), nullable=False)
    num=db.Column(db.Integer, nullable=False)
    spots= db.relationship("ParkingSpot", backref='parking_lot', lazy=True)

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    spot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id'), nullable=False)
    status=db.Colum(db.String(1), nullable=False)  # 'A' for available, 'O' for occupied

class ReserveParkingSpot(db.Model):
    __tablename__ = 'rparking_spot'
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.spot_id'), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    cost= db.Column(db.Integer, nullable=False)

@app.before_request
def create_tables():
    db.create_all()
    if not Admin.query.filter_by(email="Admin01@gmail.com").first():
        admin=Admin(name="Admin", email="Admin01@gmail.com", password=generate_password_hash("Taara4590$"))
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/clear_flash_messages', methods=['POST'])
def clear_flash_messages():
    session.pop('_flashes', None) 
    return '', 204 

@app.route('/register', methods=['GET', 'POST'])
def register():
    data=request.get_json()
    n=data.get('name')
    e=data.get('email')
    p=data.get('password')
    a=data.get('addr')
    pin=data.get('pin')
    if not e or not p or not n or not a or not pin:
        return jsonify({'msg': 'All fields are required'}), 400
    else:
        e_user=User.query.filter_by(email=e).first()
        if e_user:
            return jsonify({'msg': 'User already exists'}), 409
        else:
            h_pwd=generate_password_hash(p)
            new=User(name=n, email=e, password=h_pwd,addr=a,pin=pin)
            try:
                db.session.add(new)
                db.session.commit()
                return jsonify({'msg': 'Registration successful'}), 201 
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    e = data.get('email')
    p = data.get('password')

    if not e or not p:
        return jsonify({'msg': 'Email and Password are required'}), 400

    user = User.query.filter_by(email=e).first()
    if user and check_password_hash(user.password, p):
        access_token = create_access_token(identity={'u_id': user.u_id, 'admin': user.admin})
        return jsonify({
            'access_token': access_token,
            'admin': user.admin,
            'msg': 'Login successful'
        }), 200
    else:
        return jsonify({'msg': 'Invalid credentials'}), 401
    
@app.route('/logout')
def logout():
    u_id=session.get('u_id')
    admin_or_not=User.query.get(u_id).admin
    return 
