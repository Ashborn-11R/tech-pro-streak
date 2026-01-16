import './ProgressBar.css';

function ProgressBar({ current, max }) {
  const percentage = (current / max) * 100;

  return (
    <div className="progress-section">
      <div className="progress-header">
        <span className="progress-label">SYSTEM PROGRESS</span>
        <span className="progress-text">{current}/{max} Days</span>
      </div>
      <div className="progress-bar-container">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentage}%` }}
        >
          <div className="progress-glow"></div>
        </div>
        <div className="progress-milestones">
          {[7, 14, 21, 30].map((milestone) => (
            <div 
              key={milestone}
              className={`milestone ${current >= milestone ? 'reached' : ''}`}
              style={{ left: `${(milestone / max) * 100}%` }}
            >
              <div className="milestone-dot"></div>
              <span className="milestone-label">{milestone}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ProgressBar;