/**
 * Habit Completion API
 * POST /api/habits/[id]/complete - Mark habit as complete for today
 * DELETE /api/habits/[id]/complete - Remove today's completion
 */

import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';
import { startOfDay } from 'date-fns';

const prisma = new PrismaClient();

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    const body = await request.json();
    const { date, note } = body;

    // Use provided date or default to today
    const completionDate = date ? startOfDay(new Date(date)) : startOfDay(new Date());

    // Check if habit exists
    const habit = await prisma.habit.findUnique({
      where: { id },
    });

    if (!habit) {
      return NextResponse.json(
        { error: 'Habit not found' },
        { status: 404 }
      );
    }

    // Create or update completion
    const completion = await prisma.completion.upsert({
      where: {
        habitId_date: {
          habitId: id,
          date: completionDate,
        },
      },
      create: {
        habitId: id,
        date: completionDate,
        note: note || null,
      },
      update: {
        note: note || null,
      },
    });

    return NextResponse.json(completion, { status: 201 });
  } catch (error) {
    console.error('Error marking habit complete:', error);
    return NextResponse.json(
      { error: 'Failed to mark habit complete' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    const { searchParams } = new URL(request.url);
    const dateParam = searchParams.get('date');

    // Use provided date or default to today
    const completionDate = dateParam
      ? startOfDay(new Date(dateParam))
      : startOfDay(new Date());

    await prisma.completion.delete({
      where: {
        habitId_date: {
          habitId: id,
          date: completionDate,
        },
      },
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error removing completion:', error);
    return NextResponse.json(
      { error: 'Failed to remove completion' },
      { status: 500 }
    );
  }
}
