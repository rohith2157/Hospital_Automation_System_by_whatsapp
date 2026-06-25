import React, { useState, useEffect } from 'react';
import StatsCards from '../components/dashboard/StatsCards';
import { appointmentService, patientService, feedbackService } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [appointmentsData, setAppointmentsData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch recent data for dashboard
        const [appointments, patients, feedback] = await Promise.all([
          appointmentService.getAppointments(),
          patientService.getPatients(),
          feedbackService.getFeedback()
        ]);

        // Calculate stats
        const totalAppointments = appointments.length;
        const totalPatients = patients.length;
        const averageRating = feedback.length > 0 
          ? feedback.reduce((acc, curr) => acc + (curr.rating || 0), 0) / feedback.length
          : 0;
        const pendingFeedback = appointments.filter(apt => 
          apt.status === 'completed' && !feedback.find(fb => fb.appointment_id === apt.id)
        ).length;

        setStats({
          totalAppointments,
          totalPatients,
          averageRating,
          pendingFeedback
        });

        // Prepare chart data (appointments by status)
        const statusCount = appointments.reduce((acc, appointment) => {
          acc[appointment.status] = (acc[appointment.status] || 0) + 1;
          return acc;
        }, {});

        const chartData = Object.keys(statusCount).map(status => ({
          status: status.charAt(0).toUpperCase() + status.slice(1),
          count: statusCount[status]
        }));

        setAppointmentsData(chartData);

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to your clinic management dashboard</p>
      </div>

      <StatsCards stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Appointments by Status</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={appointmentsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="status" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-4">
            <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <h4 className="font-medium text-gray-900">Schedule New Appointment</h4>
              <p className="text-sm text-gray-600">Book a new patient appointment</p>
            </button>
            <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <h4 className="font-medium text-gray-900">Add New Patient</h4>
              <p className="text-sm text-gray-600">Register a new patient</p>
            </button>
            <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <h4 className="font-medium text-gray-900">View Today's Appointments</h4>
              <p className="text-sm text-gray-600">Check today's schedule</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;