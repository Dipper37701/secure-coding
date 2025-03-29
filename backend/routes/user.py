# backend/routes/user.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from utils.auth import hash_password, check_password

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    if not user.is_active:
        return jsonify({'error': '이 사용자는 더 이상 활성 상태가 아닙니다.'}), 403
    
    return jsonify({'user': user.to_dict()}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    data = request.get_json()
    
    # Update description if provided
    if 'description' in data:
        user.description = data['description']
    
    # Update password if provided
    if 'password' in data and data.get('currentPassword'):
        # Verify current password
        if not check_password(user.password, data['currentPassword']):
            return jsonify({'error': '현재 비밀번호가 올바르지 않습니다.'}), 400
        
        user.password = hash_password(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': '프로필이 업데이트되었습니다.',
        'user': user.to_dict()
    }), 200