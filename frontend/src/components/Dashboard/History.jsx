import StreakCalendar from './StreakCalendar';
import BadgeShelf from './BadgeShelf';
import { useEffect, useState } from 'react';
import { authAPI, missionsAPI } from '../../services/api';
import './Pages.css';

export default function History() {
  const [user, setUser] = useState(null);
  const [days, setDays] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([authAPI.getCurrentUser(), missionsAPI.getHistory(60)])
      .then(([u, h]) => { setUser(u.data.user); setDays(h.data); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page"><p className="muted">Loading history...</p></div>;

  return (
    <div className="page">
      <div className="stat-row">
        <div className="stat-card">
          <span className="stat-label">Max Streak</span>
          <span className="stat-num">{user?.longest_streak ?? 0}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Total Days</span>
          <span className="stat-num">{user?.total_days_completed ?? 0}</span>
        </div>
      </div>
      {user && <BadgeShelf user={user} />}
      <StreakCalendar history={days} />
      
      <h2 className="page-title">Log History</h2>

      {days.length === 0 ? (
        <p className="muted center">No history yet. Start your first mission!</p>
      ) : (
        <div className="log-list">
          {days.map((d) => {
            const done = [d.mission_1_completed, d.mission_2_completed, d.mission_3_completed];
            const count = done.filter(Boolean).length;
            return (
              <div key={d.id} className={`log-card ${d.all_completed ? 'ok' : 'miss'}`}>
                <div>
                  <div className="log-date">
                    {new Date(d.mission_date + 'T00:00:00').toLocaleDateString('en-US',
                      { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}
                  </div>
                  <div className="dots">
                    {done.map((v, i) => <span key={i} className={v ? 'dot on' : 'dot'} />)}
                  </div>
                </div>
                <span className={`pill ${d.all_completed ? 'ok' : 'miss'}`}>
                  {d.all_completed ? 'Complete' : `${count}/3`}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}