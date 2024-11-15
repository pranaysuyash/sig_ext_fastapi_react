// src/pages/Login.jsx

import React from 'react';
import LoginForm from '../components/Auth/LoginForm';

const Login = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <LoginForm />
    </div>
  );
};

export default Login;
