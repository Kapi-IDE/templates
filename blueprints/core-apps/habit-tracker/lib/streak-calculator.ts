/**
 * Streak Calculator Utility
 *
 * Calculates current and longest streaks from completion dates.
 * Handles timezone-aware date comparisons.
 */

import { startOfDay, differenceInDays, parseISO, subDays } from 'date-fns';

export interface StreakResult {
  currentStreak: number;
  longestStreak: number;
  lastCompletedDate: Date | null;
  isCompletedToday: boolean;
}

/**
 * Calculate streaks from an array of completion dates
 *
 * @param completionDates - Array of Date objects (completion dates)
 * @returns Streak statistics
 */
export function calculateStreaks(completionDates: Date[]): StreakResult {
  if (completionDates.length === 0) {
    return {
      currentStreak: 0,
      longestStreak: 0,
      lastCompletedDate: null,
      isCompletedToday: false,
    };
  }

  // Normalize dates to start of day and sort descending (newest first)
  const normalizedDates = completionDates
    .map(date => startOfDay(date))
    .sort((a, b) => b.getTime() - a.getTime())
    .filter((date, index, self) =>
      // Remove duplicates (same day completions)
      index === 0 || date.getTime() !== self[index - 1].getTime()
    );

  const today = startOfDay(new Date());
  const lastCompletedDate = normalizedDates[0];
  const isCompletedToday = lastCompletedDate.getTime() === today.getTime();

  // Calculate current streak
  let currentStreak = 0;
  let checkDate = today;

  // If not completed today, check if completed yesterday (streak continues)
  if (!isCompletedToday) {
    checkDate = subDays(today, 1);
  }

  for (const date of normalizedDates) {
    const daysDiff = differenceInDays(checkDate, date);

    if (daysDiff === 0) {
      currentStreak++;
      checkDate = subDays(checkDate, 1);
    } else if (daysDiff > 0) {
      // Gap in streak, stop counting
      break;
    }
  }

  // Calculate longest streak
  let longestStreak = 0;
  let tempStreak = 1;

  for (let i = 0; i < normalizedDates.length - 1; i++) {
    const daysDiff = differenceInDays(normalizedDates[i], normalizedDates[i + 1]);

    if (daysDiff === 1) {
      tempStreak++;
      longestStreak = Math.max(longestStreak, tempStreak);
    } else {
      tempStreak = 1;
    }
  }

  longestStreak = Math.max(longestStreak, tempStreak, currentStreak);

  return {
    currentStreak,
    longestStreak,
    lastCompletedDate,
    isCompletedToday,
  };
}

/**
 * Calculate completion rate for a period
 *
 * @param completionDates - Array of completion dates
 * @param days - Number of days to look back (default: 30)
 * @returns Completion rate as percentage (0-100)
 */
export function calculateCompletionRate(
  completionDates: Date[],
  days: number = 30
): number {
  const today = startOfDay(new Date());
  const startDate = subDays(today, days - 1);

  const completionsInPeriod = completionDates.filter(date => {
    const normalized = startOfDay(date);
    return normalized >= startDate && normalized <= today;
  });

  return Math.round((completionsInPeriod.length / days) * 100);
}

/**
 * Get completion calendar data for heat map visualization
 *
 * @param completionDates - Array of completion dates
 * @param days - Number of days to include (default: 90)
 * @returns Array of {date, completed} objects
 */
export function getCalendarData(
  completionDates: Date[],
  days: number = 90
): Array<{ date: Date; completed: boolean }> {
  const today = startOfDay(new Date());
  const completionSet = new Set(
    completionDates.map(date => startOfDay(date).getTime())
  );

  const calendar = [];
  for (let i = days - 1; i >= 0; i--) {
    const date = subDays(today, i);
    calendar.push({
      date,
      completed: completionSet.has(date.getTime()),
    });
  }

  return calendar;
}

/**
 * Get weekly completion stats for chart visualization
 *
 * @param completionDates - Array of completion dates
 * @param weeks - Number of weeks to include (default: 12)
 * @returns Array of {week, completions, targetDays} objects
 */
export function getWeeklyStats(
  completionDates: Date[],
  weeks: number = 12,
  targetDays: number = 7
): Array<{ week: string; completions: number; target: number }> {
  const today = startOfDay(new Date());
  const weeklyData = [];

  for (let i = weeks - 1; i >= 0; i--) {
    const weekEnd = subDays(today, i * 7);
    const weekStart = subDays(weekEnd, 6);

    const completionsInWeek = completionDates.filter(date => {
      const normalized = startOfDay(date);
      return normalized >= weekStart && normalized <= weekEnd;
    }).length;

    weeklyData.push({
      week: `Week ${weeks - i}`,
      completions: completionsInWeek,
      target: targetDays,
    });
  }

  return weeklyData;
}
