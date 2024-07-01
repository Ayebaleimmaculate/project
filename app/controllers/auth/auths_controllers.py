from flask import Blueprint, request, jsonify
import validators
from app.models.users import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from http import HTTPStatus


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not all([first_name, last_name, email, password, user_type]):
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email address already in use'}), HTTP_400_BAD_REQUEST

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        is_admin = (user_type == 'Admin')
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, user_type=user_type, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': f'{new_user.get_full_name()} has been successfully registered as an {new_user.user_type}',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'created_at': new_user.created_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to register user. Please try again later.'}), HTTP_500_INTERNAL_SERVER_ERROR


@auth.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'password' in data:
            user.password = data['password']  
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    

    
@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': "Email and password are required"}), HTTP_400_BAD_REQUEST

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'access_token': access_token,
                'is_admin': user.is_admin,
            },
            'message': "You have successfully logged into your account"
        }), HTTP_200_OK

    return jsonify({"error": "Invalid email or password"}), HTTP_401_UNAUTHORIZED

@auth.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR