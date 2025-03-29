# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from utils.auth import hash_password, check_password, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '사용자 이름과 비밀번호는 필수입니다.'}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '이미 사용 중인 사용자 이름입니다.'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        password=hash_password(data['password']),
        description=data.get('description', '')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': '회원가입이 완료되었습니다.',
        'token': token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '사용자 이름과 비밀번호는 필수입니다.'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password(user.password, data['password']):
        return jsonify({'error': '사용자 이름 또는 비밀번호가 올바르지 않습니다.'}), 401
    
    # Check if user is active
    if not user.is_active:
        return jsonify({'error': '계정이 비활성화되었습니다. 관리자에게 문의하세요.'}), 403
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': '로그인 성공',
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/check', methods=['GET'])
@jwt_required()
def check_auth():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    return jsonify({
        'message': '인증됨',
        'user': user.to_dict()
    }), 200
