import React from 'react';
import { Users, Calendar, Star, MessageSquare } from 'lucide-react';

const StatsCards = ({ stats }) => {
  const statItems = [
    {
      label: 'Total Appointments',
      value: stats?.totalAppointments || 0,
      icon: Calendar,
      color: 'blue'
    },
    {
      label: 'Total Patients',
      value: stats?.totalPatients || 0,
      icon: Users,
      color: 'green'
    },
    {
      label: 'Avg. Rating',
      value: stats?.averageRating ? stats.averageRating.toFixed(1) : '0.0',
      icon: Star,
      color: 'yellow'
    },
    {
      label: 'Pending Feedback',
      value: stats?.pendingFeedback || 0,
      icon: MessageSquare,
      color: 'purple'
    }
  ];

  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    purple: 'bg-purple-50 text-purple-600'
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {statItems.map((item, index) => {
        const Icon = item.icon;
        return (
          <div key={index} className="card p-6">
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${colorClasses[item.color]}`}>
                <Icon className="w-6 h-6" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{item.label}</p>
                <p className="text-2xl font-bold text-gray-900">{item.value}</p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default StatsCards;