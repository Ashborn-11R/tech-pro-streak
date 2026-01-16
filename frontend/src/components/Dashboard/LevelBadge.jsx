import './LevelBadge.css';

function LevelBadge({ level, levelInfo }) {
  const getIcon = () => {
    switch(level) {
      case 'Beginner': return '🌱';
      case 'Builder': return '🔨';
      case 'Pro': return '⚡';
      case 'Elite': return '🔥';
      default: return '🌱';
    }
  };

  const getLevelNumber = () => {
    switch(level) {
      case 'Beginner': return '1';
      case 'Builder': return '2';
      case 'Pro': return '3';
      case 'Elite': return '4';
      default: return '1';
    }
  };

  return (
    <div className="level-badge">
      <div className="level-icon">{getIcon()}</div>
      <div className="level-details">
        <div className="level-name">{level}</div>
        <div className="level-number">LVL {getLevelNumber()}</div>
      </div>
      {levelInfo?.next_level && (
        <div className="level-progress">
          <div className="level-progress-text">
            {levelInfo.days_to_next_level} days to {levelInfo.next_level.name}
          </div>
          <div className="level-progress-bar">
            <div 
              className="level-progress-fill"
              style={{ width: `${levelInfo.progress_percentage}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LevelBadge;