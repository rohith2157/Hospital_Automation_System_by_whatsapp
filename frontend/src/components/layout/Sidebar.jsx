import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  LayoutDashboard,
  Calendar,
  Users,
  Stethoscope,
  MessageSquare,
  Campaign,
  Settings,
  UserCog
} from 'lucide-react';

const menuItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', roles: ['superadmin', 'admin', 'reception', 'campaign', 'viewer'] },
  { path: '/appointments', icon: Calendar, label: 'Appointments', roles: ['superadmin', 'admin', 'reception', 'viewer'] },
  { path: '/patients', icon: Users, label: 'Patients', roles: ['superadmin', 'admin', 'reception', 'campaign', 'viewer'] },
  { path: '/doctors', icon: Stethoscope, label: 'Doctors', roles: ['superadmin', 'admin', 'reception', 'viewer'] },
  { path: '/feedback', icon: MessageSquare, label: 'Feedback', roles: ['superadmin', 'admin', 'reception', 'viewer'] },
  { path: '/campaigns', icon: Campaign, label: 'Campaigns', roles: ['superadmin', 'admin', 'campaign'] },
  { path: '/users', icon: UserCog, label: 'Users', roles: ['superadmin', 'admin'] },
];

const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuth();

  const filteredMenuItems = menuItems.filter(item => 
    item.roles.includes(user?.role)
  );

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-4 border-b">
        <h1 className="text-xl font-bold text-blue-600">Clinic Manager</h1>
      </div>
      <nav className="p-4">
        <ul className="space-y-2">
          {filteredMenuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-600'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;