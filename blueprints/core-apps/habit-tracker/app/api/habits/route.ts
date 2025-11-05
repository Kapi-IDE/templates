/**
 * Habits API Routes
 * GET /api/habits - List all habits with stats
 * POST /api/habits - Create new habit
 */

import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';
import { z } from 'zod';
import { calculateStreaks } from '@/lib/streak-calculator';

const prisma = new PrismaClient();

// Validation schema
const createHabitSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  category: z.enum(['health', 'work', 'learning', 'personal', 'general']).default('general'),
  color: z.string().regex(/^#[0-9A-F]{6}$/i).default('#3B82F6'),
  icon: z.string().optional(),
  targetDays: z.number().int().min(1).max(7).default(7),
  frequency: z.enum(['daily', 'weekly', 'custom']).default('daily'),
});

export async function GET() {
  try {
    const habits = await prisma.habit.findMany({
      where: {
        archived: false,
      },
      include: {
        completions: {
          orderBy: {
            date: 'desc',
          },
        },
        _count: {
          select: {
            completions: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    // Calculate streaks for each habit
    const habitsWithStats = habits.map(habit => {
      const completionDates = habit.completions.map(c => new Date(c.date));
      const streaks = calculateStreaks(completionDates);

      return {
        id: habit.id,
        name: habit.name,
        description: habit.description,
        category: habit.category,
        color: habit.color,
        icon: habit.icon,
        targetDays: habit.targetDays,
        frequency: habit.frequency,
        createdAt: habit.createdAt,
        totalCompletions: habit._count.completions,
        currentStreak: streaks.currentStreak,
        longestStreak: streaks.longestStreak,
        isCompletedToday: streaks.isCompletedToday,
        lastCompletedDate: streaks.lastCompletedDate,
      };
    });

    return NextResponse.json(habitsWithStats);
  } catch (error) {
    console.error('Error fetching habits:', error);
    return NextResponse.json(
      { error: 'Failed to fetch habits' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const validated = createHabitSchema.parse(body);

    const habit = await prisma.habit.create({
      data: validated,
    });

    return NextResponse.json(habit, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    console.error('Error creating habit:', error);
    return NextResponse.json(
      { error: 'Failed to create habit' },
      { status: 500 }
    );
  }
}
