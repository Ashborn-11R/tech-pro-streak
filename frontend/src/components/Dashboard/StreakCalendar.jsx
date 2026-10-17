import './StreakCalendar.css';

const DAYS = 84; // 12 weeks

const iso = (d) => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
};

export default function StreakCalendar({ history }) {
  const byDate = {};
  history.forEach((h) => { byDate[h.mission_date] = h; });

  const today = new Date();
  const cells = [];
  for (let i = DAYS - 1; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    const key = iso(d);
    const rec = byDate[key];
    const count = rec
      ? [rec.mission_1_completed, rec.mission_2_completed, rec.mission_3_completed].filter(Boolean).length
      : 0;
    cells.push({ key, d, count, full: rec?.all_completed });
  }

  // pad so the first column starts on Monday
  const lead = (cells[0].d.getDay() + 6) % 7;

  return (
    <div className="cal-card">
      <h3>Your Streak Journey</h3>
      <div className="cal-grid">
        {Array.from({ length: lead }).map((_, i) => <span key={`p${i}`} className="cal-cell blank" />)}
        {cells.map((c) => (
          <span
            key={c.key}
            className={`cal-cell ${c.full ? 'full' : c.count ? 'partial' : ''}`}
            title={`${c.d.toDateString()}: ${c.full ? 'Complete' : `${c.count}/3`}`}
          />
        ))}
      </div>
      <div className="cal-legend">
        <span>None</span><i className="cal-cell" /><i className="cal-cell partial" /><i className="cal-cell full" /><span>Complete</span>
      </div>
    </div>
  );
}