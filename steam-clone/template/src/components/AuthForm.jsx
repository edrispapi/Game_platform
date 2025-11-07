import { useState } from 'react';
import { FiUser, FiLock, FiMail } from 'react-icons/fi';

const AuthForm = ({ type = 'login' }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: type === 'signup' ? '' : undefined,
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = 'Invalid email format';

    if (!formData.password.trim()) newErrors.password = 'Password is required';
    else if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters';

    if (type === 'signup' && !formData.username?.trim()) newErrors.username = 'Username is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setApiError(null);
    setSuccessMessage(null);

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      const endpoint = type === 'login' ? '/api/v1/users/login' : '/api/v1/users/register';
      const payload =
        type === 'login'
          ? {
              username_or_email: formData.email,
              password: formData.password,
              remember_me: true,
            }
          : {
              username: formData.username,
              email: formData.email,
              password: formData.password,
              full_name: formData.username,
            };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail = result?.detail || 'Unable to process your request. Please try again.';
        throw new Error(Array.isArray(detail) ? detail[0]?.msg ?? 'Validation error' : detail);
      }

      if (type === 'login') {
        const session = {
          token: result?.access_token,
          user: result?.user,
          expires_in: result?.expires_in,
        };
        localStorage.setItem('vcai_session', JSON.stringify(session));
        setSuccessMessage('Welcome back! Redirecting you to the dashboard...');
      } else {
        setSuccessMessage('Account created successfully. You can now sign in.');
        setFormData((prev) => ({ ...prev, password: '' }));
      }
    } catch (error) {
      setApiError(error.message || 'Unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: null }));
  };

  return (
    <div className="max-w-md mx-auto bg-dark-800 rounded-xl border border-gray-800 p-8 shadow-lg animate-fade-in">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold mb-2">{type === 'login' ? 'Welcome Back' : 'Create Account'}</h2>
        <p className="text-gray-400">
          {type === 'login' ? 'Please sign in to continue.' : 'Sign up to start creating your games.'}
        </p>
      </div>

      <form onSubmit={handleSubmit} noValidate>
        {type === 'signup' && (
          <div className="mb-4">
            <label htmlFor="username" className="block text-sm font-medium mb-1">
              Username
            </label>
            <div className="relative">
              <FiUser className="absolute left-3 top-3 text-gray-400" />
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Your username"
                autoComplete="username"
                className={`w-full pl-10 pr-3 py-3 rounded-lg bg-gray-900 border ${
                  errors.username ? 'border-secondary' : 'border-gray-700'
                } text-light focus:outline-none focus:ring-1 focus:ring-primary`}
              />
            </div>
            {errors.username && <p className="text-secondary text-xs mt-1">{errors.username}</p>}
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email
          </label>
          <div className="relative">
            <FiMail className="absolute left-3 top-3 text-gray-400" />
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              autoComplete="email"
              className={`w-full pl-10 pr-3 py-3 rounded-lg bg-gray-900 border ${
                errors.email ? 'border-secondary' : 'border-gray-700'
              } text-light focus:outline-none focus:ring-1 focus:ring-primary`}
            />
          </div>
          {errors.email && <p className="text-secondary text-xs mt-1">{errors.email}</p>}
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <div className="relative">
            <FiLock className="absolute left-3 top-3 text-gray-400" />
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Your password"
              autoComplete={type === 'login' ? 'current-password' : 'new-password'}
              className={`w-full pl-10 pr-3 py-3 rounded-lg bg-gray-900 border ${
                errors.password ? 'border-secondary' : 'border-gray-700'
              } text-light focus:outline-none focus:ring-1 focus:ring-primary`}
            />
          </div>
          {errors.password && <p className="text-secondary text-xs mt-1">{errors.password}</p>}
        </div>

        {apiError && (
          <div className="mb-4 rounded-lg border border-secondary/60 bg-secondary/10 px-4 py-3 text-sm text-secondary">
            {apiError}
          </div>
        )}

        {successMessage && (
          <div className="mb-4 rounded-lg border border-emerald-500/50 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300">
            {successMessage}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-3 rounded-lg font-bold text-white ${
            isLoading ? 'bg-primary/70 cursor-not-allowed' : 'bg-primary hover:bg-secondary'
          } transition-all duration-300`}
        >
          {isLoading
            ? type === 'login'
              ? 'Logging in...'
              : 'Creating account...'
            : type === 'login'
            ? 'Login'
            : 'Sign Up'}
        </button>
      </form>
    </div>
  );
};

export default AuthForm;
