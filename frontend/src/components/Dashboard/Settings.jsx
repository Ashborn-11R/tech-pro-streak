import { useEffect, useState } from 'react';
import { authAPI } from '../../services/api';
import { enableReminders, disableReminders, remindersEnabled } from '../../utils/reminders';
import { showSuccess, showError, showInfo } from '../../utils/toast';
import AdminPanel from './AdminPanel';
import './Pages.css';

export default function Settings() {
  const [user, setUser] = useState(null);
  const [reminders, setReminders] = useState(remindersEnabled());

  useEffect(() => {
    authAPI.getCurrentUser().then((r) => setUser(r.data.user));
  }, []);

  const toggleReminders = async () => {
    if (reminders) {
      disableReminders();
      setReminders(false);
      showInfo('Reminders turned off');
      return;
    }
    const result = await enableReminders();
    if (result === 'granted') {
      setReminders(true);
      showSuccess('Reminders turned on');
    } else if (result === 'unsupported') {
      showError('This browser does not support notifications');
    } else {
      showError('Notifications are blocked. Allow them in your browser site settings.');
    }
  };

  return (
    <div className="page">
      <div className="panel">
        <h2 className="panel-title">Daily Reminders</h2>
        <p className="muted">
          Get a notification 2 hours and 30 minutes before midnight if your missions
          aren't done. The app needs to be open in a browser tab.
        </p>
        <button className="btn-wide" onClick={toggleReminders}>
          {reminders ? 'Turn reminders off' : 'Turn reminders on'}
        </button>
      </div>

      {user?.is_staff && <AdminPanel />}
    </div>
  );
}