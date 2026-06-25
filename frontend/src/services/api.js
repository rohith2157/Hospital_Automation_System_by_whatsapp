import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  login: (username, password) => 
    api.post('/auth/login', { username, password }).then(res => res.data),
  
  refreshToken: () => 
    api.post('/auth/refresh').then(res => res.data),
  
  getCurrentUser: () => 
    api.get('/users/me').then(res => res.data), // You might need to create this endpoint
};

// User services
export const userService = {
  getUsers: () => api.get('/users').then(res => res.data),
  createUser: (userData) => api.post('/users', userData).then(res => res.data),
  updateUser: (id, userData) => api.put(`/users/${id}`, userData).then(res => res.data),
  getPermissions: () => api.get('/permissions').then(res => res.data),
};

// Appointment services
export const appointmentService = {
  getAppointments: (params = {}) => 
    api.get('/appointments', { params }).then(res => res.data),
  getAppointment: (id) => 
    api.get(`/appointments/${id}`).then(res => res.data),
  createAppointment: (appointmentData) => 
    api.post('/appointments', appointmentData).then(res => res.data),
  updateAppointment: (id, appointmentData) => 
    api.put(`/appointments/${id}`, appointmentData).then(res => res.data),
  deleteAppointment: (id) => 
    api.delete(`/appointments/${id}`).then(res => res.data),
};

// Patient services
export const patientService = {
  getPatients: () => api.get('/patients').then(res => res.data),
  createPatient: (patientData) => api.post('/patients', patientData).then(res => res.data),
};

// Branch services
export const branchService = {
  getBranches: () => api.get('/branches').then(res => res.data),
  getBranch: (id) => api.get(`/branches/${id}`).then(res => res.data),
};

// Doctor services
export const doctorService = {
  getDoctors: (params = {}) => 
    api.get('/doctors', { params }).then(res => res.data),
  getDoctor: (id) => 
    api.get(`/doctors/${id}`).then(res => res.data),
  createDoctor: (doctorData) => 
    api.post('/doctors', doctorData).then(res => res.data),
  updateDoctor: (id, doctorData) => 
    api.put(`/doctors/${id}`, doctorData).then(res => res.data),
  deleteDoctor: (id) => 
    api.delete(`/doctors/${id}`).then(res => res.data),
};

// Feedback services
export const feedbackService = {
  getFeedback: (params = {}) => 
    api.get('/feedback', { params }).then(res => res.data),
  createFeedback: (feedbackData) => 
    api.post('/feedback', feedbackData).then(res => res.data),
};

// Campaign services
export const campaignService = {
  getCampaigns: () => api.get('/campaigns').then(res => res.data),
  createCampaign: (campaignData) => 
    api.post('/campaigns', campaignData).then(res => res.data),
  sendCampaign: (id) => 
    api.post(`/campaigns/${id}/send`).then(res => res.data),
};

export default api;