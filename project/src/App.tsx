import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Layout/Navbar';
import LoginForm from './components/Auth/LoginForm';
import ManagerDashboard from './components/Manager/ManagerDashboard';
import EmployeeDashboard from './components/Employee/EmployeeDashboard';
import PrivateRoute from './components/common/PrivateRoute';

const AppContent: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/login" element={
          user ? <Navigate to="/" replace /> : <LoginForm />
        } />
        
        <Route path="/" element={
          <PrivateRoute>
            <>
              <Navbar />
              {user?.role === 'manager' ? <ManagerDashboard /> : <EmployeeDashboard />}
            </>
          </PrivateRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;