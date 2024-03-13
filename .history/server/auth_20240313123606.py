from flask import Flask, make_response, request, jsonify, abort, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from werkzeug.exceptions import NotFound
from models import db, User, Parcelar, Delivery, Location, UserNotification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SendIT.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key

jwt = JWTManager(app)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# Error handler for 404 Not Found
@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('index.html', title='Homepage', message='Welcome to SendIT')

# Authentication endpoints
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return {'error': 'Username, email, and password are required'}, 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'error': 'Username already exists'}, 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User created successfully'}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
    else:
        return {'error': 'Invalid username or password'}, 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'message': 'Successfully logged out'})
    unset_jwt_cookies(resp)
    return resp, 200

# Example of a protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return {'user_id': current_user_id}, 200

# Your existing resource classes and routes...
