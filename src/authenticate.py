from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity#, create_refresh_token
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.database import User, db
from flasgger import swag_from

authenticate = Blueprint("authenticate", __name__, url_prefix="/Authenticate")

@authenticate.post('/Register')
def register():
    if request.json.get('username') and request.json.get('password'):
        username = request.json.get('username')
        password = request.json.get('password')
        pwd_hash = generate_password_hash(password)
        
        if len(password)<6:
            return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

        if len(username)<3:
            return jsonify({'error': "Username is too short"}), HTTP_400_BAD_REQUEST

        if not username.isalnum() or " " in username:
            return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

        pwd_hash = generate_password_hash(password)

        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify({
                    'error': "Username is taken"
                }), HTTP_409_CONFLICT
            
            user = User(username=username, password=pwd_hash)
            db.session.add(user)
            db.session.commit()

            return jsonify({
                "message": "User created",
                "user": {
                    "username": username
                }
            }), HTTP_201_CREATED

        except Exception as e:
            return jsonify({
                "error": e
            }), HTTP_400_BAD_REQUEST
    
    else:
        return jsonify({
            "error" : "username or password is not passed"
        }), HTTP_400_BAD_REQUEST

@authenticate.post("/Login")
@swag_from('./docs/auth/login.yaml')
def login():
    if request.json.get('username') and request.json.get('password'):
        username = request.json.get('username')
        password = request.json.get('password')

        try:
            user = User.query.filter_by(username=username).first()
            
            if user:
                is_pass_correct = check_password_hash(user.password, password)

                if is_pass_correct:
                    access_token = create_access_token(identity=user.username)
                    return jsonify({
                        'user': {
                            'access_token': access_token,
                            'username': username
                        }
                    }), HTTP_200_OK
            
                return jsonify({
                    'error': 'Wrong credentials',
                    'data_passed': {
                        'username': username
                    }
                }), HTTP_401_UNAUTHORIZED

            return jsonify({
                'error': 'No user is registered with given details',
                'data_passed': {
                    'username': username
                }
            }), HTTP_404_NOT_FOUND

        except Exception as e:
            return jsonify({
                "error": e
            }), HTTP_404_NOT_FOUND

    else:
        return jsonify({
            "error" : "username or password is not passed"
        }), HTTP_400_BAD_REQUEST

@authenticate.get("/me")
@jwt_required()
def me():
    username = get_jwt_identity()
    return {
        "user": {
            "username": username
        }
    }, HTTP_200_OK