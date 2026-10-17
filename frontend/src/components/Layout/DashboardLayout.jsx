import { useEffect, useState } from 'react';
import { NavLink, Outlet, Navigate, useNavigate } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { clearTokens, isAuthenticated } from '../../utils/auth';
import './Layout.css';

const tabs = [
  { to: '/dashboard', icon: '⚡', label: 'Missions' },
  { to: '/history', icon: '📅', label: 'History' },
  { to: '/settings', icon: '⚙️', label: 'Settings' },
];

export default function DashboardLayout() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) return;
    authAPI.getCurrentUser()
      .then((res) => setUser(res.data.user))
      .catch(() => { clearTokens(); navigate('/login'); });
  }, [navigate]);

  if (!isAuthenticated()) return <Navigate to="/login" />;

  const logout = () => { clearTokens(); navigate('/login'); };

  return (
    <div className="layout">
      <header className="top-nav">
        <h1>🔥 Tech Pro Streak</h1>
        <div className="top-right">
          {user && <span>Hi, {user.username}!</span>}
          <button className="btn-logout" onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="layout-main"><Outlet /></main>

      <nav className="bottom-nav">
        {tabs.map((t) => (
          <NavLink key={t.to} to={t.to}
            className={({ isActive }) => (isActive ? 'tab active' : 'tab')}>
            <span className="tab-icon">{t.icon}</span>
            <span className="tab-label">{t.label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}