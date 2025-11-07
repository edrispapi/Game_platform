import { Link, useNavigate } from 'react-router-dom';
import {
  FiCode,
  FiUser,
  FiLogIn,
  FiLogOut,
  FiSun,
  FiMoon,
} from 'react-icons/fi';
import { useEffect, useMemo, useState } from 'react';

const THEME_KEY = 'vcai_theme';
const SESSION_KEY = 'vcai_session';

const readSession = () => {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    console.warn('Failed to read session from storage', error);
    return null;
  }
};

const Navbar = () => {
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window === 'undefined') return true;
    const storedTheme = localStorage.getItem(THEME_KEY);
    if (storedTheme) return storedTheme === 'dark';
    return true;
  });
  const [session, setSession] = useState(() => readSession());
  const [logoutError, setLogoutError] = useState(null);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    if (typeof window !== 'undefined') {
      localStorage.setItem(THEME_KEY, darkMode ? 'dark' : 'light');
    }
  }, [darkMode]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const handleStorage = (event) => {
      if (event.key === SESSION_KEY) {
        setSession(readSession());
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
  };

  const handleLogout = async () => {
    if (!session?.token) {
      setSession(null);
      localStorage.removeItem(SESSION_KEY);
      return;
    }

    setIsLoggingOut(true);
    setLogoutError(null);

    try {
      const response = await fetch('/api/v1/users/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${session.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload?.detail || 'Unable to log out. Please try again.');
      }

      localStorage.removeItem(SESSION_KEY);
      setSession(null);
      navigate('/login');
    } catch (error) {
      setLogoutError(error.message || 'Unexpected error logging out.');
    } finally {
      setIsLoggingOut(false);
    }
  };

  const userDisplayName = useMemo(() => {
    if (!session?.user) return null;
    return session.user.full_name || session.user.username || session.user.email;
  }, [session]);

  return (
    <nav className="bg-dark-800 border-b border-gray-800 p-4">
      <div className="container mx-auto flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <FiCode className="text-primary text-2xl" />
            <span className="text-xl font-bold">Vibe Coding AI</span>
          </Link>

          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-gray-700 transition-colors md:hidden"
            aria-label="Toggle theme"
            type="button"
          >
            {darkMode ? <FiSun className="text-yellow-300" /> : <FiMoon />}
          </button>
        </div>

        <div className="hidden md:flex md:items-center md:space-x-6">
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
          <button
            onClick={toggleDarkMode}
            className="hidden rounded-full p-2 hover:bg-gray-700 transition-colors md:block"
            aria-label="Toggle theme"
            type="button"
          >
            {darkMode ? <FiSun className="text-yellow-300" /> : <FiMoon />}
          </button>

          {session?.token ? (
            <div className="flex items-center space-x-3">
              <span className="hidden text-sm text-gray-400 md:inline">{userDisplayName}</span>
              <Link
                to="/profile"
                className="flex items-center space-x-1 hover:text-primary transition-colors"
              >
                <FiUser />
                <span className="hidden sm:inline">Profile</span>
              </Link>
              <button
                onClick={handleLogout}
                disabled={isLoggingOut}
                className="flex items-center space-x-1 hover:text-primary transition-colors disabled:cursor-not-allowed"
                type="button"
              >
                <FiLogOut />
                <span>{isLoggingOut ? 'Logging out...' : 'Logout'}</span>
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
        <div className="mt-2 rounded-lg border border-secondary/50 bg-secondary/10 px-4 py-2 text-sm text-secondary">
          {logoutError}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
