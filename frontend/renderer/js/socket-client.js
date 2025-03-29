// frontend/renderer/js/socket-client.js
const SOCKET_URL = 'http://localhost:5000';

let socket = null;
let callbacks = {
  onConnect: () => {},
  onDisconnect: () => {},
  onError: () => {},
  onJoin: () => {},
  onLeave: () => {},
  onMessage: () => {},
  onUserJoined: () => {},
  onUserLeft: () => {}
};

/**
 * Initialize socket connection
 * @param {string} token - JWT token for authentication
 * @returns {Promise} - Promise resolving when connection is established
 */
function initializeSocket(token) {
  return new Promise((resolve, reject) => {
    if (socket) {
      socket.disconnect();
    }
    
    // Create socket connection with authentication token
    socket = io(SOCKET_URL, {
      query: { token }
    });
    
    // Set up event handlers
    socket.on('connect', () => {
      console.log('Socket connected');
      callbacks.onConnect();
      resolve(socket);
    });
    
    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
      callbacks.onError(error);
      reject(error);
    });
    
    socket.on('disconnect', () => {
      console.log('Socket disconnected');
      callbacks.onDisconnect();
    });
    
    socket.on('error', (error) => {
      console.error('Socket error:', error);
      callbacks.onError(error);
    });
    
    socket.on('join_success', (data) => {
      console.log('Joined room:', data.room_id);
      callbacks.onJoin(data);
    });
    
    socket.on('leave_success', (data) => {
      console.log('Left room:', data.room_id);
      callbacks.onLeave(data);
    });
    
    socket.on('new_message', (message) => {
      console.log('New message:', message);
      callbacks.onMessage(message);
    });
    
    socket.on('user_joined', (user) => {
      console.log('User joined:', user);
      callbacks.onUserJoined(user);
    });
    
    socket.on('user_left', (user) => {
      console.log('User left:', user);
      callbacks.onUserLeft(user);
    });
  });
}

/**
 * Disconnect socket
 */
function disconnectSocket() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
}

/**
 * Join a chat room
 * @param {number} roomId - Room ID to join
 */
function joinRoom(roomId) {
  if (socket) {
    socket.emit('join', { room_id: roomId });
  }
}

/**
 * Leave a chat room
 * @param {number} roomId - Room ID to leave
 */
function leaveRoom(roomId) {
  if (socket) {
    socket.emit('leave', { room_id: roomId });
  }
}

/**
 * Send a message to a chat room
 * @param {number} roomId - Room ID to send message to
 * @param {string} content - Message content
 */
function sendMessage(roomId, content) {
  if (socket) {
    socket.emit('message', { room_id: roomId, content });
  }
}

/**
 * Set callbacks for socket events
 * @param {object} newCallbacks - Object containing callback functions
 */
function setCallbacks(newCallbacks) {
  callbacks = { ...callbacks, ...newCallbacks };
}

// Export socket functions
window.socketClient = {
  initialize: initializeSocket,
  disconnect: disconnectSocket,
  joinRoom,
  leaveRoom,
  sendMessage,
  setCallbacks
};
