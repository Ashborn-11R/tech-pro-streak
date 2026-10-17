import { ACHIEVEMENTS, RARITY_COLORS } from '../../utils/achievements';

export default function BadgeShelf({ user }) {
  const unlocked = ACHIEVEMENTS.filter((a) => a.check(user)).length;

  return (
    <div className="cal-card">
      <h3>Achievements ({unlocked}/{ACHIEVEMENTS.length})</h3>
      <div className="badge-grid">
        {ACHIEVEMENTS.map((a) => {
          const on = a.check(user);
          return (
            <div key={a.id} className={`badge-tile ${on ? 'on' : ''}`}
                 style={on ? { borderColor: RARITY_COLORS[a.rarity] } : undefined}>
              <span className="badge-icon">{on ? a.icon : '🔒'}</span>
              <strong>{a.name}</strong>
              <small>{a.description}</small>
            </div>
          );
        })}
      </div>
    </div>
  );
}