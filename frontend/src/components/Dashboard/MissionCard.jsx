import { useState } from 'react';
import './MissionCard.css';

function MissionCard({
  missionNumber, title, description, completed, notes,
  onComplete, onUndo, loading,
}) {
  const [showNotes, setShowNotes] = useState(false);
  const [noteText, setNoteText] = useState(notes || '');

  const handleToggle = () => {
    if (loading) return;
    if (completed) {
      onUndo(missionNumber);
    } else {
      onComplete(missionNumber, noteText);
    }
  };

  const icons = { 1: '💬', 2: '⚡', 3: '🎯' };

  return (
    <div className={`mission-card ${completed ? 'completed' : ''}`}>
      <div className="mission-header">
        <div className="mission-icon">{icons[missionNumber] || '✨'}</div>
        <div className="mission-info">
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
        <div className="mission-checkbox">
          <input
            type="checkbox"
            checked={completed}
            onChange={handleToggle}
            disabled={loading}
            id={`mission-${missionNumber}`}
          />
          <label htmlFor={`mission-${missionNumber}`}>
            <div className="checkbox-custom"></div>
          </label>
        </div>
      </div>

      {!completed && (
        <div className="mission-notes">
          <button
            className="toggle-notes-btn"
            onClick={() => setShowNotes(!showNotes)}
          >
            {showNotes ? '− Hide Notes' : '+ Add Notes'}
          </button>

          {showNotes && (
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="What did you accomplish?"
              rows="3"
            />
          )}
        </div>
      )}

      {completed && notes && (
        <div className="mission-completed-notes">
          <p><strong>Your notes:</strong> {notes}</p>
        </div>
      )}

      {loading && (
        <div className="mission-loading">
          <div className="spinner-small"></div>
        </div>
      )}
    </div>
  );
}

export default MissionCard;