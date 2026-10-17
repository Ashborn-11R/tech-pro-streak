import './Pages.css';

export default function Settings() {
  return (
    <div className="page">
      <div className="panel">
        <h2 className="panel-title">Protocol Admin</h2>
        <p className="muted">Modify the central motivational array or mission parameters.</p>
        <div className="info-box">
          ℹ️ Staff only: opens the Django admin, where missions and quotes are edited.
        </div>
        <a className="btn-wide" href="http://127.0.0.1:8000/admin/streaks/missiontemplate/"
           target="_blank" rel="noreferrer">Edit Global Missions</a>
        <a className="btn-wide" href="http://127.0.0.1:8000/admin/streaks/motivationalquote/"
           target="_blank" rel="noreferrer">Edit Motivational Quotes</a>
      </div>
    </div>
  );
}