import { Link } from 'react-router-dom';
import {
  FiCode,
  FiUser,
  FiLogIn,
  FiLogOut,
  FiSun,
  FiMoon,
} from 'react-icons/fi';
import { useEffect, useState } from 'react';

const Navbar = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
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
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-gray-700 transition-colors"
            aria-label="Toggle theme"
          >
            {darkMode ? <FiSun className="text-yellow-300" /> : <FiMoon />}
          </button>

          {isLoggedIn ? (
            <>
              <Link
                to="/profile"
                className="flex items-center space-x-1 hover:text-primary transition-colors"
              >
                <FiUser />
                <span>Profile</span>
              </Link>
              <button
                onClick={() => setIsLoggedIn(false)}
                className="flex items-center space-x-1 hover:text-primary transition-colors"
              >
                <FiLogOut />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <Link
              to="/login"
              className="flex items-center space-x-1 hover:text-primary transition-colors"
            >
              <FiLogIn />
              <span>Login</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
