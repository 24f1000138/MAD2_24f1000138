from flask import Flask,request,session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt
)
from datetime import datetime, timedelta,date
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy.sql import func
import os
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})
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
    pin=db.Column(db.String(6), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    rparking_spots = db.relationship("ReserveParkingSpot", backref='user', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(30),unique=True, nullable=False)
    password=db.Column(db.String(15),unique=True,nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=True)

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
    status=db.Column(db.String(1), nullable=False)

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

@app.route('/register', methods=['POST'])
@cross_origin()
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
@cross_origin()
def login():
    data = request.get_json()
    e = data.get('email')
    p = data.get('password')

    if not e or not p:
        return jsonify({'msg': 'Email and Password are required'}), 400

    user = User.query.filter_by(email=e).first()
    admin= Admin.query.filter_by(email=e).first()
    if user and check_password_hash(user.password, p):
        access_token=create_access_token(identity=str(user.u_id), additional_claims={"admin": False})
        return jsonify({
            'access_token': access_token,
            'admin': user.admin,
            'msg': 'User Login successful'
        }), 200
    elif admin and check_password_hash(admin.password, p):
        access_token=create_access_token(identity=str(admin.a_id), additional_claims={"admin": True})
        return jsonify({
            'access_token': access_token,
            'admin': admin.admin,
            'msg': 'Admin Login successful'
        }), 200
    else:
        return jsonify({'msg': 'Invalid credentials'}), 401

 
@app.route('/logout', methods=['POST'])
@jwt_required()
@cross_origin() 
def logout():
    jti = get_jwt()
    return jsonify({ 
            'msg': 'Logout successful'
        }), 200

@app.route('/admin_dashboard', methods=['OPTIONS'])
@cross_origin()
def admin_dashboard_options():
    return '', 200

@app.route('/admin_dashboard', methods=['GET','POST'])
@jwt_required()
@cross_origin()
def admin_dashboard():
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    p_lots = ParkingLot.query.all()
    data = []
    for lot in p_lots:
        spots= ParkingSpot.query.filter_by(lot_id=lot.lot_id).all()
        reserved_spots = ReserveParkingSpot.query.join(ParkingSpot).filter(ParkingSpot.lot_id == lot.lot_id).count()
        data.append({
            'lot_id': lot.lot_id,
            'name': lot.name,
            'num': lot.num,
            'occupied': reserved_spots,
            'spots': [{'spot_id': spot.spot_id, 'status': spot.status} for spot in spots]
        })
    return jsonify(data), 200

@app.route('/admin_addlot', methods=['POST','OPTIONS'])
@jwt_required(optional=True)
@cross_origin()
def admin_addlot():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200 
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    address = data.get('address')
    pinc = data.get('pinc')
    num = data.get('num')

    if not name or not price or not address or not pinc or not num:
        return jsonify({'msg': 'All fields are required'}), 400
    try:
        new_lot = ParkingLot(name=name, price=price, address=address, pinc=pinc, num=num)
        db.session.add(new_lot)
        db.session.flush()
        for i in range(num):
            new_spot = ParkingSpot(lot_id=new_lot.lot_id, status='A')
            db.session.add(new_spot)
            db.session.commit()
    
        return jsonify({'msg': 'Parking Lot added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500    
    
@app.route('/admin_editlot/<int:lot_id>', methods=['GET','POST'])
@cross_origin()
@jwt_required()
def admin_editlot(lot_id):
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'msg': 'Parking Lot not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'lot_id': lot.lot_id,
            'name': lot.name,
            'price': lot.price,
            'address': lot.address,
            'pinc': lot.pinc,
            'num': lot.num
        }), 200
    if request.method == 'POST':
        data = request.get_json()
        lot.name = data.get('name', lot.name)
        lot.price = data.get('price', lot.price)
        lot.address = data.get('address', lot.address)
        lot.pinc = data.get('pinc', lot.pinc)
        lot.num = data.get('num', lot.num)
        try:
            db.session.commit()
            return jsonify({'msg': 'Parking Lot updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': str(e)}), 500

@app.route('/admin_dashboard/<int:lot_id>', methods=['DELETE','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def admin_deletelot(lot_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'msg': 'Parking Lot not found'}), 404

    o_spots=ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='O').count()
    if o_spots > 0:
        return jsonify({'msg': 'Cannot delete Parking Lot with reserved spots'}), 400
    try:
        ParkingSpot.query.filter_by(lot_id=lot.lot_id).delete()
        db.session.delete(lot)
        db.session.commit()
        return jsonify({'msg': 'Parking Lot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
