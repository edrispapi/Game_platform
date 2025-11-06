import { Link } from 'react-router-dom';
import { FiCode, FiUser, FiLogIn, FiLogOut, FiSun, FiMoon } from 'react-icons/fi';
import { useEffect, useMemo, useState } from 'react';

const Navbar = () => {
  const apiBaseUrl = useMemo(
    () => import.meta.env.VITE_API_GATEWAY_URL ?? 'http://localhost:8000',
    []
  );
  const [darkMode, setDarkMode] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [isProcessingLogout, setIsProcessingLogout] = useState(false);
  const [logoutError, setLogoutError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('authUser');

    if (token && storedUser) {
      setIsLoggedIn(true);
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        setUser(null);
      }
    }

    const handleLogin = (event) => {
      const { user: userData } = event.detail || {};
      if (userData) {
        setIsLoggedIn(true);
        setUser(userData);
      }
    };

    const handleLogout = () => {
      setIsLoggedIn(false);
      setUser(null);
    };

    window.addEventListener('auth:login', handleLogin);
    window.addEventListener('auth:logout', handleLogout);

    return () => {
      window.removeEventListener('auth:login', handleLogin);
      window.removeEventListener('auth:logout', handleLogout);
    };
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
  };

  const handleLogout = async () => {
    if (isProcessingLogout) return;

    setIsProcessingLogout(true);
    setLogoutError(null);

    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        await fetch(`${apiBaseUrl}/api/v1/users/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      setLogoutError('Unable to reach the user service. Logout may not have completed.');
    } finally {
      setIsProcessingLogout(false);
      localStorage.removeItem('authToken');
      localStorage.removeItem('authUser');
      setIsLoggedIn(false);
      setUser(null);
      window.dispatchEvent(new CustomEvent('auth:logout'));
    }
  };

  return (
    <nav className="bg-dark-800 border-b border-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          <FiCode className="text-primary text-2xl" />
          <span className="text-xl font-bold">Vibe Coding AI</span>
        </Link>

        <div className="hidden md:flex space-x-6">
          <Link to="/create" className="hover:text-primary transition-colors">
            Create
          </Link>
          <Link to="/games" className="hover:text-primary transition-colors">
            Games
          </Link>
          <Link to="/about" className="hover:text-primary transition-colors">
            About
          </Link>
          <Link to="/contact" className="hover:text-primary transition-colors">
            Contact
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <button onClick={toggleDarkMode} className="p-2 rounded-full hover:bg-gray-700 transition-colors">
            {darkMode ? <FiSun className="text-yellow-300" /> : <FiMoon />}
          </button>

          {isLoggedIn ? (
            <div className="flex items-center space-x-4">
              <Link to="/profile" className="flex items-center space-x-2 hover:text-primary transition-colors">
                <FiUser />
                <span>{user?.display_name || user?.username || 'Profile'}</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 hover:text-primary transition-colors disabled:opacity-60"
                disabled={isProcessingLogout}
              >
                <FiLogOut />
                <span>{isProcessingLogout ? 'Logging out...' : 'Logout'}</span>
              </button>
            </div>
          ) : (
            <Link to="/login" className="flex items-center space-x-1 hover:text-primary transition-colors">
              <FiLogIn />
              <span>Login</span>
            </Link>
          )}
        </div>
      </div>
      {logoutError && (
        <div className="mt-3 text-center text-xs text-secondary">
          {logoutError}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
