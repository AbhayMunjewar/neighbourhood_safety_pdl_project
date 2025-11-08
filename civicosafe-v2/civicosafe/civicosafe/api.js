// API Configuration
const API_BASE_URL = 'http://localhost:3000/api';

// Get authentication token from localStorage
function getAuthToken() {
  return localStorage.getItem('authToken');
}

// Set authentication token
function setAuthToken(token) {
  localStorage.setItem('authToken', token);
}

// Remove authentication token
function removeAuthToken() {
  localStorage.removeItem('authToken');
}

// Make API request with authentication
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAuthToken();

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers
    });

    // Handle non-JSON responses
    let data;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      const text = await response.text();
      throw new Error(`Server returned non-JSON response: ${text.substring(0, 100)}`);
    }

    if (!response.ok) {
      throw new Error(data.message || data.error || `Request failed with status ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error('API Error:', error);
    
    // Provide more helpful error messages
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Cannot connect to server. Make sure the backend is running on http://localhost:3000');
    }
    
    if (error.message) {
      throw error;
    }
    
    throw new Error('Network error: ' + error.message);
  }
}

// Auth API
const authAPI = {
  register: async (name, email, password) => {
    return apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    });
  },

  login: async (email, password) => {
    const response = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    if (response.token) {
      setAuthToken(response.token);
    }
    return response;
  },

  logout: () => {
    removeAuthToken();
    window.location.href = 'login.html';
  },

  getCurrentUser: async () => {
    return apiRequest('/auth/me');
  }
};

// Incidents API
const incidentsAPI = {
  getAll: async () => {
    return apiRequest('/incidents');
  },

  getById: async (id) => {
    return apiRequest(`/incidents/${id}`);
  },

  create: async (incidentData) => {
    return apiRequest('/incidents', {
      method: 'POST',
      body: JSON.stringify(incidentData)
    });
  },

  updateStatus: async (id, status) => {
    return apiRequest(`/incidents/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
  }
};

// Alerts API
const alertsAPI = {
  getAll: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return apiRequest(`/alerts${queryParams ? '?' + queryParams : ''}`);
  },

  create: async (alertData) => {
    return apiRequest('/alerts', {
      method: 'POST',
      body: JSON.stringify(alertData)
    });
  }
};

// Members API
const membersAPI = {
  getAll: async (search = '') => {
    const queryParams = search ? `?search=${encodeURIComponent(search)}` : '';
    return apiRequest(`/members${queryParams}`);
  },

  getById: async (id) => {
    return apiRequest(`/members/${id}`);
  },

  update: async (id, memberData) => {
    return apiRequest(`/members/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(memberData)
    });
  }
};

// Dashboard API
const dashboardAPI = {
  getStats: async () => {
    return apiRequest('/dashboard/stats');
  },

  getActivity: async () => {
    return apiRequest('/dashboard/activity');
  }
};

// Export for use in HTML files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    authAPI,
    incidentsAPI,
    alertsAPI,
    membersAPI,
    dashboardAPI,
    getAuthToken,
    setAuthToken,
    removeAuthToken
  };
}

