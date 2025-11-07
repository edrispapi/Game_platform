import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import GameCreatorDashboard from './pages/GameCreatorDashboard';

const App = () => (
  <Router>
    <div className="min-h-screen bg-dark text-light font-sans flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/create" element={<GameCreatorDashboard />} />
        </Routes>
      </main>
      <Footer />
    </div>
  </Router>
);

export default App;
