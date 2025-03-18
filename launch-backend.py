from flask import Flask, render_template, request, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

bcrypt = Bcrypt()
db = SQLAlchemy(app)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_VERIFY_SUB"] = False

class User(db.Model): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

class Memo(db.Model): 
    __tablename__ = 'memo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(140), nullable=True)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register(): 
    data = request.json
    if not data['username'] or not data['password']: 
        return jsonify({"message": "Please fill in all the fields"})
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password_hash=hashed_pw)
    if User.query.filter_by(username=data['username']).first() is not None: 
        return jsonify({"message": f"User with username {data['username']} already exists"}), 403
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login(): 
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']): 
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return jsonify({"token": access_token, "message": f"You're logged in as {data['username']}"})
    return jsonify({"message": "Invaild ID or Password"}), 401

@app.route('/user', methods=['GET'])
@jwt_required()
def user(): 
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user: 
        return jsonify({"username": user.username})
    return jsonify({'message': 'No such user'}), 404

@app.route('/memo', methods=['POST'])
@jwt_required()
def write_memo(): 
    user_id = get_jwt_identity()
    assert request.get_json() is not None
    content = request.json.get("content")
    memo = Memo(user_id=user_id, content=content)
    db.session.add(memo)
    db.session.commit()
    return jsonify({"message": "Memo saved"})

@app.route('/memos', methods=['GET'])
@jwt_required()
def get_memo(): 
    user_id = get_jwt_identity()
    memos = Memo.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": m.id, "content": m.content} for m in memos])

# Initialize DB
with app.app_context(): 
    db.create_all()

if __name__=="__main__": 
    app.run(debug=True)