import { useEffect } from 'react';

export const remindersEnabled = () =>
  typeof Notification !== 'undefined' &&
  Notification.permission === 'granted' &&
  localStorage.getItem('reminders_enabled') === 'true';

export async function enableReminders() {
  if (typeof Notification === 'undefined') return 'unsupported';
  const permission = await Notification.requestPermission();
  if (permission !== 'granted') return permission;
  localStorage.setItem('reminders_enabled', 'true');
  new Notification('Reminders are on 🔥', {
    body: "We'll nudge you before your streak is at risk.",
  });
  return 'granted';
}

export const disableReminders = () =>
  localStorage.setItem('reminders_enabled', 'false');

const WARNINGS = [
  { before: 2 * 3600, title: '⏰ 2 hours left', body: 'Finish your 3 missions to keep your streak alive.' },
  { before: 30 * 60, title: '🔥 Final call', body: "30 minutes left. Don't break your streak!" },
];

// Schedules the warnings relative to "now", skips them once the day is done
export function useReminders(secondsLeft, allDone) {
  useEffect(() => {
    if (secondsLeft == null || allDone || !remindersEnabled()) return;

    const timers = WARNINGS
      .map((w) => {
        const delay = (secondsLeft - w.before) * 1000;
        if (delay <= 0) return null;
        return setTimeout(
          () => new Notification(w.title, { body: w.body, tag: 'streak-reminder' }),
          delay
        );
      })
      .filter(Boolean);

    return () => timers.forEach(clearTimeout);
  }, [secondsLeft, allDone]);
}