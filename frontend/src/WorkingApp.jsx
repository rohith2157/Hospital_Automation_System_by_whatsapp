import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

function WorkingApp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [userModules, setUserModules] = useState(['dashboard']);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/auth/login', {
        username,
        password
      });
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        setUser(response.data.user);
        setUserModules(response.data.user.modules || ['dashboard']);
        setLoggedIn(true);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      // Sync users to backend before logging out
      const token = localStorage.getItem('token');
      if (token && users.length > 0) {
        await axios.post('http://localhost:5000/api/sync-users', { users }, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
    } catch (err) {
      console.log('Note: Could not sync users to backend');
    }
    localStorage.removeItem('token');
    setLoggedIn(false);
    setUser(null);
    setUserModules(['dashboard']);
    setUsername('');
    setPassword('');
  };

  const [currentPage, setCurrentPage] = useState('dashboard');
  const [users, setUsers] = useState([
    { id: 1, username: 'rahul', full_name: 'Rahul Kumar', email: 'rahul@hospital.com', role: 'reception', is_active: true, phone: '9876543210', modules: ['dashboard', 'appointments'] },
    { id: 2, username: 'kushal', full_name: 'Kushal Sharma', email: 'kushal@hospital.com', role: 'reception', is_active: true, phone: '9876543211', modules: ['dashboard', 'patients', 'appointments'] },
    { id: 3, username: 'dheeraj', full_name: 'Dheeraj Singh', email: 'dheeraj@hospital.com', role: 'admin', is_active: true, phone: '9876543212', modules: ['dashboard', 'appointments', 'patients', 'doctors', 'users'] },
    { id: 4, username: 'suddhu', full_name: 'Sudhir Patel', email: 'suddhu@hospital.com', role: 'viewer', is_active: false, phone: '9876543213', modules: ['dashboard'] },
    { id: 5, username: 'gopal', full_name: 'Gopal Reddy', email: 'gopal@hospital.com', role: 'reception', is_active: true, phone: '9876543214', modules: ['dashboard', 'patients'] },
    { id: 6, username: 'kumar', full_name: 'Kumar Verma', email: 'kumar@hospital.com', role: 'reception', is_active: true, phone: '9876543215', modules: ['dashboard', 'doctors'] },
    { id: 7, username: 'rohith', full_name: 'Rohith Kumar', email: 'rohith@hospital.com', role: 'superadmin', is_active: true, phone: '9876543216', modules: ['dashboard', 'appointments', 'patients', 'doctors', 'users'] }
  ]);
  const [patients, setPatients] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [selectedAppointments, setSelectedAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({
    totalPatients: 0,
    totalAppointments: 0,
    appointmentsToday: 0
  });
  const [showAddPatientModal, setShowAddPatientModal] = useState(false);
  const [showAddAppointmentModal, setShowAddAppointmentModal] = useState(false);
  const [showAddDoctorModal, setShowAddDoctorModal] = useState(false);
  const [showEditDoctorModal, setShowEditDoctorModal] = useState(false);
  const [newPatient, setNewPatient] = useState({ name: '', phone: '', age: '', gender: 'male' });
  const [newAppointment, setNewAppointment] = useState({ patient: '', patient_phone: '', doctor_id: '', date: '', time: '' });
  const [newDoctor, setNewDoctor] = useState({ name: '', specialization: '', branch_id: 1 });
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [deleting, setDeleting] = useState(null);
  const [showAddPassword, setShowAddPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showResetPassword, setShowResetPassword] = useState(false);
  const [showLoginPassword, setShowLoginPassword] = useState(false);

  // Users page state
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  const [showEditUserModal, setShowEditUserModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [newUser, setNewUser] = useState({ username: '', full_name: '', email: '', role: 'viewer', password: '', confirm_password: '', is_active: true, modules: ['dashboard'] });
  const [editingUser, setEditingUser] = useState(null);
  const [passwordReset, setPasswordReset] = useState('');
  const [selectedUserForPassword, setSelectedUserForPassword] = useState(null);
  
  // Available modules
  const availableModules = ['dashboard', 'appointments', 'patients', 'doctors', 'users'];

  // Load users from localStorage on mount
  useEffect(() => {
    const savedUsers = localStorage.getItem('hospital_users');
    if (savedUsers) {
      try {
        setUsers(JSON.parse(savedUsers));
      } catch (err) {
        console.error('Error loading saved users:', err);
      }
    }
  }, []);

  // Sync current logged-in user data every 5 seconds
  useEffect(() => {
    if (!loggedIn || !user?.username) return;

    const syncCurrentUser = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) return;

        const response = await axios.get(
          `http://localhost:5000/api/current-user/${user.username}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const latestData = response.data;
        
        // Update user state if data changed
        if (JSON.stringify(latestData) !== JSON.stringify(user)) {
          setUser(latestData);
          setUserModules(latestData.modules || ['dashboard']);
        }
      } catch (err) {
        // Silent fail - don't log errors for auto-sync
      }
    };

    // Sync immediately and then every 5 seconds
    syncCurrentUser();
    const interval = setInterval(syncCurrentUser, 5000);
    
    return () => clearInterval(interval);
  }, [loggedIn, user?.username]);

  const handleDeleteAppointment = async (appointmentId) => {
    if (!window.confirm('Are you sure you want to delete this appointment? This action cannot be undone.')) {
      return;
    }

    setDeleting(appointmentId);
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:5000/api/appointments/${appointmentId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Remove from UI immediately
      setAppointments(appointments.filter(apt => apt.id !== appointmentId));
      fetchDashboardStats(); // Update dashboard stats
      alert('Appointment deleted successfully!');
    } catch (err) {
      console.error('Error deleting appointment:', err);
      alert('Failed to delete appointment. Please try again.');
    } finally {
      setDeleting(null);
    }
  };

  const handleBulkDeleteAppointments = async () => {
    if (selectedAppointments.length === 0) return;
    if (!window.confirm(`Are you sure you want to delete ${selectedAppointments.length} appointments? This action cannot be undone.`)) {
      return;
    }

    setDeleting('bulk');
    try {
      const token = localStorage.getItem('token');
      await Promise.all(selectedAppointments.map(id => 
        axios.delete(`http://localhost:5000/api/appointments/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ));
      
      setAppointments(appointments.filter(apt => !selectedAppointments.includes(apt.id)));
      setSelectedAppointments([]);
      fetchDashboardStats();
      alert('Selected appointments deleted successfully!');
    } catch (err) {
      console.error('Error bulk deleting appointments:', err);
      alert('Failed to delete some appointments. Please try again.');
      fetchAppointments();
    } finally {
      setDeleting(null);
    }
  };

  // User Management Functions
  const handleAddUser = async (e) => {
    e.preventDefault();
    if (newUser.password !== newUser.confirm_password) {
      alert('Passwords do not match!');
      return;
    }
    try {
      const token = localStorage.getItem('token');
      // Only send fields that backend expects
      const userPayload = {
        username: newUser.username,
        full_name: newUser.full_name,
        email: newUser.email,
        role: newUser.role,
        password: newUser.password,
        is_active: newUser.is_active,
        modules: newUser.modules || ['dashboard']
      };
      const response = await api.post('/users', userPayload, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Add to local state with the new ID
      const newUserData = {
        id: response.data.id || users.length + 1,
        username: newUser.username,
        full_name: newUser.full_name,
        email: newUser.email,
        role: newUser.role,
        is_active: newUser.is_active,
        modules: newUser.modules || ['dashboard'],
        phone: ''
      };
      const updatedUsers = [...users, newUserData];
      setUsers(updatedUsers);
      // Save to localStorage
      localStorage.setItem('hospital_users', JSON.stringify(updatedUsers));
      setShowAddUserModal(false);
      setNewUser({ username: '', full_name: '', email: '', role: 'viewer', password: '', confirm_password: '', is_active: true, modules: ['dashboard'] });
      alert('User created successfully!');
    } catch (err) {
      console.error('Error adding user:', err);
      const errorMsg = err.response?.data?.message || err.message || 'Unknown error';
      console.error('Detailed error:', errorMsg, err.response?.data);
      alert('Failed to add user: ' + errorMsg);
    }
  };

  const handleEditUser = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await api.put(`/users/${editingUser.id}`, editingUser, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Update local state
      const updatedUsers = users.map(u => u.id === editingUser.id ? editingUser : u);
      setUsers(updatedUsers);
      // Save to localStorage
      localStorage.setItem('hospital_users', JSON.stringify(updatedUsers));
      setShowEditUserModal(false);
      setEditingUser(null);
      alert('User updated successfully in database!');
    } catch (err) {
      console.error('Error updating user:', err);
      const errorMsg = err.response?.data?.message || err.message || 'Unknown error';
      alert('Failed to update user: ' + errorMsg);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return;
    }
    try {
      const token = localStorage.getItem('token');
      await api.delete(`/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const updatedUsers = users.filter(u => u.id !== userId);
      setUsers(updatedUsers);
      // Save to localStorage
      alert('User deleted successfully from database!');
    } catch (err) {
      console.error('Error deleting user:', err);
      const errorMsg = err.response?.data?.message || err.message || 'Unknown error';
      alert('Failed to delete user: ' + errorMsg);
    }
  };

  const handleResetPassword = async () => {
    if (passwordReset.length < 6) {
      alert('Password must be at least 6 characters!');
      return;
    }
    try {
      const token = localStorage.getItem('token');
      await api.put(`/users/${selectedUserForPassword.id}`, { password: passwordReset }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Update local state with new password
      const updatedUsers = users.map(u => 
        u.id === selectedUserForPassword.id ? { ...u, password: passwordReset } : u
      );
      setUsers(updatedUsers);
      // Save to localStorage
      localStorage.setItem('hospital_users', JSON.stringify(updatedUsers));
      setShowPasswordModal(false);
      setPasswordReset('');
      setSelectedUserForPassword(null);
      alert('Password reset successfully in database!');
    } catch (err) {
      console.error('Error resetting password:', err);
      const errorMsg = err.response?.data?.message || err.message || 'Unknown error';
      alert('Failed to reset password: ' + errorMsg);
    }
  };

  const handleToggleUserStatus = async (user) => {
    try {
      const token = localStorage.getItem('token');
      await api.put(`/users/${user.id}`, { is_active: !user.is_active }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Update local state from database
      const updatedUsers = users.map(u => u.id === user.id ? {...u, is_active: !u.is_active} : u);
      setUsers(updatedUsers);
      localStorage.setItem('hospital_users', JSON.stringify(updatedUsers));
    } catch (err) {
      console.error('Error toggling user status:', err);
      const errorMsg = err.response?.data?.message || err.message || 'Unknown error';
      alert('Failed to toggle user status: ' + errorMsg);
    }
  };

  const openEditUserModal = (user) => {
    setEditingUser({ ...user });
    setShowEditUserModal(true);
  };

  const filteredUsers = users.filter(u => {
    const matchSearch = searchTerm === '' || 
      u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.full_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.email || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchRole = roleFilter === '' || u.role === roleFilter;
    return matchSearch && matchRole;
  });

  const fetchDashboardStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/dashboard/summary', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDashboardStats(response.data);
    } catch (err) {
      console.error('Error fetching dashboard stats:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await api.get('/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
      // Update localStorage cache from database
      localStorage.setItem('hospital_users', JSON.stringify(response.data));
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const fetchPatients = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/patients', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPatients(response.data);
    } catch (err) {
      console.error('Error fetching patients:', err);
    }
  };

  const fetchAppointments = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/appointments', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAppointments(response.data);
    } catch (err) {
      console.error('Error fetching appointments:', err);
    }
  };

  const fetchDoctors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/doctors', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDoctors(response.data);
    } catch (err) {
      console.error('Error fetching doctors:', err);
    }
  };

  const handleAddDoctor = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:5000/api/doctors', newDoctor, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowAddDoctorModal(false);
      setNewDoctor({ name: '', specialization: '', branch_id: 1 });
      fetchDoctors();
    } catch (err) {
      console.error('Error adding doctor:', err);
      alert('Failed to add doctor. Please try again.');
    }
  };

  const handleEditDoctor = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.put(`http://localhost:5000/api/doctors/${editingDoctor.id}`, editingDoctor, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowEditDoctorModal(false);
      setEditingDoctor(null);
      fetchDoctors();
    } catch (err) {
      console.error('Error updating doctor:', err);
      alert('Failed to update doctor. Please try again.');
    }
  };

  const handleDeleteDoctor = async (doctorId) => {
    if (!window.confirm('Are you sure you want to delete this doctor?')) {
      return;
    }
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:5000/api/doctors/${doctorId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchDoctors();
    } catch (err) {
      console.error('Error deleting doctor:', err);
      alert('Failed to delete doctor. Please try again.');
    }
  };

  const openEditDoctorModal = (doctor) => {
    setEditingDoctor({ ...doctor });
    setShowEditDoctorModal(true);
  };

  const handleAddPatient = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:5000/api/patients', newPatient, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowAddPatientModal(false);
      setNewPatient({ name: '', phone: '', age: '', gender: 'male' });
      fetchPatients();
      fetchDashboardStats();
    } catch (err) {
      console.error('Error adding patient:', err);
    }
  };

  const handleAddAppointment = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      
      // Transform data to match backend API requirements
      const appointmentData = {
        patient_name: newAppointment.patient,
        patient_phone: newAppointment.patient_phone,
        doctor_id: parseInt(newAppointment.doctor_id),
        scheduled_at: `${newAppointment.date}T${newAppointment.time}:00`,
        source: 'admin'
      };
      
      await axios.post('http://localhost:5000/api/appointments', appointmentData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowAddAppointmentModal(false);
      setNewAppointment({ patient: '', patient_phone: '', doctor_id: '', date: '', time: '' });
      fetchAppointments();
      fetchDashboardStats();
    } catch (err) {
      console.error('Error adding appointment:', err);
      alert('Failed to create appointment. Please check all fields.');
    }
  };

  React.useEffect(() => {
    if (loggedIn) {
      fetchDashboardStats();
      if (currentPage === 'appointments') fetchAppointments();
      if (currentPage === 'patients') fetchPatients();
      if (currentPage === 'doctors') fetchDoctors();
      if (currentPage === 'users') fetchUsers();
    }
  }, [loggedIn, currentPage]);

  if (loggedIn && user) {
    return (
      <div className="min-h-screen bg-gray-100 flex">
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-lg">
          <div className="p-4 border-b">
            <h1 className="text-xl font-bold text-blue-600">Clinic Manager</h1>
          </div>
          <nav className="p-4">
            <ul className="space-y-2">
              {userModules.includes('dashboard') && (
                <li>
                  <button
                    onClick={() => setCurrentPage('dashboard')}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      currentPage === 'dashboard'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    📊 Dashboard
                  </button>
                </li>
              )}
              {userModules.includes('appointments') && (
                <li>
                  <button
                    onClick={() => setCurrentPage('appointments')}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      currentPage === 'appointments'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    📅 Appointments
                  </button>
                </li>
              )}
              {userModules.includes('patients') && (
                <li>
                  <button
                    onClick={() => setCurrentPage('patients')}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      currentPage === 'patients'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    👥 Patients
                  </button>
                </li>
              )}
              {userModules.includes('doctors') && (
                <li>
                  <button
                    onClick={() => setCurrentPage('doctors')}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      currentPage === 'doctors'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    👨‍⚕️ Doctors
                  </button>
                </li>
              )}
              {userModules.includes('users') && (
                <li>
                  <button
                    onClick={() => {
                      setCurrentPage('users');
                      setTimeout(() => fetchUsers(), 0);
                    }}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      currentPage === 'users'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    👤 Users
                  </button>
                </li>
              )}
            </ul>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          <header className="bg-white shadow-sm border-b">
            <div className="flex items-center justify-between px-6 py-4">
              <div>
                <h2 className="text-2xl font-semibold text-gray-800">
                  Welcome back, {user.full_name || user.username}!
                </h2>
                <p className="text-gray-600 capitalize">{user.role}</p>
              </div>
              <div className="flex gap-3">
                <button 
                  onClick={() => {
                    if (currentPage === 'dashboard') fetchDashboardStats();
                    if (currentPage === 'appointments') fetchAppointments();
                    if (currentPage === 'patients') fetchPatients();
                    if (currentPage === 'doctors') fetchDoctors();
                    if (currentPage === 'users') fetchUsers();
                  }} 
                  className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors shadow-sm flex items-center gap-2"
                  title="Refresh Data"
                >
                  <span className="text-sm">🔄</span> Refresh
                </button>
                <button onClick={handleLogout} className="btn-secondary">
                  Logout
                </button>
              </div>
            </div>
          </header>
          
          <main className="flex-1 overflow-auto p-6">
            <div className="max-w-7xl mx-auto">
              {currentPage === 'dashboard' && userModules.includes('dashboard') && (
                <>
                  {/* Stats Cards - Show based on role */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    {/* Total Patients - Show for Admin, Reception, Doctors can view */}
                    {(user.role === 'superadmin' || user.role === 'admin' || user.role === 'reception') && (
                      <div className="card p-6 bg-gradient-to-br from-blue-50 to-blue-100">
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Patients</h3>
                        <p className="text-3xl font-bold text-blue-600">{dashboardStats.totalPatients}</p>
                        <p className="text-sm text-gray-500 mt-2">Registered patients</p>
                      </div>
                    )}
                    
                    {/* Appointments Today - Show for Admin, Reception, Doctors */}
                    {(user.role === 'superadmin' || user.role === 'admin' || user.role === 'reception') && (
                      <div className="card p-6 bg-gradient-to-br from-green-50 to-green-100">
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Appointments Today</h3>
                        <p className="text-3xl font-bold text-green-600">{dashboardStats.appointmentsToday}</p>
                        <p className="text-sm text-gray-500 mt-2">Today's schedule</p>
                      </div>
                    )}
                    
                    {/* Total Appointments - Show for all */}
                    <div className="card p-6 bg-gradient-to-br from-purple-50 to-purple-100">
                      <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Appointments</h3>
                      <p className="text-3xl font-bold text-purple-600">{dashboardStats.totalAppointments}</p>
                      <p className="text-sm text-gray-500 mt-2">All appointments</p>
                    </div>
                  </div>
                  
                  {/* Welcome Card */}
                  <div className="card p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                    <h3 className="text-2xl font-semibold mb-2">Welcome, {user.full_name || user.username}! 👋</h3>
                    <p className="text-blue-100">
                      You're logged in as <strong>{user.role.toUpperCase()}</strong>. 
                      {user.role === 'superadmin' && " You have full access to all features."}
                      {user.role === 'admin' && " You can manage users, appointments, and patients."}
                      {(user.role === 'viewer' || user.role === 'reception') && " You can view and manage your assigned tasks."}
                      {user.role === 'reception' && " You can manage patient records and appointments."}
                    </p>
                  </div>
                  
                  {/* Role-specific info */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                    <div className="card p-6">
                      <h3 className="text-lg font-semibold text-gray-800 mb-3">📊 Quick Stats</h3>
                      <ul className="space-y-2 text-gray-600">
                        <li>✓ Total Patients: <span className="font-semibold">{dashboardStats.totalPatients}</span></li>
                        <li>✓ Appointments: <span className="font-semibold">{dashboardStats.totalAppointments}</span></li>
                        {(user.role === 'superadmin' || user.role === 'admin') && (
                          <li>✓ Role: <span className="font-semibold capitalize">{user.role}</span></li>
                        )}
                      </ul>
                    </div>
                    
                    <div className="card p-6">
                      <h3 className="text-lg font-semibold text-gray-800 mb-3">🔐 Your Modules</h3>
                      <div className="flex flex-wrap gap-2">
                        {userModules.map(module => (
                          <span key={module} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium capitalize">
                            {module}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </>
              )}

              {currentPage === 'users' && (
                <div className="card p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-gray-800">User Management</h3>
                    <button
                      onClick={() => setShowAddUserModal(true)}
                      className="btn-primary"
                    >
                      + Add User
                    </button>
                  </div>

                  {/* Search and Filter */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <input
                      type="text"
                      placeholder="Search by username, name, or email..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="input-field"
                    />
                    <select
                      value={roleFilter}
                      onChange={(e) => setRoleFilter(e.target.value)}
                      className="input-field"
                    >
                      <option value="">All Roles</option>
                      <option value="admin">Admin</option>
                      <option value="superadmin">Superadmin</option>
                      <option value="campaign">Campaign</option>
                      <option value="reception">Reception</option>
                      <option value="viewer">Viewer</option>
                    </select>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Full Name</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {filteredUsers.length === 0 ? (
                          <tr>
                            <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
                              {users.length === 0 ? (
                                <span>No users found</span>
                              ) : (
                                <span>No users found matching your search</span>
                              )}
                            </td>
                          </tr>
                        ) : (
                          filteredUsers.map((u) => (
                            <tr key={u.id} className="hover:bg-gray-50">
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">@{u.username}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{u.full_name || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{u.email || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 capitalize">
                                  {u.role}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <button
                                  onClick={() => handleToggleUserStatus(u)}
                                  className="cursor-pointer"
                                >
                                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                  }`}>
                                    {u.is_active ? '✓ Active' : '✗ Inactive'}
                                  </span>
                                </button>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                                <button
                                  onClick={() => openEditUserModal(u)}
                                  className="text-blue-600 hover:text-blue-900"
                                  title="Edit"
                                >
                                  ✏️
                                </button>
                                <button
                                  onClick={() => {
                                    setSelectedUserForPassword(u);
                                    setShowPasswordModal(true);
                                  }}
                                  className="text-orange-600 hover:text-orange-900"
                                  title="Reset Password"
                                >
                                  🔐
                                </button>
                                <button
                                  onClick={() => handleDeleteUser(u.id)}
                                  className="text-red-600 hover:text-red-900"
                                  title="Delete"
                                >
                                  🗑️
                                </button>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {currentPage === 'appointments' && (
                <div className="card p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-gray-800">Appointments</h3>
                    <div className="flex gap-2">
                      {selectedAppointments.length > 0 && (
                        <button
                          onClick={handleBulkDeleteAppointments}
                          disabled={deleting === 'bulk'}
                          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition disabled:opacity-50 flex items-center gap-2"
                        >
                          {deleting === 'bulk' ? 'Deleting...' : `🗑️ Delete Selected (${selectedAppointments.length})`}
                        </button>
                      )}
                      <button
                        onClick={() => {
                          setShowAddAppointmentModal(true);
                          fetchDoctors();
                        }}
                        className="btn-primary"
                      >
                        + Add Appointment
                      </button>
                    </div>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase w-12">
                            <input
                              type="checkbox"
                              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                              checked={appointments.length > 0 && selectedAppointments.length === appointments.length}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setSelectedAppointments(appointments.map(apt => apt.id));
                                } else {
                                  setSelectedAppointments([]);
                                }
                              }}
                            />
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patient</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Doctor</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {appointments.length === 0 ? (
                          <tr>
                            <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                              <span>No appointments found</span>
                            </td>
                          </tr>
                        ) : (
                          appointments.map((apt) => (
                            <tr key={apt.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-center">
                                <input
                                  type="checkbox"
                                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                  checked={selectedAppointments.includes(apt.id)}
                                  onChange={(e) => {
                                    if (e.target.checked) {
                                      setSelectedAppointments([...selectedAppointments, apt.id]);
                                    } else {
                                      setSelectedAppointments(selectedAppointments.filter(id => id !== apt.id));
                                    }
                                  }}
                                />
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{apt.patient}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{apt.doctor}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{apt.date}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{apt.time}</td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                  apt.status === 'booked' ? 'bg-green-100 text-green-800' :
                                  apt.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                                  'bg-gray-100 text-gray-800'
                                }`}>
                                  {apt.status}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button
                                  onClick={() => handleDeleteAppointment(apt.id)}
                                  disabled={deleting === apt.id}
                                  className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition"
                                  title="Delete appointment"
                                >
                                  {deleting === apt.id ? 'Deleting...' : '🗑️ Delete'}
                                </button>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {currentPage === 'patients' && (
                <div className="card p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-gray-800">Patients</h3>
                    <button
                      onClick={() => setShowAddPatientModal(true)}
                      className="btn-primary"
                    >
                      + Add Patient
                    </button>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gender</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Visit</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {patients.length === 0 ? (
                          <tr>
                            <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                              <span>No patients found</span>
                            </td>
                          </tr>
                        ) : (
                          patients.map((p) => (
                            <tr key={p.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{p.name}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.phone}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.age || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">{p.gender || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.last_visit || '-'}</td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {currentPage === 'doctors' && (
                <div className="card p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-gray-800">Doctors</h3>
                    <button
                      onClick={() => setShowAddDoctorModal(true)}
                      className="btn-primary flex items-center gap-2"
                    >
                      <span>+</span> Add Doctor
                    </button>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Specialization</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Branch ID</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {doctors.length === 0 ? (
                          <tr>
                            <td colSpan="4" className="px-6 py-4 text-center text-gray-500">
                              <span>No doctors found</span>
                            </td>
                          </tr>
                        ) : (
                          doctors.map((doc) => (
                            <tr key={doc.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{doc.name}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.specialization || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.branch_id || '-'}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm">
                                <button
                                  onClick={() => openEditDoctorModal(doc)}
                                  className="text-blue-600 hover:text-blue-900 mr-3"
                                >
                                  ✏️ Edit
                                </button>
                                <button
                                  onClick={() => handleDeleteDoctor(doc.id)}
                                  className="text-red-600 hover:text-red-900"
                                >
                                  🗑️ Delete
                                </button>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </main>
        </div>

        {/* Add Patient Modal */}
        {showAddPatientModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-xl font-semibold mb-4">Add New Patient</h3>
              <form onSubmit={handleAddPatient} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input
                    type="text"
                    required
                    value={newPatient.name}
                    onChange={(e) => setNewPatient({...newPatient, name: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input
                    type="text"
                    required
                    value={newPatient.phone}
                    onChange={(e) => setNewPatient({...newPatient, phone: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                  <input
                    type="number"
                    value={newPatient.age}
                    onChange={(e) => setNewPatient({...newPatient, age: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                  <select
                    value={newPatient.gender}
                    onChange={(e) => setNewPatient({...newPatient, gender: e.target.value})}
                    className="input-field"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setShowAddPatientModal(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Patient
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Add Appointment Modal */}
        {showAddAppointmentModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-xl font-semibold mb-4">Add New Appointment</h3>
              <form onSubmit={handleAddAppointment} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Patient Name</label>
                  <input
                    type="text"
                    required
                    value={newAppointment.patient}
                    onChange={(e) => setNewAppointment({...newAppointment, patient: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Patient Phone <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    required
                    placeholder="8333035340"
                    pattern="[0-9]{10}"
                    title="Please enter a valid 10-digit phone number"
                    value={newAppointment.patient_phone || ''}
                    onChange={(e) => setNewAppointment({...newAppointment, patient_phone: e.target.value})}
                    className="input-field"
                  />
                  <p className="text-xs text-gray-500 mt-1">Enter 10-digit mobile number (without +91)</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Doctor</label>
                  <select
                    required
                    value={newAppointment.doctor_id}
                    onChange={(e) => setNewAppointment({...newAppointment, doctor_id: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Select Doctor</option>
                    {doctors.map((doc) => (
                      <option key={doc.id} value={doc.id}>{doc.name} - {doc.specialization}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                  <input
                    type="date"
                    required
                    value={newAppointment.date}
                    onChange={(e) => setNewAppointment({...newAppointment, date: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
                  <input
                    type="time"
                    required
                    value={newAppointment.time}
                    onChange={(e) => setNewAppointment({...newAppointment, time: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setShowAddAppointmentModal(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Appointment
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Add Doctor Modal */}
        {showAddDoctorModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-xl font-semibold mb-4">Add New Doctor</h3>
              <form onSubmit={handleAddDoctor} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Doctor Name</label>
                  <input
                    type="text"
                    required
                    value={newDoctor.name}
                    onChange={(e) => setNewDoctor({...newDoctor, name: e.target.value})}
                    className="input-field"
                    placeholder="Dr. John Smith"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Specialization</label>
                  <input
                    type="text"
                    required
                    value={newDoctor.specialization}
                    onChange={(e) => setNewDoctor({...newDoctor, specialization: e.target.value})}
                    className="input-field"
                    placeholder="Cardiologist, Pediatrician, etc."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Branch ID</label>
                  <input
                    type="number"
                    value={newDoctor.branch_id}
                    onChange={(e) => setNewDoctor({...newDoctor, branch_id: parseInt(e.target.value) || 1})}
                    className="input-field"
                    min="1"
                  />
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddDoctorModal(false);
                      setNewDoctor({ name: '', specialization: '', branch_id: 1 });
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Doctor
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Edit Doctor Modal */}
        {showEditDoctorModal && editingDoctor && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-xl font-semibold mb-4">Edit Doctor</h3>
              <form onSubmit={handleEditDoctor} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Doctor Name</label>
                  <input
                    type="text"
                    required
                    value={editingDoctor.name}
                    onChange={(e) => setEditingDoctor({...editingDoctor, name: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Specialization</label>
                  <input
                    type="text"
                    required
                    value={editingDoctor.specialization || ''}
                    onChange={(e) => setEditingDoctor({...editingDoctor, specialization: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Branch ID</label>
                  <input
                    type="number"
                    value={editingDoctor.branch_id || 1}
                    onChange={(e) => setEditingDoctor({...editingDoctor, branch_id: parseInt(e.target.value) || 1})}
                    className="input-field"
                    min="1"
                  />
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowEditDoctorModal(false);
                      setEditingDoctor(null);
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Add User Modal */}
        {showAddUserModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
              <h3 className="text-xl font-semibold mb-4">Add New User</h3>
              <form onSubmit={handleAddUser} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                  <input
                    type="text"
                    required
                    value={newUser.username}
                    onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                    className="input-field"
                    placeholder="johndoe"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={newUser.full_name}
                    onChange={(e) => setNewUser({...newUser, full_name: e.target.value})}
                    className="input-field"
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    required
                    value={newUser.email}
                    onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                    className="input-field"
                    placeholder="john@hospital.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                  <select
                    value={newUser.role}
                    onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                    className="input-field"
                  >
                    <option value="viewer">Viewer</option>
                    <option value="admin">Admin</option>
                    <option value="reception">Reception</option>
                    <option value="campaign">Campaign</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div className="relative">
                    <input
                      type={showAddPassword ? "text" : "password"}
                      required
                      value={newUser.password}
                      onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                      className="input-field pr-10"
                      placeholder="••••••••"
                      minLength="6"
                    />
                    <button
                      type="button"
                      onClick={() => setShowAddPassword(!showAddPassword)}
                      className="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
                    >
                      {showAddPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                  <div className="relative">
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      required
                      value={newUser.confirm_password}
                      onChange={(e) => setNewUser({...newUser, confirm_password: e.target.value})}
                      className="input-field pr-10"
                      placeholder="••••••••"
                      minLength="6"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
                    >
                      {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Assign Modules</label>
                  <div className="space-y-2 bg-gray-50 p-3 rounded">
                    {availableModules.map(module => (
                      <div key={module} className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id={`add_${module}`}
                          checked={newUser.modules?.includes(module) || false}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setNewUser({...newUser, modules: [...(newUser.modules || []), module]});
                            } else {
                              setNewUser({...newUser, modules: (newUser.modules || []).filter(m => m !== module)});
                            }
                          }}
                          className="w-4 h-4"
                        />
                        <label htmlFor={`add_${module}`} className="text-sm text-gray-700 capitalize cursor-pointer">
                          {module}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={newUser.is_active}
                    onChange={(e) => setNewUser({...newUser, is_active: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <label className="text-sm text-gray-700">Active</label>
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddUserModal(false);
                      setNewUser({ username: '', full_name: '', email: '', role: 'viewer', password: '', confirm_password: '', is_active: true, modules: ['dashboard'] });
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add User
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Edit User Modal */}
        {showEditUserModal && editingUser && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
              <h3 className="text-xl font-semibold mb-4">Edit User</h3>
              <form onSubmit={handleEditUser} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Username (Read-only)</label>
                  <input
                    type="text"
                    value={editingUser.username}
                    disabled
                    className="input-field bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={editingUser.full_name || ''}
                    onChange={(e) => setEditingUser({...editingUser, full_name: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    required
                    value={editingUser.email || ''}
                    onChange={(e) => setEditingUser({...editingUser, email: e.target.value})}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                  <select
                    value={editingUser.role || 'viewer'}
                    onChange={(e) => setEditingUser({...editingUser, role: e.target.value})}
                    className="input-field"
                  >
                    <option value="viewer">Viewer</option>
                    <option value="admin">Admin</option>
                    <option value="reception">Reception</option>
                    <option value="campaign">Campaign</option>
                    <option value="superadmin">Superadmin</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Assign Modules</label>
                  <div className="space-y-2 bg-gray-50 p-3 rounded">
                    {availableModules.map(module => (
                      <div key={module} className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id={`edit_${module}`}
                          checked={editingUser.modules?.includes(module) || false}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setEditingUser({...editingUser, modules: [...(editingUser.modules || []), module]});
                            } else {
                              setEditingUser({...editingUser, modules: (editingUser.modules || []).filter(m => m !== module)});
                            }
                          }}
                          className="w-4 h-4"
                        />
                        <label htmlFor={`edit_${module}`} className="text-sm text-gray-700 capitalize cursor-pointer">
                          {module}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={editingUser.is_active !== false}
                    onChange={(e) => setEditingUser({...editingUser, is_active: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <label className="text-sm text-gray-700">Active</label>
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowEditUserModal(false);
                      setEditingUser(null);
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Update User
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Reset Password Modal */}
        {showPasswordModal && selectedUserForPassword && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
              <h3 className="text-xl font-semibold mb-4">Reset Password - @{selectedUserForPassword.username}</h3>
              <div className="space-y-4">
                <p className="text-gray-600">Enter new password for <strong>{selectedUserForPassword.full_name}</strong></p>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                  <div className="relative">
                    <input
                      type={showResetPassword ? "text" : "password"}
                      required
                      value={passwordReset}
                      onChange={(e) => setPasswordReset(e.target.value)}
                      className="input-field pr-10"
                      placeholder="••••••••"
                      minLength="6"
                    />
                    <button
                      type="button"
                      onClick={() => setShowResetPassword(!showResetPassword)}
                      className="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
                    >
                      {showResetPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                  <p className="text-sm text-yellow-800">⚠️ The user will need to use this new password to log in next time.</p>
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowPasswordModal(false);
                      setPasswordReset('');
                      setSelectedUserForPassword(null);
                    }}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleResetPassword}
                    className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700"
                  >
                    Reset Password
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full p-8 bg-white rounded-lg shadow-md">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Clinic Management System
          </h2>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              id="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-field"
              placeholder="Enter your username"
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                type={showLoginPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field pr-10"
                placeholder="Enter your password"
                disabled={loading}
              />
              <button
                type="button"
                onClick={() => setShowLoginPassword(!showLoginPassword)}
                className="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
                disabled={loading}
              >
                {showLoginPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <div className="mt-4 text-center text-sm text-gray-500">
          <p>Default credentials:</p>
          <p>Username: <strong>admin</strong> | Password: <strong>********</strong></p>
        </div>
      </div>
    </div>
  );
}

export default WorkingApp;
