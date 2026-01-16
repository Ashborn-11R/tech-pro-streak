import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardAPI, missionsAPI } from '../../services/api';
import { clearTokens } from '../../utils/auth';
import MissionCard from './MissionCard';
import StreakCounter from './StreakCounter';
import ProgressBar from './ProgressBar';
import LevelBadge from './LevelBadge';
import './Dashboard.css';

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [completingMission, setCompletingMission] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await dashboardAPI.getDashboard();
      setDashboard(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteMission = async (missionNumber, notes) => {
    setCompletingMission(missionNumber);

    try {
      const response = await missionsAPI.complete({
        mission_number: missionNumber,
        notes: notes || '',
      });

      // Reload dashboard to get updated data
      await loadDashboard();

      // Show celebration if streak increased
      if (response.data.streak_increased) {
        alert(`🔥 Amazing! Day ${response.data.user.current_streak} complete!`);
      }
    } catch (err) {
      alert('Failed to complete mission');
      console.error(err);
    } finally {
      setCompletingMission(null);
    }
  };

  const handleLogout = () => {
    clearTokens();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading your journey...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>{error}</p>
        <button onClick={loadDashboard}>Retry</button>
      </div>
    );
  }

  const { user, mission, templates, quote, time_until_midnight, level_info } = dashboard;

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <h1>🔥 Tech Pro Streak</h1>
        <div className="nav-right">
          <span>Hi, {user.username}!</span>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-container">
        {/* Streak Stats */}
        <div className="stats-section">
          <StreakCounter streak={user.current_streak} />
          <LevelBadge level={user.level} levelInfo={level_info} />
          
          <div className="time-remaining">
            <p>⏰ Time left today: <strong>{time_until_midnight.formatted}</strong></p>
          </div>
        </div>

        {/* Progress Bar */}
        <ProgressBar current={user.current_streak} max={30} />

        {/* Motivational Quote */}
        {quote && (
          <div className="quote-card">
            <p className="quote-text">"{quote.quote}"</p>
            {quote.author && <p className="quote-author">— {quote.author}</p>}
          </div>
        )}

        {/* Today's Missions */}
        <div className="missions-section">
          <h2>Today's Missions</h2>
          <p className="missions-subtitle">Complete all 3 to maintain your streak 🔥</p>

          <div className="missions-list">
            {templates.map((template) => (
              <MissionCard
                key={template.mission_number}
                missionNumber={template.mission_number}
                title={template.title}
                description={template.description}
                completed={mission[`mission_${template.mission_number}_completed`]}
                notes={mission[`mission_${template.mission_number}_notes`] || ''}
                onComplete={handleCompleteMission}
                loading={completingMission === template.mission_number}
              />
            ))}
          </div>

          {mission.all_completed && (
            <div className="completion-banner">
              <h3>🎉 All missions complete!</h3>
              <p>You've earned Day {user.current_streak}! Come back tomorrow.</p>
            </div>
          )}
        </div>

        {/* User Stats */}
        <div className="user-stats">
          <div className="stat-item">
            <span className="stat-label">Longest Streak</span>
            <span className="stat-value">{user.longest_streak} days</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Days</span>
            <span className="stat-value">{user.total_days_completed}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;