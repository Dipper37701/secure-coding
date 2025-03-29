// frontend/renderer/js/auth.js

// Check if user is logged in
async function checkAuth() {
  try {
    const token = await window.api.getToken();
    if (!token) {
      return false;
    }
    
    // Verify token with backend
    const response = await window.apiClient.auth.check();
    
    // Update user data
    await window.api.setUser(response.user);
    
    return true;
  } catch (error) {
    console.error('인증 오류:', error);
    await logout();
    return false;
  }
}

// Login user
async function login(username, password) {
  try {
    const response = await window.apiClient.auth.login({ username, password });
    
    // Save token and user data
    await window.api.setToken(response.token);
    await window.api.setUser(response.user);
    console.log(response.token);
    
    return response.user;
  } catch (error) {
    console.error('로그인 오류:', error);
    throw error;
  }
}

// Register new user
async function register(username, password, description = '') {
  try {
    const response = await window.apiClient.auth.register({
      username,
      password,
      description
    });
    
    // Save token and user data
    await window.api.setToken(response.token);
    await window.api.setUser(response.user);
    
    return response.user;
  } catch (error) {
    console.error('회원가입 오류:', error);
    throw error;
  }
}

// Logout user
async function logout() {
  try {
    // Clear token and user data
    await window.api.clearToken();
    await window.api.clearUser();
    
    // Disconnect socket if connected
    if (window.socketClient) {
      window.socketClient.disconnect();
    }
    
    return true;
  } catch (error) {
    console.error('로그아웃 오류:', error);
    throw error;
  }
}

// Get current user data
async function getCurrentUser() {
  try {
    return await window.api.getUser() || null;
  } catch (error) {
    console.error('사용자 정보 가져오기 오류:', error);
    return null;
  }
}

// Redirect to login page if not authenticated
async function requireAuth() {
  const isAuthenticated = await checkAuth();
  if (!isAuthenticated) {
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

// Redirect to main page if already authenticated
async function requireNoAuth() {
  const isAuthenticated = await checkAuth();
  if (isAuthenticated) {
    window.location.href = 'index.html';
    return false;
  }
  return true;
}

// Set up auth module
window.auth = {
  checkAuth,
  login,
  register,
  logout,
  getCurrentUser,
  requireAuth,
  requireNoAuth
};

// Initialize socket connection if authenticated
async function initializeSocketIfAuthenticated() {
  const token = await window.api.getToken();
  if (token && window.socketClient) {
    try {
      await window.socketClient.initialize(token);
    } catch (error) {
      console.error('소켓 초기화 오류:', error);
    }
  }
}

// Check auth status when page loads
document.addEventListener('DOMContentLoaded', async () => {
  await checkAuth();
  await initializeSocketIfAuthenticated();
});
