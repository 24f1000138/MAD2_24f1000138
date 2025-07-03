from flask import Flask,request,session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
)
from datetime import datetime, timedelta
from sqlalchemy import case
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
    vehicles = db.relationship("Vehicle", backref='user', lazy=True)
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
    end_time = db.Column(db.DateTime, nullable=True)
    cost= db.Column(db.Integer, nullable=True)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    v_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('rparking_spot.spot_id'), nullable=False)
    vehicle_no = db.Column(db.String(10), nullable=False)

def graph_1():
    data= db.session.query(
        ParkingLot.name,
        func.sum(ReserveParkingSpot.cost)
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).join(ReserveParkingSpot, ParkingSpot.spot_id == ReserveParkingSpot.spot_id).group_by(ParkingLot.name).all()
    if not data:
        return
    lot_names = [row[0] for row in data]
    lot_costs = [row[1] for row in data]
    pie= plt.figure(figsize=(10, 6))
    plt.pie(lot_costs, labels=lot_names, autopct='%1.1f%%', startangle=140)
    plt.title('Revenue from each Parking Lot')
    pie_path = os.path.join(static_dir, 'lot_earnings.png')
    pie.savefig(pie_path)
    plt.close()
    
def graph_2():
    data=db.session.query(
        ParkingLot.name,
        func.sum(case((ParkingSpot.status == 'A', 1), else_=0)).label('available'),
        func.sum(case((ParkingSpot.status == 'O', 1), else_=0)).label('occupied')
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).group_by(ParkingLot.name).all()
    if not data:
        return
    lot_names = [row[0] for row in data]
    lot_a = [row[1] for row in data]
    lot_o = [row[2] for row in data]
    bar = plt.figure(figsize=(10, 6))
    plt.bar([i - 0.175 for i in range(len(lot_names))], lot_a, width=0.35, label='Available', color='green')
    plt.bar([i + 0.175 for i in range(len(lot_names))], lot_o, width=0.35, label='Occupied', color='tomato')

    plt.xlabel('Parking Lots')
    plt.ylabel('Number of Spots')
    plt.title('Available Parking Spots in Each Lot')
    plt.xticks(range(len(lot_names)), lot_names, rotation=45)
    plt.legend()
    bar_path = os.path.join(static_dir, 'lot_availability.png')
    bar.savefig(bar_path)
    plt.close()

def graph_3():
    data= db.session.query(
        ParkingLot.name,
        func.sum(case((ReserveParkingSpot.end_time.isnot(None), 1),else_=0)).label('reservation_count')
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).join(ReserveParkingSpot, ParkingSpot.spot_id == ReserveParkingSpot.spot_id).group_by(ParkingLot.name).all()
    if not data:
        return
    lot_names = [row[0] for row in data]
    lot_counts = [row[1] for row in data]
    bar = plt.figure(figsize=(10, 6))
    plt.bar(lot_names, lot_counts, color='blue')
    plt.xlabel('Parking Lots')
    plt.ylabel('Number of Reservations')
    plt.title('Summary on already used parking spots')
    plt.xticks(rotation=45)
    bar_path = os.path.join(static_dir, 'lot_reservations.png')
    bar.savefig(bar_path)
    plt.close()

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

 
@app.route('/logout', methods=['GET','POST','OPTIONS'])
@jwt_required()
@cross_origin() 
def logout():
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

    p_lots = ParkingLot.query.filter(~ParkingLot.name.ilike('__deleted__%')).all()
    data = []
    for lot in p_lots:
        spots= ParkingSpot.query.filter_by(lot_id=lot.lot_id).all()
        reserved_spots = ReserveParkingSpot.query.join(ParkingSpot).filter(ParkingSpot.lot_id == lot.lot_id, ReserveParkingSpot.end_time == None).count()
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
        n=lot.num
        lot.num = data.get('num', lot.num)
        try:
            if lot.num > n:
                for i in range(n, lot.num):
                    new_spot = ParkingSpot(lot_id=lot.lot_id, status='A')
                    db.session.add(new_spot)
            elif lot.num < n:
                o_spots=ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='O').count()
                if o_spots == lot.num:
                    return jsonify({'msg': 'Cannot reduce Parking Lot with reserved spots'}), 400
                available_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='A').limit(n - lot.num).all()
                for spot in available_spots:
                    db.session.delete(spot)
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
        for spot in ParkingSpot.query.filter_by(lot_id=lot.lot_id).all():
            spot.status = 'X'
        lot.name =  f"__deleted__{lot.name}"
        db.session.commit()
        return jsonify({'msg': 'Parking Lot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

@app.route('/admin_viewspot/<int:spot_id>', methods=['GET','OPTIONS','DELETE'])
@cross_origin()
@jwt_required(optional=True)
def admin_viewspot(spot_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    if request.method == 'DELETE':
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return jsonify({'msg': 'Parking Spot not found'}), 404
        
        if spot.status == 'O':
            return jsonify({'msg': 'Cannot delete reserved Parking Spot'}), 400
        try:
            lot= ParkingLot.query.get(spot.lot_id)
            db.session.delete(spot)            
            if lot.num>0 and lot:
                lot.num -= 1
            db.session.commit()
            return jsonify({'msg': 'Parking Spot deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': str(e)}), 500
    if request.method == 'GET':
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return jsonify({'msg': 'Parking Spot not found'}), 404

        return jsonify({
            'spot_id': spot.spot_id,
            'status': spot.status
        }), 200

@app.route('/admin_summary', methods=['GET','OPTIONS'] )
@cross_origin()
@jwt_required(optional=True)
def admin_summary():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403
    
    graph_1()
    graph_2()
    return jsonify({
        'msg': 'Summary graphs generated successfully',
        'revenue_graph': '/static/lot_earnings.png',
        'availability_graph': '/static/lot_availability.png'
    }), 200

@app.route('/user_summary', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_summary():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    print(current_user)
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        
        graph_3()
        return jsonify({
            'msg': 'Summary graphs generated successfully',
            'reservation_graph': '/static/lot_reservations.png'
        }), 200

@app.route('/admin_reservespot/<int:spot_id>', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def admin_reservespot(spot_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403
    spot1= ParkingSpot.query.get(spot_id)
    lot= ParkingLot.query.get(spot1.lot_id)
    price=lot.price
    spot=ReserveParkingSpot.query.filter_by(spot_id=spot_id).first()
    if not spot:
        return jsonify({'msg': 'Reserved Parking Spot not found'}), 404
    user = User.query.get(spot.u_id)
    vehicle=Vehicle.query.filter_by(u_id=user.u_id,spot_id=spot.spot_id).first()
    if spot.end_time:
        hours = ((spot.end_time - spot.start_time).total_seconds() // 3600) + 1
        cost = int(hours * price)
    else:
        hours = ((datetime.utcnow() - spot.start_time).total_seconds() // 3600) + 1
        cost = int(hours * price)
    return jsonify({
        'spot_id': spot.spot_id,
        'u_id': spot.u_id,
        'user_name': user.name if user else None,
        'vehicle_no': vehicle.vehicle_no if vehicle else None,
        'start_time': spot.start_time.isoformat(),
        'cost': cost
    }), 200

@app.route('/admin_users', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def admin_users():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403

    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'u_id': user.u_id,
            'email': user.email,
            'name': user.name,
            'addr': user.addr,
            'pin': user.pin
        })
    return jsonify(data), 200

@app.route('/user_dashboard', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_dashboard():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = int(current_user['sub'])
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        spots=ReserveParkingSpot.query.filter_by(u_id=user.u_id).all()
        data = []
        for spot in spots:
            s=ParkingSpot.query.get(spot.spot_id)
            loc= ParkingLot.query.get(s.lot_id).name
            veh= Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot.spot_id).all()
            veh1= Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot.spot_id).count()
            if (spot.end_time is None) or (spot.start_time < datetime.utcnow()- timedelta(days=5)):
                if veh1 > 1:
                    for i in range(veh1):
                        data.append({
                            'r_id': spot.r_id,
                            'loc' : loc,
                            'veh_no': veh[i].vehicle_no,
                            'stamp': spot.start_time.isoformat()
                        })
                else:
                    data.append({
                        'r_id': spot.r_id,
                        'loc' : loc,
                        'veh_no': veh[0].vehicle_no if veh else None,
                        'stamp': spot.start_time.isoformat()
                    })
        return jsonify(data), 200

@app.route('/user_search', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_search():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = int(current_user['sub'])
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        query = request.args.get('query', '').strip()
        p_lots = ParkingLot.query.filter(
            ((ParkingLot.name.ilike(f'%{query}%')) & (~ParkingLot.name.ilike('__deleted__%'))) |
            (ParkingLot.pinc.ilike(f'%{query}%'))
        ).all()

        data = []
        for lot in p_lots:
            reserved_spots = ReserveParkingSpot.query.join(ParkingSpot).filter(ParkingSpot.lot_id == lot.lot_id, ReserveParkingSpot.end_time == None).count()
            count=lot.num-reserved_spots
            data.append({
                'lot_id': lot.lot_id,
                'addr': lot.address,
                'available': count,
            })
        return jsonify(data), 200

@app.route('/user_book/<int:lot_id>', methods=['GET','POST','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_book(lot_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = int(current_user['sub'])
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        
        lot = ParkingLot.query.get(lot_id)
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if not lot:
            return jsonify({'msg': 'Parking Lot not found'}), 404
        if request.method == 'GET':
            data=[{
                'lot_id': lot.lot_id,
                'spot_id': spot.spot_id if spot else None,
                'u_id':user_id}]
            
            return jsonify(data), 200    
    
        if request.method == 'POST':

            data = request.get_json()
            lot_id = data.get('lot_id', lot.lot_id)
            spot_id = data.get('spot_id', spot.spot_id)
            user_id = data.get('u_id', user.u_id)
            vehicle_no = data.get('vehicle_no')
            if vehicle_no:
                if not vehicle_no.strip():
                    return jsonify({'msg': 'Vehicle number is required'}), 400
                
                a_veh=db.session.query(Vehicle).join(ReserveParkingSpot).filter(Vehicle.u_id == user.u_id,Vehicle.vehicle_no == vehicle_no,Vehicle.spot_id == ReserveParkingSpot.spot_id,ReserveParkingSpot.end_time == None).first()
                if a_veh:
                    return jsonify({'msg': 'Vehicle already booked a spot and in use'}), 409
                if not Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot_id).first():
                        new_vehicle = Vehicle(u_id=user.u_id, spot_id=spot_id, vehicle_no=vehicle_no)
                        db.session.add(new_vehicle)
                        db.session.commit()
                new=ReserveParkingSpot(
                    spot_id=spot_id,
                    u_id=user.u_id,
                    start_time=datetime.utcnow(),
                    end_time=None,
                    cost=0
                )
                try:
                    db.session.add(new)
                    db.session.commit()
                    spot = ParkingSpot.query.get(spot_id)
                    spot.status = 'O'
                    db.session.commit()
                    return jsonify({'msg': 'Booking successful'}), 201
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'msg': str(e)}), 500

@app.route('/user_release/<int:r_id>', methods=['GET','POST','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)    
def user_release(r_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        spot = ReserveParkingSpot.query.get(r_id)
        if not spot or spot.u_id != user.u_id:
            return jsonify({'msg': 'Reservation not found or access denied'}), 404

        end_time = datetime.utcnow()
        hours = ((end_time - spot.start_time).total_seconds() // 3600) + 1
        s = ParkingSpot.query.get(spot.spot_id)
        lot= ParkingLot.query.get(s.lot_id)
        cost = int(hours * lot.price)
        veh_no= Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot.spot_id).first()
        if request.method == 'GET':
            data=[{
                'spot_id': spot.spot_id,
                'veh_no': veh_no.vehicle_no if veh_no else None,
                'start_time': spot.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'cost': cost
            }]
            return jsonify(data), 200
        if request.method == 'POST':
            if veh_no:
                spot.end_time = end_time
                spot.cost = cost
                s.status = 'A'
                db.session.commit()

            return jsonify({'msg': 'Spot released successfully', 'cost': cost}), 200

@app.route('/user_history', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_history():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = int(current_user['sub'])
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        spots = ReserveParkingSpot.query.filter_by(u_id=user.u_id).order_by(ReserveParkingSpot.end_time.desc()).all()
        data = []
        for spot in spots:
            if spot.end_time is not None:
                s = ParkingSpot.query.get(spot.spot_id)
                loc = ParkingLot.query.get(s.lot_id).name
                veh = Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot.spot_id).all()
                veh1 = Vehicle.query.filter_by(u_id=user.u_id, spot_id=spot.spot_id).count()
            
                if veh1 > 1:
                    for i in range(veh1):
                        data.append({
                            'r_id': spot.r_id,
                            'loc': loc,
                            'veh_no': veh[i].vehicle_no,
                            'start_time': spot.start_time.isoformat(),
                            'end_time': spot.end_time.isoformat(),
                            'cost': spot.cost
                        })
                else:
                    data.append({
                        'r_id': spot.r_id,
                        'loc': loc,
                        'veh_no': veh[0].vehicle_no if veh else None,
                        'start_time': spot.start_time.isoformat(),
                        'end_time': spot.end_time.isoformat() if spot.end_time else None,
                        'cost': spot.cost
                    })
        return jsonify(data), 200

@app.route('/user_profile', methods=['GET','POST','OPTIONS'])
@cross_origin()
@jwt_required(optional=True)
def user_profile():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = int(current_user['sub'])
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        if request.method == 'GET':
            data = {
                'name': user.name,
                'email': user.email,
                'addr': user.addr,
                'pin': user.pin
            }
            return jsonify(data), 200
        if request.method == 'POST':
            data = request.get_json()
            user.name = data.get('name', user.name)
            email = data.get('email', user.email) 
            e_user = User.query.filter(User.email == email, User.u_id != user.u_id).first()
            if e_user:
                return jsonify({'msg': 'Email already exists'}), 409
            else:
                user.email = email
            user.addr = data.get('addr', user.addr)
            user.pin = data.get('pin', user.pin)
            try:
                db.session.commit()
                return jsonify({'msg': 'Profile updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
