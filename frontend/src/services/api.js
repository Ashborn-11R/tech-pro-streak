import axios from 'axios';

const API_BASE_URL = '/api'; // Vite proxy handles this

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  getCurrentUser: () => api.get('/auth/me/'),
  updateProfile: (data) => api.put('/auth/profile/', data),
};

// Dashboard API
export const dashboardAPI = {
  getDashboard: () => api.get('/dashboard/'),
};

// Missions API
export const missionsAPI = {
  getToday: () => api.get('/missions/today/'),
  complete: (data) => api.post('/missions/complete/', data),
  undo: (data) => api.post('/missions/undo/', data),
  getHistory: (limit = 30) => api.get(`/missions/history/?limit=${limit}`),
};

// Streak API
export const streakAPI = {
  getStatus: () => api.get('/streak/status/'),
  getHistory: () => api.get('/streak/history/'),
};

export default api;