import './StreakCounter.css';

function StreakCounter({ streak }) {
  return (
    <div className="streak-counter">
      <div className="flame-container">
        <div className={`flame ${streak > 0 ? 'burning' : ''}`}>🔥</div>
      </div>
      <div className="streak-info">
        <div className="streak-number">{streak}</div>
        <div className="streak-label">Day Streak</div>
      </div>
    </div>
  );
}

export default StreakCounter;