import { newlyUnlocked } from '../../utils/achievements';
import AchievementModal from './AchievementModal';
import { useState, useEffect } from 'react';
import { dashboardAPI, missionsAPI } from '../../services/api';
import { showSuccess, showError, showInfo, showWithAction } from '../../utils/toast';
import MissionCard from './MissionCard';
import StreakCounter from './StreakCounter';
import ProgressBar from './ProgressBar';
import LevelBadge from './LevelBadge';
import './Dashboard.css';

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busyMission, setBusyMission] = useState(null);
  const [unlockedQueue, setUnlockedQueue] = useState([]);
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

  const handleUndoMission = async (missionNumber) => {
    setBusyMission(missionNumber);
    try {
      const response = await missionsAPI.undo({ mission_number: missionNumber });
      await loadDashboard();
      showInfo(
        response.data.streak_rolled_back
          ? `Mission ${missionNumber} unticked. Streak restored to Day ${response.data.user.current_streak}.`
          : `Mission ${missionNumber} unticked.`
      );
    } catch (err) {
      showError('Failed to undo mission');
      console.error(err);
    } finally {
      setBusyMission(null);
    }
  };

  const handleCompleteMission = async (missionNumber, notes) => {
    setBusyMission(missionNumber);
    try {
      const response = await missionsAPI.complete({
        mission_number: missionNumber,
        notes: notes || '',
      });

      const before = dashboard.user;
      await loadDashboard();
      const fresh = response.data.user;
      const unlocked = newlyUnlocked(before, fresh);
      if (unlocked.length) setUnlockedQueue((q) => [...q, ...unlocked]);

      const message = response.data.streak_increased
        ? `🔥 Day ${response.data.user.current_streak} complete!`
        : `Mission ${missionNumber} done!`;

      showWithAction(message, 'Undo', () => handleUndoMission(missionNumber), {
        position: 'top-center',
      });
    } catch (err) {
      showError('Failed to complete mission');
      console.error(err);
    } finally {
      setBusyMission(null);
    }
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
              onUndo={handleUndoMission}
              loading={busyMission === template.mission_number}
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
      
      {unlockedQueue.length > 0 && (
        <AchievementModal
          achievement={unlockedQueue[0]}
          onClose={() => setUnlockedQueue((q) => q.slice(1))}
        />
      )}
    </div>
  );
}

export default Dashboard;