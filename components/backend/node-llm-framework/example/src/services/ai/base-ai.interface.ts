/**
 * Base AI Service Interface (Node.js)
 * Unified interface for Azure, Gemini, Claude, and Nova providers.
 */

export interface AIImageInput {
  type: 'image_url';
  image_url: {
    url: string;
    detail?: 'low' | 'high' | 'auto';
  };
}

export interface AITextInput {
  type: 'text';
  text: string;
}

export type AIMessageContent = string | (AITextInput | AIImageInput)[];

export interface AIGenerateOptions {
  prompt: AIMessageContent;
  model?: string;
  systemPrompt?: string;
  maxTokens?: number;
  temperature?: number;
  thinkingBudget?: number;
}

export interface AIStructuredOptions extends AIGenerateOptions {
  schema: any;
}

export interface BaseAIService {
  generateText(options: AIGenerateOptions): Promise<string>;
  generateStructuredResponse<T>(options: AIStructuredOptions): Promise<T>;
  streamText(options: AIGenerateOptions): Promise<AsyncIterable<string>>;
  supportsThinking(): boolean;
  supportsStructuredOutput(): boolean;
  getAvailableModels(): string[];
}

export interface TaskAnalysisResult {
  initial_response: string;
  category: string;
  complexity: number;
  updated_topic_title: string;
  is_topic_shift_detected: boolean;
}

export const TASK_ANALYSIS_SCHEMA = {
  type: 'object',
  properties: {
    initial_response: {
      type: 'string',
      description: "User-facing response acknowledging their request",
    },
    category: {
      type: 'string',
      enum: [
        'chat',
        'code_review',
        'code_gen_big',
        'code_gen_agentic',
        'svg_mockup',
        'slides',
        'test_cases',
        'brutal_honesty_analysis',
        'file_analysis',
        'autodoc',
      ],
      description: 'Task category for routing',
    },
    complexity: {
      type: 'number',
      minimum: 0,
      maximum: 10,
      description: 'Task complexity score from 0-10',
    },
    updated_topic_title: {
      type: 'string',
      description: "Concise updated title for the conversation topic.",
    },
    is_topic_shift_detected: {
      type: 'boolean',
      description:
        'True if the new request is significantly different from prior conversation history.',
    },
  },
  required: [
    'initial_response',
    'category',
    'complexity',
    'updated_topic_title',
    'is_topic_shift_detected',
  ],
};
