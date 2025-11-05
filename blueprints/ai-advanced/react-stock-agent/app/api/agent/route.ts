/**
 * ReAct Stock Agent API
 * Handles agent requests with ReAct framework
 */

import { NextRequest, NextResponse } from 'next/server';
import { ReActAgent, createReActPrompt } from '@/lib/react-agent';
import { createLLMClient } from '@/lib/universal-llm';
import { stockTools } from '@/tools/stock-tools';
import type { LLMConfig } from '@/lib/universal-llm';

export async function POST(req: NextRequest) {
  try {
    const { question, llmConfig } = await req.json() as {
      question: string;
      llmConfig: LLMConfig;
    };

    if (!question || !llmConfig) {
      return NextResponse.json(
        { error: 'Missing question or LLM configuration' },
        { status: 400 }
      );
    }

    // Create LLM client from user's config
    const llm = createLLMClient(llmConfig);

    // Create ReAct system prompt
    const systemPrompt = createReActPrompt({
      role: 'a stock market analyst',
      tools: {
        stock_price: {
          description: 'Returns the current stock price of the given ticker symbol (e.g., AAPL for Apple Inc.)',
          example: 'stock_price: AAPL'
        },
        ddgs_news: {
          description: 'Performs a news search for the given ticker query using DuckDuckGo and returns a summarized text of all the news articles found. Use the news content to analyze and determine whether the overall sentiment is positive, negative, or neutral.',
          example: 'ddgs_news: Tesla'
        },
        calculate: {
          description: 'Runs a calculation and returns the result. Use Python-style syntax, including any necessary operations.',
          example: 'calculate: result=4 * 7 / 3'
        }
      },
      examples: `
Question: What is the current price of Tesla, and is the recent news about it positive or negative?

Thought: First, I need to get the current stock price of Tesla.
Action: stock_price: TSLA
PAUSE

Observation: The current stock price of Tesla (TSLA) is $700.

Thought: Now, I should retrieve the latest news about Tesla and determine the overall sentiment.
Action: ddgs_news: Tesla
PAUSE

Observation: Tesla secures a new battery deal with Panasonic...
Tesla's latest earnings surpass expectations...

--Next News--

Tesla faces regulatory challenges in Europe...

--Next News--

...

Thought: After analyzing the news content, the sentiment appears to be mostly positive due to the strong earnings and new battery deal.
I should calculate the number of stocks you could buy for $10,000.

Action: calculate: result=10000/700
PAUSE

Observation: You could buy 14 shares.

Answer: The current price of Tesla (TSLA) is $700. The recent news about Tesla is generally positive, with strong earnings and a new battery deal.
You could buy 14 shares to cover your $10,000 investment.

RECOMMENDATION: BUY

If the news is neither negative or positive and you cannot make a decision, return a HOLD statement. If not give a BUY or SELL statement.
This is for a lab experiment and not a trading strategy and thus be bold.

Return the number of shares that could be bought.
      `.trim()
    });

    // Create ReAct agent
    const agent = new ReActAgent({
      llm,
      tools: stockTools,
      systemPrompt,
      maxSteps: 10,
      debug: process.env.NODE_ENV === 'development'
    });

    // Run agent
    const result = await agent.run(question);

    if (result.success) {
      return NextResponse.json({
        success: true,
        answer: result.answer,
        steps: result.steps,
        totalSteps: result.totalSteps
      });
    } else {
      return NextResponse.json(
        {
          success: false,
          error: result.error || 'Agent failed to complete',
          steps: result.steps
        },
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Agent API error:', error);
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
