const API_BASE_URL = 'http://localhost:5000/api';
/**
 * Base API function for making requests
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {object} data - Request data
 * @param {boolean} auth - Whether to include auth token
 * @param {FormData} formData - Form data for file uploads
 * @returns {Promise} - Promise resolving to response data
 */
async function send_api(endpoint, method = 'GET', data = null, auth = false, formData = null) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers = {
    'Accept': 'application/json'
  };
  
  if (!formData) {
    headers['Content-Type'] = 'application/json';
  }
  
  if (auth) {
    const token = await window.api.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  
  const options = {
    method,
    headers
  };
  
  if (data && !formData) {
    options.body = JSON.stringify(data);
  } else if (formData) {
    options.body = formData;
    // Don't set Content-Type for FormData, browser will set it with boundary
    delete headers['Content-Type'];
  }
  
  try {
    const response = await fetch(url, options);
    const responseData = await response.json();
    
    if (!response.ok) {
      throw new Error(responseData.error || 'API 요청 실패');
    }
    
    return responseData;
  } catch (error) {
    console.error('API 오류:', error);
    throw error;
  }
}

/**
 * Authentication API
 */
const authApi = {
  // Register new user
  register: (userData) => {
    return send_api('/auth/register', 'POST', userData);
  },
  
  // Login user
  login: (credentials) => {
    return send_api('/auth/login', 'POST', credentials);
  },
  
  // Check authentication status
  check: () => {
    return send_api('/auth/check', 'GET', null, true);
  }
};

/**
 * Users API
 */
const userApi = {
  // Get user by ID
  getUser: (userId) => {
    return send_api(`/users/${userId}`, 'GET');
  },
  
  // Get current user profile
  getProfile: () => {
    return send_api('/users/profile', 'GET', null, true);
  },
  
  // Update current user profile
  updateProfile: (userData) => {
    return send_api('/users/profile', 'PUT', userData, true);
  }
};

/**
 * Products API
 */
const productApi = {
  // Get all products
  getProducts: (page = 1, perPage = 20) => {
    return send_api(`/products?page=${page}&per_page=${perPage}`, 'GET');
  },
  
  // Get product by ID
  getProduct: (productId) => {
    return send_api(`/products/${productId}`, 'GET');
  },
  
  // Create new product
  createProduct: (productData, image = null) => {
    if (image) {
      const formData = new FormData();
      
      // Add product data to form
      Object.keys(productData).forEach(key => {
        formData.append(key, productData[key]);
      });
      
      // Add image to form
      formData.append('image', image);
      
      return send_api('/products', 'POST', null, true, formData);
    } else {
      return send_api('/products', 'POST', productData, true);
    }
  },
  
  // Update product
  updateProduct: (productId, productData, image = null) => {
    if (image) {
      const formData = new FormData();
      
      // Add product data to form
      Object.keys(productData).forEach(key => {
        formData.append(key, productData[key]);
      });
      
      // Add image to form
      formData.append('image', image);
      
      return send_api(`/products/${productId}`, 'PUT', null, true, formData);
    } else {
      return send_api(`/products/${productId}`, 'PUT', productData, true);
    }
  },
  
  // Delete product
  deleteProduct: (productId) => {
    return send_api(`/products/${productId}`, 'DELETE', null, true);
  },
  
  // Get current user's products
  getUserProducts: (page = 1, perPage = 20) => {
    return send_api(`/products/user?page=${page}&per_page=${perPage}`, 'GET', null, true);
  }
};

/**
 * Chat API
 */
const chatApi = {
  // Get all chat rooms for current user
  getChatRooms: () => {
    return send_api('/chats/rooms', 'GET', null, true);
  },
  
  // Get global chat room
  getGlobalChat: () => {
    return send_api('/chats/rooms/global', 'GET', null, true);
  },
  
  // Create private chat with user
  createPrivateChat: (participantId) => {
    return send_api('/chats/rooms', 'POST', { participant_id: participantId }, true);
  },
  
  // Get messages for a chat room
  getMessages: (roomId, page = 1, perPage = 50) => {
    return send_api(`/chats/rooms/${roomId}/messages?page=${page}&per_page=${perPage}`, 'GET', null, true);
  },
  
  // Join global chat
  joinGlobalChat: () => {
    return send_api('/chats/join/global', 'POST', {}, true);
  }
};

/**
 * Report API
 */
const reportApi = {
  // Report a user
  reportUser: (targetId, reason) => {
    return send_api(`/reports/user/${targetId}`, 'POST', { reason }, true);
  },
  
  // Report a product
  reportProduct: (productId, reason) => {
    return send_api(`/reports/product/${productId}`, 'POST', { reason }, true);
  }
};

// Export API modules
window.apiClient = {
  auth: authApi,
  user: userApi,
  product: productApi,
  chat: chatApi,
  report: reportApi
};
