/**
 * Universal LLM Client
 * Supports: OpenAI, Azure OpenAI, Gemini, Claude (Bedrock), Ollama
 */

import OpenAI from 'openai';

export type LLMProvider = 'openai' | 'azure' | 'gemini' | 'claude' | 'ollama';

export interface LLMConfig {
  provider: LLMProvider;
  model?: string;
  temperature?: number;
  maxTokens?: number;
}

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
}

export interface LLMResponse {
  answer: string;
  citations: number[];
  relatedQuestions: string[];
}

/**
 * Generate answer from search results using configured LLM provider
 */
export async function generateAnswer(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const provider = config.provider || (process.env.LLM_PROVIDER as LLMProvider) || 'openai';

  switch (provider) {
    case 'openai':
      return generateWithOpenAI(query, searchResults, config);
    case 'azure':
      return generateWithAzure(query, searchResults, config);
    case 'gemini':
      return generateWithGemini(query, searchResults, config);
    case 'claude':
      return generateWithClaude(query, searchResults, config);
    case 'ollama':
      return generateWithOllama(query, searchResults, config);
    default:
      throw new Error(`Unsupported LLM provider: ${provider}`);
  }
}

/**
 * OpenAI Implementation
 */
async function generateWithOpenAI(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  const systemPrompt = buildSystemPrompt(searchResults);
  const userPrompt = buildUserPrompt(query);

  const completion = await openai.chat.completions.create({
    model: config.model || process.env.OPENAI_MODEL || 'gpt-4o-mini',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
    temperature: config.temperature || 0.7,
    max_tokens: config.maxTokens || 1000,
  });

  return parseResponse(completion.choices[0].message.content || '');
}

/**
 * Azure OpenAI Implementation
 */
async function generateWithAzure(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const openai = new OpenAI({
    apiKey: process.env.AZURE_OPENAI_API_KEY,
    baseURL: `${process.env.AZURE_OPENAI_ENDPOINT}/openai/deployments/${process.env.AZURE_OPENAI_DEPLOYMENT}`,
    defaultQuery: { 'api-version': process.env.AZURE_OPENAI_API_VERSION || '2024-02-01' },
    defaultHeaders: { 'api-key': process.env.AZURE_OPENAI_API_KEY },
  });

  const systemPrompt = buildSystemPrompt(searchResults);
  const userPrompt = buildUserPrompt(query);

  const completion = await openai.chat.completions.create({
    model: '', // Azure uses deployment name in URL
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
    temperature: config.temperature || 0.7,
    max_tokens: config.maxTokens || 1000,
  });

  return parseResponse(completion.choices[0].message.content || '');
}

/**
 * Google Gemini Implementation
 */
async function generateWithGemini(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const apiKey = process.env.GEMINI_API_KEY;
  const model = config.model || process.env.GEMINI_MODEL || 'gemini-2.0-flash-exp';

  const systemPrompt = buildSystemPrompt(searchResults);
  const userPrompt = buildUserPrompt(query);

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1/models/${model}:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: systemPrompt + '\n\n' + userPrompt }
            ]
          }
        ],
        generationConfig: {
          temperature: config.temperature || 0.7,
          maxOutputTokens: config.maxTokens || 1000,
        }
      })
    }
  );

  const data = await response.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';

  return parseResponse(text);
}

/**
 * Anthropic Claude (via AWS Bedrock) Implementation
 */
async function generateWithClaude(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const { BedrockRuntimeClient, InvokeModelCommand } = await import('@aws-sdk/client-bedrock-runtime');

  const client = new BedrockRuntimeClient({
    region: process.env.AWS_REGION || 'us-east-1',
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
    },
  });

  const systemPrompt = buildSystemPrompt(searchResults);
  const userPrompt = buildUserPrompt(query);

  const command = new InvokeModelCommand({
    modelId: config.model || process.env.CLAUDE_MODEL || 'anthropic.claude-3-5-sonnet-20241022-v2:0',
    body: JSON.stringify({
      anthropic_version: 'bedrock-2023-05-31',
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
      max_tokens: config.maxTokens || 1000,
      temperature: config.temperature || 0.7,
    }),
  });

  const response = await client.send(command);
  const responseBody = JSON.parse(new TextDecoder().decode(response.body));
  const text = responseBody.content[0].text;

  return parseResponse(text);
}

/**
 * Ollama Local Implementation
 */
async function generateWithOllama(
  query: string,
  searchResults: SearchResult[],
  config: LLMConfig
): Promise<LLMResponse> {
  const baseUrl = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
  const model = config.model || process.env.OLLAMA_MODEL || 'llama3.2:latest';

  const systemPrompt = buildSystemPrompt(searchResults);
  const userPrompt = buildUserPrompt(query);

  const response = await fetch(`${baseUrl}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt: `${systemPrompt}\n\nUser: ${userPrompt}\n\nAssistant:`,
      stream: false,
      options: {
        temperature: config.temperature || 0.7,
        num_predict: config.maxTokens || 1000,
      }
    })
  });

  const data = await response.json();
  return parseResponse(data.response);
}

/**
 * Build system prompt with search results
 */
function buildSystemPrompt(searchResults: SearchResult[]): string {
  const resultsText = searchResults
    .map((result, idx) => `[${idx + 1}] ${result.title}\n${result.snippet}\nSource: ${result.url}`)
    .join('\n\n');

  return `You are a helpful AI assistant that answers questions based on web search results.

Search Results:
${resultsText}

Instructions:
1. Provide a comprehensive answer based ONLY on the search results above
2. Cite sources using [1], [2], etc. notation
3. If the search results don't contain enough information, say so
4. Suggest 3 related follow-up questions at the end
5. Format your response as JSON:
{
  "answer": "Your detailed answer with [1] citations",
  "citations": [1, 2, 3],
  "relatedQuestions": ["Question 1?", "Question 2?", "Question 3?"]
}`;
}

/**
 * Build user prompt
 */
function buildUserPrompt(query: string): string {
  return `Question: ${query}

Please provide a detailed answer with citations.`;
}

/**
 * Parse LLM response into structured format
 */
function parseResponse(text: string): LLMResponse {
  try {
    // Try parsing as JSON first
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return {
        answer: parsed.answer || text,
        citations: parsed.citations || [],
        relatedQuestions: parsed.relatedQuestions || [],
      };
    }
  } catch (e) {
    // Fallback: extract citations and questions from text
  }

  // Fallback parsing
  const citationMatches = text.matchAll(/\[(\d+)\]/g);
  const citations = Array.from(citationMatches).map(m => parseInt(m[1]));

  const relatedQuestions: string[] = [];
  const questionMatches = text.matchAll(/(?:Related questions?|Follow-up questions?):\s*([\s\S]*?)(?:\n\n|$)/gi);
  for (const match of questionMatches) {
    const questions = match[1].split('\n').filter(q => q.trim());
    relatedQuestions.push(...questions.slice(0, 3));
  }

  return {
    answer: text,
    citations: Array.from(new Set(citations)),
    relatedQuestions: relatedQuestions.slice(0, 3),
  };
}
