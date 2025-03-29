# backend/sockets/chat.py
from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from jwt.exceptions import InvalidTokenError
from models import db, ChatMessage, ChatRoom, ChatParticipant, User

# 사용자 ID를 저장하기 위한 딕셔너리
# key: socket ID, value: user ID
socket_to_user = {}

def register_chat_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        token = request.args.get('token')
        if not token:
            return False
        
        try:
            # Decode token to get user ID
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            
            # Check if user exists and is active
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return False
            
            # Store user ID in the dictionary with socket ID as key
            socket_to_user[request.sid] = user_id
            print(f"User {user_id} connected with socket ID {request.sid}")
            return True
        except InvalidTokenError:
            print("Invalid token during socket connection")
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        # Clean up the mapping when socket disconnects
        if request.sid in socket_to_user:
            print(f"User {socket_to_user[request.sid]} disconnected")
            del socket_to_user[request.sid]
    
    @socketio.on('join')
    def handle_join(data):
        room_id = data.get('room_id')
        if not room_id:
            emit('error', {'message': '채팅방 ID가 필요합니다.'})
            return
        
        # Get user ID from our dictionary using the socket ID
        user_id = socket_to_user.get(request.sid)
        if user_id is None:
            emit('error', {'message': '인증이 필요합니다.'})
            return
        
        # Check if user is a participant
        participant = ChatParticipant.query.filter_by(room_id=room_id, user_id=user_id).first()
        if not participant:
            emit('error', {'message': '이 채팅방에 접근할 권한이 없습니다.'})
            return
        
        # Join room
        join_room(room_id)
        emit('join_success', {'room_id': room_id})
        
        # Notify others
        user = User.query.get(user_id)
        emit('user_joined', {
            'user_id': user_id,
            'username': user.username
        }, room=room_id, include_self=False)
    
    @socketio.on('leave')
    def handle_leave(data):
        room_id = data.get('room_id')
        if not room_id:
            emit('error', {'message': '채팅방 ID가 필요합니다.'})
            return
        
        # Get user ID from our dictionary
        user_id = socket_to_user.get(request.sid)
        if user_id is None:
            emit('error', {'message': '인증이 필요합니다.'})
            return
        
        # Leave room
        leave_room(room_id)
        emit('leave_success', {'room_id': room_id})
        
        # Notify others
        user = User.query.get(user_id)
        emit('user_left', {
            'user_id': user_id,
            'username': user.username
        }, room=room_id)
    
    @socketio.on('message')
    def handle_message(data):
        room_id = data.get('room_id')
        content = data.get('content')
        
        if not room_id or not content:
            emit('error', {'message': '채팅방 ID와 메시지 내용이 필요합니다.'})
            return
        
        # Get user ID from our dictionary
        user_id = socket_to_user.get(request.sid)
        if user_id is None:
            emit('error', {'message': '인증이 필요합니다.'})
            return
        
        # Check if user is a participant
        participant = ChatParticipant.query.filter_by(room_id=room_id, user_id=user_id).first()
        if not participant:
            emit('error', {'message': '이 채팅방에 접근할 권한이 없습니다.'})
            return
        
        # Create message
        message = ChatMessage(
            room_id=room_id,
            sender_id=user_id,
            content=content
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Broadcast message to room
        emit('new_message', message.to_dict(), room=room_id)