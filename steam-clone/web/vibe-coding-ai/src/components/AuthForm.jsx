import { useEffect, useMemo, useState } from 'react';
import { FiUser, FiLock, FiMail } from 'react-icons/fi';

const AuthForm = ({ type = 'login' }) => {
  const apiBaseUrl = useMemo(
    () => import.meta.env.VITE_API_GATEWAY_URL ?? 'http://localhost:8000',
    []
  );

  const initialFormState = useMemo(
    () => ({
      email: '',
      password: '',
      ...(type === 'signup' ? { username: '' } : {}),
    }),
    [type]
  );

  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    setFormData(initialFormState);
    setErrors({});
    setServerError(null);
    setSuccessMessage(null);
  }, [initialFormState]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      setIsLoading(true);
      setServerError(null);
      setSuccessMessage(null);

      try {
        const endpoint = type === 'login' ? '/api/v1/users/login' : '/api/v1/users/register';
        const payload =
          type === 'login'
            ? {
                username_or_email: formData.email,
                password: formData.password,
                remember_me: false,
              }
            : {
                username: formData.username,
                email: formData.email,
                password: formData.password,
              };

        const response = await fetch(`${apiBaseUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });

        let data = null;
        try {
          data = await response.json();
        } catch (error) {
          // Ignore JSON parsing errors for non-JSON responses
        }

        if (!response.ok) {
          let errorMessage = 'Unable to process request. Please try again later.';

          if (data?.detail) {
            if (typeof data.detail === 'string') {
              errorMessage = data.detail;
            } else if (Array.isArray(data.detail)) {
              errorMessage = data.detail
                .map((item) => item?.msg || item?.detail || item)
                .filter(Boolean)
                .join(' ');
            } else if (typeof data.detail === 'object') {
              errorMessage = data.detail.message || JSON.stringify(data.detail);
            }
          }

          throw new Error(errorMessage);
        }

        if (type === 'login' && data) {
          localStorage.setItem('authToken', data.access_token);
          localStorage.setItem('authUser', JSON.stringify(data.user));
          window.dispatchEvent(new CustomEvent('auth:login', { detail: data }));
          setSuccessMessage(`Welcome back, ${data.user.display_name || data.user.username}!`);
          setErrors({});
        } else if (data) {
          setSuccessMessage('Account created successfully. You can now log in.');
          setFormData(initialFormState);
          setErrors({});
        }
      } catch (error) {
        setServerError(error.message || 'Something went wrong. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
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
        {serverError && (
          <div className="mb-4 rounded-lg border border-secondary bg-secondary/10 px-4 py-3 text-sm text-secondary">
            {serverError}
          </div>
        )}
        {successMessage && (
          <div className="mb-4 rounded-lg border border-primary bg-primary/10 px-4 py-3 text-sm text-primary">
            {successMessage}
          </div>
        )}
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
              className={`w-full pl-10 pr-3 py-3 rounded-lg bg-gray-900 border ${
                errors.password ? 'border-secondary' : 'border-gray-700'
              } text-light focus:outline-none focus:ring-1 focus:ring-primary`}
            />
          </div>
          {errors.password && <p className="text-secondary text-xs mt-1">{errors.password}</p>}
        </div>
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
