import celery
from flask import Flask,request, jsonify, send_from_directory, send_file
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
from flask_cors import CORS
from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail, Message
import tempfile
import csv
from io import StringIO
import pytz
import qrcode
import requests

os.add_dll_directory(r"C:\GTK3\bin")
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache= Cache(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mangaimathimk@gmail.com'
app.config['MAIL_PASSWORD'] = 'wbzf kzpy qrkc xvkz'
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/1',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    celery.conf.timezone = 'Asia/Kolkata'
    celery.conf.enable_utc = False

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)
mail= Mail(app)
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
    vehicle_no= db.Column(db.String(10), db.ForeignKey('vehicle.vehicle_no'), nullable=False)
    payment_status = db.Column(db.String(10), nullable=False, default='Pending')

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    v_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    r_id = db.Column(db.Integer, db.ForeignKey('rparking_spot.r_id'), nullable=True)
    vehicle_no = db.Column(db.String(10), nullable=False)

CELERYBEAT_SCHEDULE = {
    'daily_rem':{
        'task': 'tasks.send_reminder',
        'schedule': crontab(hour=13, minute=30), 
    },
    'monthly_rep': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=30, hour=13, minute=30), 
    }
}
celery.conf.beat_schedule = CELERYBEAT_SCHEDULE

@celery.task(name='tasks.send_reminder')
def send_reminder():
    with app.app_context():
        spots = ReserveParkingSpot.query.filter(ReserveParkingSpot.end_time == None).order_by(ReserveParkingSpot.start_time.asc()).all()
        for spot in spots:
            user = User.query.get(spot.u_id)
            spot1=ParkingSpot.query.get(spot.spot_id)
            lot= ParkingLot.query.get(spot1.lot_id)
            if spot.start_time.tzinfo is None:
                spot.start_time = IST.localize(spot.start_time)
            cost= (((datetime.now(IST) - spot.start_time).total_seconds() // 3600 )+1)* lot.price
            if user:
                msg = Message('Daily Parking Spot Reminder',
                              sender='mangaimathimk@gmail.com',
                              recipients=[user.email])
                msg.body = f'Hi {user.name}! Remember to check your parking spot {spot.spot_id} at address "{lot.address}". The cost is ₹{lot.price} per hour and the estimated cost is already ₹{cost}. Come and pick up your vehicle at your earliest convenience. Have a great day!'
                mail.send(msg)
                print(f'Reminder sent to {user.email}')

@celery.task(name='tasks.generate_monthly_report')
def generate_monthly_report():
    with app.app_context():
        from weasyprint import HTML
        users= User.query.all()
        for user in users:
            today = datetime.now(IST)
            this_month=datetime(today.year, today.month, 30)
            if today.month == 1:
                last_month = datetime(today.year - 1, 12, 30)
            else:
                last_month = datetime(today.year, today.month - 1, 30)
            spots= ReserveParkingSpot.query.filter(ReserveParkingSpot.u_id==user.u_id, ReserveParkingSpot.end_time>=last_month, ReserveParkingSpot.end_time<this_month).all()
            if spots:
                html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: "Segoe UI", sans-serif;
                        margin: 40px;
                        font-size: 14px;
                    }}
                    h1 {{
                        text-align: center;
                        color: #2c3e50;
                    }}
                    p {{
                        margin: 10px 0;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                        margin-bottom: 20px;
                    }}
                    th, td {{
                        border: 1px solid #999;
                        padding: 10px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .summary {{
                        margin-top: 20px;
                        font-weight: bold;
                    }}
                </style>
                </head>
                <body>
                <h1>Monthly Parking Report</h1>
                <p><strong>User:</strong> {user.name}</p>
                <p><strong>Email:</strong> {user.email}</p>
                <table>
                    <tr>
                    <th>Spot ID</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Cost</th>
                    </tr>
                '''
                for spot in spots:
                    if spot.start_time.tzinfo is None:
                        spot.start_time = IST.localize(spot.start_time)
                    if spot.end_time.tzinfo is None:
                        spot.end_time = IST.localize(spot.end_time)
                    html_content += f"<tr><td>{spot.spot_id}</td><td>{spot.start_time.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{spot.end_time.strftime('%Y-%m-%d %H:%M:%S')}</td><td>{spot.cost}</td></tr>"
                html_content += '</table>'
                html_content += f'<p class="summary">Total Spots Used this month: {len(spots)}</p>'
                html_content += f'<p class="summary">Total Cost incurred this month: ₹{sum(spot.cost for spot in spots)}</p>'
                html_content += '<p>Thank you for your patronage!Please use our services again.</p>'
                pdf = HTML(string=html_content).write_pdf()
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    temp_file.write(pdf)
                    temp_file_path = temp_file.name
                
                msg = Message('Monthly Parking Report',
                              sender='noreply@parkingapp.com',
                              recipients=[user.email])
                msg.body = f'Hi {user.name}! Below we have attached your monthly parking report. Please find the details of your parking spots used in the last month and for any discrepancies, contact us at mangaimathimk@gmail.com. Thank you for using our services!'
                with app.open_resource(temp_file_path) as fp:
                    msg.attach('monthly_report.pdf', 'application/pdf', fp.read())
                mail.send(msg)
                print(f'Monthly report sent to {user.email}')

@celery.task(name='tasks.export_csv')
def export_csv():
    with app.app_context():
        users = User.query.all()
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['User ID', 'Name', 'Email', 'Address', 'PIN'])
        for user in users:
            writer.writerow([user.u_id, user.name, user.email, user.addr, user.pin])
        output.seek(0)
        csv_path = os.path.join(static_dir, 'users.csv')
        with open(csv_path, 'w') as f:
            f.write(output.getvalue())
        print(f'CSV file created at {csv_path} for admin to see')

@celery.task(name='tasks.export_csv_user')
def export_csv_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        spots= ReserveParkingSpot.query.filter_by(u_id=user.u_id).all()
        if not user:
            return
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Reservation ID', 'Spot ID', 'Start Time', 'End Time', 'Vehicle Number', 'Cost', 'Remarks'])
        for spot in spots:
            veh= Vehicle.query.filter_by(u_id=user.u_id, r_id= spot.r_id).first()
            if spot.start_time.tzinfo is None:
                spot.start_time = IST.localize(spot.start_time)
            if spot.end_time:
                if spot.end_time.tzinfo is None:
                    spot.end_time = IST.localize(spot.end_time)

            if spot.cost==None:
                remarks="Yet to be released"
            else:
                remarks="Released/Parked Out"
            writer.writerow([spot.r_id, spot.spot_id, spot.start_time.strftime('%Y-%m-%d %H:%M:%S'), spot.end_time.strftime('%Y-%m-%d %H:%M:%S') if spot.end_time else None, veh.vehicle_no if veh else None, spot.cost, remarks])
        output.seek(0)
        csv_path = os.path.join(static_dir, f'user_{user.u_id}_report.csv')
        with open(csv_path, 'w',encoding='utf-8') as f:
            f.write(output.getvalue())
        msg = Message('Your CSV report is ready!',
              sender='mangaimathimk@gmail.com',
              recipients=[user.email])
        msg.body = f'Hi {user.name},\n\nYour parking history CSV has been generated.'
        mail.send(msg)
        print(f'CSV file created at {csv_path} for user {user.name} to see')

@app.route('/trigger_csv', methods=['GET','POST'])
@jwt_required()
def trigger_admin_csv():
    export_csv.delay()
    return jsonify({"message": "CSV generation started. You'll be notified once it's ready. After generation, you can view it on static folder"}), 202

@app.route('/trigger_csv/<int:user_id>', methods=['POST'])
@jwt_required()
def trigger_csv(user_id):
    export_csv_user.delay(user_id)
    return jsonify({"message": "CSV generation started. You'll be notified once it's ready. After generation, it will be downloaded automatically."}), 202

@app.route('/download_csv/<int:user_id>', methods=['GET'])
def download_csv(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    filename = f'user_{user.u_id}_report.csv'
    file_path = os.path.join(static_dir, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'CSV file not found. Please export first.'}), 404
    return send_from_directory(directory=static_dir, path=filename, as_attachment=True)

@app.route('/check_csv/<int:user_id>', methods=['GET'])
@jwt_required()
def check_csv(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"ready": False}), 404
    filename = f'user_{user.u_id}_report.csv'
    file_path = os.path.join(static_dir, filename)
    if os.path.exists(file_path):
        return jsonify({"ready": True})
    return jsonify({"ready": False})

def graph_1():
    data= db.session.query(
        ParkingLot.name,
        func.sum(ReserveParkingSpot.cost)
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).join(ReserveParkingSpot, ParkingSpot.spot_id == ReserveParkingSpot.spot_id).filter(~ParkingLot.name.ilike('__deleted__%')).group_by(ParkingLot.name).all()
    if not data:
        return -1
    lot_names = [row[0] for row in data]
    lot_costs = [row[1] for row in data]
    pie= plt.figure(figsize=(10, 6))
    plt.pie(lot_costs, labels=lot_names, autopct='%1.1f%%', startangle=140)
    plt.title('Revenue from each Parking Lot')
    pie_path = os.path.join(static_dir, 'lot_earnings.png')
    pie.savefig(pie_path)
    print(lot_names)
    plt.close()
    
def graph_2():
    data=db.session.query(
        ParkingLot.name,
        func.sum(case((ParkingSpot.status == 'A', 1), else_=0)).label('available'),
        func.sum(case((ParkingSpot.status == 'O', 1), else_=0)).label('occupied')
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).filter(~ParkingLot.name.ilike('__deleted__%')).group_by(ParkingLot.name).all()
    if not data:
        return -1
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
    print(lot_names)
    bar.savefig(bar_path)
    plt.close()

def graph_3():
    data= db.session.query(
        ParkingLot.name,
        func.sum(case((ReserveParkingSpot.end_time.isnot(None), 1),else_=0)).label('reservation_count')
    ).join(ParkingSpot, ParkingLot.lot_id == ParkingSpot.lot_id).join(ReserveParkingSpot, ParkingSpot.spot_id == ReserveParkingSpot.spot_id).filter(~ParkingLot.name.ilike('__deleted__%')).group_by(ParkingLot.name).all()
    if not data:
        return -1
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

def skip_cache1():
    try:
        current_user = get_jwt_identity()
        return current_user is None 
    except RuntimeError:
        return True 
    
def cache_key1():
    try:
        current_user = get_jwt_identity()
        return f"admin_dashboard_{current_user}" if current_user else "admin_dashboard_none"
    except RuntimeError:
        return "admin_dashboard_error"

def cache_key2():
    try:
        current_user = get_jwt_identity()
        return f"admin_users_{current_user}" if current_user else "admin_users_none"
    except RuntimeError:
        return "admin_users_error"

def cache_key3():
    try:
        current_user = get_jwt_identity()
        return f"user_dashboard_{current_user}" if current_user else "user_dashboard_none"
    except RuntimeError:
        return "user_dashboard_error"
    
def cache_key4():
    try:
        current_user = get_jwt_identity()
        return f"user_history_{current_user}" if current_user else "user_history_none"
    except RuntimeError:
        return "user_history_error"

@app.before_request
def create_tables():
    db.create_all()
    if not Admin.query.filter_by(email="Admin01@gmail.com").first():
        admin=Admin(name="Admin", email="Admin01@gmail.com", password=generate_password_hash("Taara4590$"))
        db.session.add(admin)
        db.session.commit() 

@app.route('/register', methods=['POST'])
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
                cache.delete(f"admin_users_1")
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
def logout():
    return jsonify({ 
            'msg': 'Logout successful'
        }), 200

@cache.cached(unless=skip_cache1, key_prefix=cache_key1)
@app.route('/admin_dashboard', methods=['GET', 'OPTIONS'])
@jwt_required()
def admin_dashboard():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
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
@jwt_required()
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
        cache.delete(f"admin_dashboard_1")
        return jsonify({'msg': 'Parking Lot added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500    
    
@app.route('/admin_editlot/<int:lot_id>', methods=['GET','POST'])
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
            cache.delete(f"admin_dashboard_1")
            return jsonify({'msg': 'Parking Lot updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'msg': str(e)}), 500

@app.route('/admin_dashboard/<int:lot_id>', methods=['DELETE','OPTIONS'])
@jwt_required()
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
        cache.delete(f"admin_dashboard_1")
        return jsonify({'msg': 'Parking Lot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

@app.route('/admin_viewspot/<int:spot_id>', methods=['GET','OPTIONS','DELETE'])
@jwt_required()
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

@app.route('/admin_search', methods=['GET','OPTIONS'])
@jwt_required()
def admin_search():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403
    
    search_by = request.args.get('searchBy',default='location').strip()
    query = request.args.get('query', '').strip()
    results=[]
    if search_by == 'location':
        if not query:
            return jsonify([]), 200
        p_lots= ParkingLot.query.filter(
            ((ParkingLot.name.ilike(f'%{query}%')) & (~ParkingLot.name.ilike('__deleted__%')))).all()
        
        for lot in p_lots: 
            spots= ParkingSpot.query.filter_by(lot_id=lot.lot_id).all()
            reserved_spots = ReserveParkingSpot.query.join(ParkingSpot).filter(ParkingSpot.lot_id == lot.lot_id, ReserveParkingSpot.end_time == None).count()
            results.append({
                'lot_id': lot.lot_id,
                'name': lot.name,
                'num': lot.num,
                'occupied': reserved_spots,
                'spots': [{'spot_id': spot.spot_id, 'status': spot.status} for spot in spots]
            }) 
    elif search_by == 'user':
        try:
            userId= int(query)
            user = User.query.get(userId)
            if not user:
                return jsonify({'msg': 'User not found'}), 404
            results.append({
                'u_id': user.u_id,
                'email': user.email,
                'name': user.name,
                'addr': user.addr,
                'pin': user.pin
            }) 
        except ValueError:
            return jsonify([]), 200
    elif search_by == 'spot':
        try:
            spotId = int(query)
            spot = ParkingSpot.query.get(spotId)
            if not spot:
                return jsonify({'msg': 'Parking Spot not found'}), 404
            lot = ParkingLot.query.get(spot.lot_id)
            reserved_spots = ReserveParkingSpot.query.filter_by(spot_id=spotId, end_time=None).count()
            results.append({
                'spot_id': spot.spot_id,
                'lot_id': lot.lot_id,
                'lot_name': lot.name,
                'status': spot.status,
                'r_count': reserved_spots
            }) 
        except ValueError:
            return jsonify([]), 200
    else:
        return jsonify([]), 200
    return jsonify(results), 200

@app.route('/admin_summary', methods=['GET','OPTIONS'] )
@jwt_required()
def admin_summary():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        return jsonify({'msg': 'Access denied'}), 403
    
    c1=graph_1()
    c2=graph_2()   
    return jsonify({
        'msg': 'Summary graphs generated successfully',
        'revenue_graph': '/static/lot_earnings.png' if c1 != -1 else None,
        'availability_graph': '/static/lot_availability.png' if c2 != -1 else None
    }), 200

@app.route('/user_summary', methods=['GET','OPTIONS'])
@jwt_required()
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
        
        c3=graph_3()
        if c3 == -1:
            return jsonify({'msg': 'No data available for summary graphs'}), 404
        return jsonify({
        'msg': 'Summary graphs generated successfully',
        'reservation_graph': '/static/lot_reservations.png',
        'name': user.name
}), 200

@app.route('/admin_reservespot/<int:spot_id>', methods=['GET','OPTIONS'])
@jwt_required()
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
    vehicle=Vehicle.query.filter_by(u_id=user.u_id,r_id=spot.r_id).first()
    if spot.start_time.tzinfo is None:
            spot.start_time = IST.localize(spot.start_time)
    if spot.end_time:
        if spot.end_time.tzinfo is None:
            spot.end_time = IST.localize(spot.end_time)
        hours = ((spot.end_time - spot.start_time).total_seconds() // 3600) + 1
        cost = int(hours * price)
    else:
        hours = ((datetime.now(IST) - spot.start_time).total_seconds() // 3600) + 1
        cost = int(hours * price)
    return jsonify({
        'spot_id': spot.spot_id,
        'u_id': spot.u_id,
        'user_name': user.name if user else None,
        'vehicle_no': vehicle.vehicle_no if vehicle else None,
        'start_time': spot.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'cost': cost
    }), 200

@cache.cached(timeout=60,unless=skip_cache1, key_prefix=cache_key2)
@app.route('/admin_users', methods=['GET','OPTIONS'])
@jwt_required()
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

@cache.cached(unless=skip_cache1, key_prefix=cache_key3)
@app.route('/user_dashboard', methods=['GET','OPTIONS'])
@jwt_required()
def user_dashboard():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        spots=ReserveParkingSpot.query.filter_by(u_id=user.u_id).all()
        data = []
        for spot in spots:
            s=ParkingSpot.query.get(spot.spot_id)
            loc= ParkingLot.query.get(s.lot_id).name
            sp=ReserveParkingSpot.query.filter_by(r_id=spot.r_id).first()
            veh_no=sp.vehicle_no
            if sp.start_time.tzinfo is None:
                sp.start_time = IST.localize(sp.start_time)
            if (spot.end_time is None) or (spot.start_time >= datetime.now(IST) - timedelta(days=30)):
                 data.append({
                    'name': user.name,
                    'r_id': spot.r_id,
                    'loc' : loc,
                    'veh_no': veh_no if veh_no else None,
                    'stamp': spot.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': spot.end_time.strftime('%Y-%m-%d %H:%M:%S') if spot.end_time else None
                })
        return jsonify(data), 200

@app.route('/user_search', methods=['GET','OPTIONS'])
@jwt_required()
def user_search():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        query = request.args.get('query', '').strip()
        if not query:
            return jsonify([]), 200
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
@jwt_required()
def user_book(lot_id):
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
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
                a_veh=db.session.query(Vehicle).join(ReserveParkingSpot, Vehicle.r_id == ReserveParkingSpot.r_id).filter(Vehicle.u_id == user.u_id,Vehicle.vehicle_no == vehicle_no, ReserveParkingSpot.end_time == None).first()
                if a_veh:
                    return jsonify({'msg': 'Vehicle already booked a spot and in use'}), 409
                
                new=ReserveParkingSpot(
                        spot_id=spot_id,
                        u_id=user.u_id,
                        start_time =datetime.now(IST),
                        end_time=None,
                        cost=0,
                        vehicle_no=vehicle_no,
                        payment_status='Pending'
                    )
                db.session.add(new)
                db.session.commit()
                if not Vehicle.query.filter_by(u_id=user.u_id, vehicle_no=vehicle_no).first():       
                    try: 
                        r_id=new.r_id
                        new_vehicle = Vehicle(u_id=user.u_id, r_id=r_id, vehicle_no=vehicle_no)
                        db.session.add(new_vehicle)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        return jsonify({'msg': str(e)}), 500
                else:
                    veh=Vehicle.query.filter_by(u_id=user.u_id, vehicle_no=vehicle_no).first()
                    veh.r_id = new.r_id
                    db.session.commit()
                spot = ParkingSpot.query.get(spot_id)
                spot.status = 'O'
                db.session.commit()
                cache.delete(f"user_dashboard_{user_id}")
                cache.delete(f"admin_dashboard_1")
                return jsonify({'msg': 'Booking successful'}), 201
                    
            else:
                return jsonify({'msg': 'Vehicle number is required'}), 400

@app.route('/user_release/<int:r_id>', methods=['GET','POST','OPTIONS'])
@jwt_required()    
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

        end_time = datetime.now(IST)
        if spot.start_time.tzinfo is None:
            spot.start_time = IST.localize(spot.start_time)
        hours = ((end_time - spot.start_time).total_seconds() // 3600) + 1
        s = ParkingSpot.query.get(spot.spot_id)
        lot= ParkingLot.query.get(s.lot_id)
        cost = int(hours * lot.price)
        veh_no= Vehicle.query.filter_by(u_id=user.u_id, r_id=spot.r_id).first()
        print(veh_no)
        if request.method == 'GET':
            data=[{
                'spot_id': spot.spot_id,
                'veh_no': veh_no.vehicle_no if veh_no else None,
                'start_time': spot.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'cost': cost
            }]
            return jsonify(data), 200
        if request.method == 'POST':
            if veh_no:
                spot.end_time = end_time
                spot.cost = cost
                s.status = 'A'
                veh_no.r_id = None
                db.session.commit()
                cache.delete(f"user_dashboard_{user_id}")
                cache.delete(f"user_history_{user_id}")
                cache.delete(f"admin_dashboard_1")
            return jsonify({'msg': 'Spot released successfully', 'cost': cost}), 200

@cache.cached(unless=skip_cache1,key_prefix=cache_key4)
@app.route('/user_history', methods=['GET','OPTIONS'])
@jwt_required()
def user_history():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        spots = ReserveParkingSpot.query.filter(ReserveParkingSpot.u_id == user.u_id, ReserveParkingSpot.end_time != None).order_by(ReserveParkingSpot.end_time.desc()).all()
        data = []
        for spot in spots:
            s = ParkingSpot.query.get(spot.spot_id)
            loc = ParkingLot.query.get(s.lot_id).name
            sp= ReserveParkingSpot.query.filter_by(r_id=spot.r_id).first()
            veh_no=sp.vehicle_no
            data.append({
                    'name': user.name,
                    'u_id': user_id,
                    'r_id': spot.r_id,
                    'loc': loc,
                    'veh_no': veh_no if veh_no else None,
                    'start_time': spot.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': spot.end_time.strftime('%Y-%m-%d %H:%M:%S') if spot.end_time else None,
                    'cost': spot.cost,
                    'payment': spot.payment_status
            })
        return jsonify(data), 200

@app.route('/user_profile', methods=['GET','POST','OPTIONS'])
@jwt_required()
def user_profile():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'CORS preflight'}), 200
    current_user = get_jwt()
    if not current_user.get('admin'):
        user_id = current_user.get("sub")
        user = User.query.get(int(user_id))
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
                cache.delete(f"user_dashboard_{user_id}")
                cache.delete("admin_users_1")
                return jsonify({'msg': 'Profile updated successfully'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg': str(e)}), 500

@app.route('/generate_qr/<int:r_id>', methods=['GET'])
def generate_qr(r_id):
    spot = ReserveParkingSpot.query.get(r_id)
    if not spot:
        return "Invalid reservation", 404
    amount = spot.cost or 10
    NGROK_URL = "https://24f1000138.loca.lt"
    upi_link = f"{NGROK_URL}/mark_paid/{r_id}/{amount}"
    qr_img = qrcode.make(upi_link)
    qr_path = os.path.join(static_dir, f"qr_{r_id}.png")
    qr_img.save(qr_path)
    return send_file(qr_path, mimetype='image/png')

@app.route('/mark_paid/<int:r_id>/<int:amount>', methods=['GET'])
def mark_paid(r_id, amount):
    spot = ReserveParkingSpot.query.get(r_id)
    if not spot:
        return '<h2>Invalid Reservation ID</h2>', 404
    spot.payment_status = "Paid"
    db.session.commit()
    return f'''
        <html>
          <head><title>Payment Complete</title></head>
          <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h2 style="color: green;"> Payment Completed</h2>
            <p> ₹ {amount} received on ParkPay </p>
            <p>Thank you for your patronage.You may now return to the app.</p>
          </body>
        </html>
    '''

@app.route('/get_tunnel_password', methods=['GET'])
def get_tunnel_password():
    try:
        response = requests.get("https://loca.lt/mytunnelpassword", timeout=5)
        if response.status_code == 200:
            return {'password': response.text.strip()}
        else:
            return {'password': 'Unavailable'}, 500
    except Exception as e:
        return {'password': f"Error: {str(e)}"}, 500

@app.route('/check_payment_status/<int:r_id>', methods=['GET'])
def check_payment_status(r_id):
    spot = ReserveParkingSpot.query.get(r_id)
    if not spot:
        return {'status': 'Invalid ID'}, 404
    return {'status': spot.payment_status}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
