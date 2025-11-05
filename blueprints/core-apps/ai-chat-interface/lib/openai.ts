/**
 * OpenAI Client Configuration
 *
 * Handles OpenAI API integration with streaming support
 */

import OpenAI from 'openai';

// Validate API key
if (!process.env.OPENAI_API_KEY) {
  throw new Error(
    'Missing OPENAI_API_KEY environment variable. ' +
    'Please add it to your .env.local file. ' +
    'Get your API key from https://platform.openai.com/api-keys'
  );
}

// Initialize OpenAI client
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Default model configuration
export const DEFAULT_MODEL = process.env.OPENAI_MODEL || 'gpt-4o-mini';
export const DEFAULT_TEMPERATURE = 0.7;
export const DEFAULT_MAX_TOKENS = 2000;

// Model pricing (per 1M tokens)
export const MODEL_PRICING = {
  'gpt-4o': { input: 2.50, output: 10.00 },
  'gpt-4o-mini': { input: 0.150, output: 0.600 },
  'gpt-4-turbo': { input: 10.00, output: 30.00 },
  'gpt-3.5-turbo': { input: 0.50, output: 1.50 },
} as const;

/**
 * Calculate cost for a completion
 */
export function calculateCost(
  model: string,
  inputTokens: number,
  outputTokens: number
): number {
  const pricing = MODEL_PRICING[model as keyof typeof MODEL_PRICING];
  if (!pricing) return 0;

  const inputCost = (inputTokens / 1_000_000) * pricing.input;
  const outputCost = (outputTokens / 1_000_000) * pricing.output;

  return inputCost + outputCost;
}

/**
 * Streaming chat completion
 */
export async function createChatStream(messages: Array<{ role: string; content: string }>) {
  const stream = await openai.chat.completions.create({
    model: DEFAULT_MODEL,
    messages: messages as any,
    temperature: DEFAULT_TEMPERATURE,
    max_tokens: DEFAULT_MAX_TOKENS,
    stream: true,
  });

  return stream;
}
