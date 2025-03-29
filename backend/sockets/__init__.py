# backend/sockets/__init__.py
def register_socket_events(socketio):
    from .chat import register_chat_events
    register_chat_events(socketio)