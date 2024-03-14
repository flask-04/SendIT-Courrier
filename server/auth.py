from models import User,bcrypt,db,TokenBlocklist
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity,get_jwt
from flask import Blueprint,jsonify,request,make_response
auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/signup')
def signup_for_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    hashed_password = data['password']

    # check if username and email exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 404
    
    email_address = User.query.filter_by(email=email).first()
    if email_address:
        return jsonify({'message': 'Email already exists'}), 404
    
    else:

        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.serialize()), 201)
        return response

@auth_bp.post('/login')
def login_for_user(): 
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find  the user by username
    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password.encode('utf-8')):
        return jsonify({"message": "Invalid Credentials"}), 401
    else:
        # If username and password are correct  create a token for this user
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify({
             'message': 'Login successful',
             'Token': {
                  'access': access_token,
                  'refresh': refresh_token,
             }
        }), 200

    
    
@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token":access_token})
    
@auth_bp.get('/logout')
@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_blocklist = TokenBlocklist(jti=jti)

    db.session.add(token_blocklist)
    db.session.commit()

    return jsonify({"message":f"{token_type} token revoked successfully"}),200
    