import { useEffect } from 'react';
import { RARITY_COLORS } from '../../utils/achievements';
import './AchievementModal.css';

export default function AchievementModal({ achievement, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 6000);
    return () => clearTimeout(t);
  }, [onClose]);

  const color = RARITY_COLORS[achievement.rarity];

  return (
    <div className="ach-overlay" onClick={onClose}>
      <div className="ach-modal" style={{ borderColor: color }} onClick={(e) => e.stopPropagation()}>
        <span className="ach-tag" style={{ color, borderColor: color }}>Achievement Unlocked</span>
        <div className="ach-icon">{achievement.icon}</div>
        <h2>{achievement.name}</h2>
        <p>{achievement.description}</p>
        <span className="ach-rarity" style={{ background: color }}>{achievement.rarity}</span>
        <button className="ach-close" onClick={onClose}>Nice!</button>
      </div>
    </div>
  );
}