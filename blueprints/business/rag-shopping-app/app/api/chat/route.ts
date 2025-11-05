import { NextRequest, NextResponse } from 'next/server';
import { shoppingAssistant } from '../../../lib/rag-engine';

export async function POST(request: NextRequest) {
  try {
    const { query, history } = await request.json();

    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    const response = await shoppingAssistant(query, history || []);

    return NextResponse.json({ response });
  } catch (error) {
    console.error('Chat error:', error);
    return NextResponse.json(
      { error: 'Chat failed' },
      { status: 500 }
    );
  }
}
