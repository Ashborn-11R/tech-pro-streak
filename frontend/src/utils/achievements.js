export const ACHIEVEMENTS = [
  { id: 'first_day', name: 'First Steps', description: 'Complete your first day', icon: '🎯', rarity: 'common',
    check: (u) => u.total_days_completed >= 1 },
  { id: 'week', name: 'Week Warrior', description: 'Reach a 7-day streak', icon: '🔥', rarity: 'rare',
    check: (u) => u.longest_streak >= 7 },
  { id: 'two_weeks', name: 'Fortnight Fighter', description: 'Reach a 14-day streak', icon: '⚡', rarity: 'epic',
    check: (u) => u.longest_streak >= 14 },
  { id: 'three_weeks', name: 'Habit Hero', description: 'Reach a 21-day streak', icon: '💪', rarity: 'legendary',
    check: (u) => u.longest_streak >= 21 },
  { id: 'month', name: 'Month Master', description: 'Complete the full 30 days', icon: '👑', rarity: 'mythic',
    check: (u) => u.longest_streak >= 30 },
  { id: 'dedication', name: 'Dedication', description: 'Complete 50 total days', icon: '🎖️', rarity: 'epic',
    check: (u) => u.total_days_completed >= 50 },
];

export const RARITY_COLORS = {
  common: '#9ca3af', rare: '#3b82f6', epic: '#a855f7', legendary: '#f59e0b', mythic: '#ec4899',
};

// Achievements unlocked by `after` that weren't unlocked by `before`
export const newlyUnlocked = (before, after) =>
  ACHIEVEMENTS.filter((a) => a.check(after) && !(before && a.check(before)));