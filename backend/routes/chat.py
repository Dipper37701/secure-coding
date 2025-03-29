# backend/routes/chat.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ChatRoom, ChatParticipant, ChatMessage, User

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_chat_rooms():
    user_id = get_jwt_identity()
    
    # Get rooms where user is a participant
    participations = ChatParticipant.query.filter_by(user_id=user_id).all()
    room_ids = [p.room_id for p in participations]
    
    rooms = ChatRoom.query.filter(ChatRoom.id.in_(room_ids)).all()
    
    return jsonify({
        'rooms': [room.to_dict() for room in rooms]
    }), 200

@chat_bp.route('/rooms/global', methods=['GET'])
@jwt_required()
def get_global_chat():
    # Find or create global chat room
    global_room = ChatRoom.query.filter_by(name='Global Chat', is_private=False).first()
    
    if not global_room:
        global_room = ChatRoom(name='Global Chat', is_private=False)
        db.session.add(global_room)
        db.session.commit()
    
    return jsonify({
        'room': global_room.to_dict()
    }), 200

@chat_bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_private_chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('participant_id'):
        return jsonify({'error': '대화 상대가 필요합니다.'}), 400
    
    participant_id = data['participant_id']
    
    # Check if participant exists
    participant = User.query.get(participant_id)
    if not participant or not participant.is_active:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    # Check if a private chat already exists between these users
    user_rooms = ChatParticipant.query.filter_by(user_id=user_id).all()
    user_room_ids = [p.room_id for p in user_rooms]
    
    participant_rooms = ChatParticipant.query.filter_by(user_id=participant_id).all()
    participant_room_ids = [p.room_id for p in participant_rooms]
    
    # Find common rooms
    common_room_ids = set(user_room_ids).intersection(set(participant_room_ids))
    
    for room_id in common_room_ids:
        room = ChatRoom.query.get(room_id)
        if room.is_private and len(room.participants) == 2:
            return jsonify({
                'message': '채팅방이 이미 존재합니다.',
                'room': room.to_dict()
            }), 200
    
    # Create new private room
    room = ChatRoom(is_private=True)
    db.session.add(room)
    db.session.flush()
    
    # Add participants
    user_participant = ChatParticipant(room_id=room.id, user_id=user_id)
    participant_participant = ChatParticipant(room_id=room.id, user_id=participant_id)
    
    db.session.add(user_participant)
    db.session.add(participant_participant)
    db.session.commit()
    
    return jsonify({
        'message': '채팅방이 생성되었습니다.',
        'room': room.to_dict()
    }), 201

@chat_bp.route('/rooms/<int:room_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(room_id):
    user_id = get_jwt_identity()
    
    # Check if user is a participant
    participant = ChatParticipant.query.filter_by(room_id=room_id, user_id=user_id).first()
    if not participant:
        return jsonify({'error': '이 채팅방에 접근할 권한이 없습니다.'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # Get messages
    messages = ChatMessage.query.filter_by(room_id=room_id).order_by(
        ChatMessage.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'messages': [message.to_dict() for message in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    }), 200

@chat_bp.route('/join/global', methods=['POST'])
@jwt_required()
def join_global_chat():
    user_id = get_jwt_identity()
    
    # Find or create global chat room
    global_room = ChatRoom.query.filter_by(name='Global Chat', is_private=False).first()
    
    if not global_room:
        global_room = ChatRoom(name='Global Chat', is_private=False)
        db.session.add(global_room)
        db.session.flush()
    
    # Check if user is already a participant
    participant = ChatParticipant.query.filter_by(room_id=global_room.id, user_id=user_id).first()
    
    if not participant:
        participant = ChatParticipant(room_id=global_room.id, user_id=user_id)
        db.session.add(participant)
        db.session.commit()
    
    return jsonify({
        'message': '전체 채팅방에 참여했습니다.',
        'room': global_room.to_dict()
    }), 200