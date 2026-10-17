import { useEffect, useState } from 'react';
import { adminAPI } from '../../services/api';
import { showSuccess, showError } from '../../utils/toast';

export default function AdminPanel() {
  const [missions, setMissions] = useState([]);
  const [quotes, setQuotes] = useState([]);
  const [newQuote, setNewQuote] = useState({ quote: '', author: '' });

  const load = async () => {
    try {
      const [m, q] = await Promise.all([adminAPI.getMissions(), adminAPI.getQuotes()]);
      setMissions(m.data);
      setQuotes(q.data);
    } catch {
      showError('Could not load admin data');
    }
  };

  useEffect(() => { load(); }, []);

  const editMission = (id, field, value) =>
    setMissions((ms) => ms.map((m) => (m.id === id ? { ...m, [field]: value } : m)));

  const saveMission = async (m) => {
    try {
      await adminAPI.updateMission(m.id, { title: m.title, description: m.description });
      showSuccess('Mission saved');
    } catch {
      showError('Save failed');
    }
  };

  const addQuote = async (e) => {
    e.preventDefault();
    if (!newQuote.quote.trim()) return;
    try {
      await adminAPI.createQuote(newQuote);
      setNewQuote({ quote: '', author: '' });
      showSuccess('Quote added');
      load();
    } catch {
      showError('Could not add quote');
    }
  };

  const toggleQuote = async (q) => {
    try {
      await adminAPI.updateQuote(q.id, { active: !q.active });
      load();
    } catch {
      showError('Update failed');
    }
  };

  const removeQuote = async (q) => {
    if (!window.confirm('Delete this quote?')) return;
    try {
      await adminAPI.deleteQuote(q.id);
      showSuccess('Quote deleted');
      load();
    } catch {
      showError('Delete failed');
    }
  };

  return (
    <>
      <div className="panel">
        <h2 className="panel-title">Global Missions</h2>
        <p className="muted">Changes apply to every user immediately.</p>
        {missions.map((m) => (
          <div key={m.id} className="admin-item">
            <span className="admin-tag">Mission {m.mission_number}</span>
            <input className="field" value={m.title}
                   onChange={(e) => editMission(m.id, 'title', e.target.value)} />
            <textarea className="field" rows="3" value={m.description}
                      onChange={(e) => editMission(m.id, 'description', e.target.value)} />
            <button className="btn-wide" onClick={() => saveMission(m)}>Save mission</button>
          </div>
        ))}
      </div>

      <div className="panel">
        <h2 className="panel-title">Motivational Quotes</h2>
        <form onSubmit={addQuote} className="admin-item">
          <textarea className="field" rows="2" placeholder="New quote..."
                    value={newQuote.quote}
                    onChange={(e) => setNewQuote({ ...newQuote, quote: e.target.value })} />
          <input className="field" placeholder="Author (optional)"
                 value={newQuote.author}
                 onChange={(e) => setNewQuote({ ...newQuote, author: e.target.value })} />
          <button className="btn-wide" type="submit">Add quote</button>
        </form>

        {quotes.map((q) => (
          <div key={q.id} className={`quote-row ${q.active ? '' : 'off'}`}>
            <div>
              <div>“{q.quote}”</div>
              {q.author && <small className="muted">— {q.author}</small>}
            </div>
            <div className="quote-actions">
              <button onClick={() => toggleQuote(q)}>{q.active ? 'Hide' : 'Show'}</button>
              <button onClick={() => removeQuote(q)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}