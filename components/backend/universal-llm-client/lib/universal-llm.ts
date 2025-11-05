/**
 * Universal LLM Client
 *
 * Unified interface for multiple LLM providers:
 * - OpenAI (GPT-4, GPT-4o, GPT-3.5)
 * - Azure OpenAI (Enterprise)
 * - Google Gemini (Cheapest cloud)
 * - Anthropic Claude (Best reasoning)
 * - Ollama (FREE local)
 *
 * Usage:
 * ```typescript
 * const client = createLLMClient({
 *   provider: 'openai',
 *   apiKey: process.env.OPENAI_API_KEY,
 *   model: 'gpt-4o-mini'
 * });
 *
 * const response = await client.chat({
 *   messages: [{ role: 'user', content: 'Hello!' }]
 * });
 * ```
 */

export type LLMProvider = 'openai' | 'azure' | 'gemini' | 'claude' | 'ollama';

export interface LLMConfig {
  provider: LLMProvider;
  apiKey?: string;
  model?: string;
  baseURL?: string;

  // Azure-specific
  azureEndpoint?: string;
  azureDeployment?: string;
  azureApiVersion?: string;

  // AWS Bedrock (Claude) specific
  awsRegion?: string;
  awsAccessKeyId?: string;
  awsSecretAccessKey?: string;

  // Default parameters
  temperature?: number;
  maxTokens?: number;
  topP?: number;
}

export interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface ChatOptions {
  messages: Message[];
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  stream?: boolean;
  stopSequences?: string[];
}

export interface ChatResponse {
  content: string;
  finishReason: 'stop' | 'length' | 'content_filter' | 'error';
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model: string;
  provider: LLMProvider;
}

export interface StreamChunk {
  content: string;
  done: boolean;
}

export interface LLMClient {
  chat(options: ChatOptions): Promise<ChatResponse>;
  chatStream(options: ChatOptions): AsyncGenerator<StreamChunk, void, unknown>;
  getProvider(): LLMProvider;
  getModel(): string;
}

/**
 * Create an LLM client for the specified provider
 */
export function createLLMClient(config: LLMConfig): LLMClient {
  switch (config.provider) {
    case 'openai':
      return new OpenAIClient(config);
    case 'azure':
      return new AzureOpenAIClient(config);
    case 'gemini':
      return new GeminiClient(config);
    case 'claude':
      return new ClaudeClient(config);
    case 'ollama':
      return new OllamaClient(config);
    default:
      throw new Error(`Unsupported LLM provider: ${config.provider}`);
  }
}

/**
 * Auto-detect provider from environment variables
 */
export function createLLMClientFromEnv(): LLMClient {
  const provider = (process.env.LLM_PROVIDER || 'openai') as LLMProvider;

  const config: LLMConfig = {
    provider,
    temperature: parseFloat(process.env.LLM_TEMPERATURE || '0.7'),
    maxTokens: parseInt(process.env.LLM_MAX_TOKENS || '1000'),
  };

  switch (provider) {
    case 'openai':
      config.apiKey = process.env.OPENAI_API_KEY;
      config.model = process.env.OPENAI_MODEL || 'gpt-4o-mini';
      break;

    case 'azure':
      config.apiKey = process.env.AZURE_OPENAI_API_KEY;
      config.azureEndpoint = process.env.AZURE_OPENAI_ENDPOINT;
      config.azureDeployment = process.env.AZURE_OPENAI_DEPLOYMENT;
      config.azureApiVersion = process.env.AZURE_OPENAI_API_VERSION || '2024-02-01';
      break;

    case 'gemini':
      config.apiKey = process.env.GEMINI_API_KEY;
      config.model = process.env.GEMINI_MODEL || 'gemini-2.0-flash-exp';
      break;

    case 'claude':
      config.awsRegion = process.env.AWS_REGION || 'us-east-1';
      config.awsAccessKeyId = process.env.AWS_ACCESS_KEY_ID;
      config.awsSecretAccessKey = process.env.AWS_SECRET_ACCESS_KEY;
      config.model = process.env.CLAUDE_MODEL || 'anthropic.claude-3-5-sonnet-20241022-v2:0';
      break;

    case 'ollama':
      config.baseURL = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
      config.model = process.env.OLLAMA_MODEL || 'llama3.2:latest';
      break;
  }

  return createLLMClient(config);
}

/**
 * OpenAI Client Implementation
 */
class OpenAIClient implements LLMClient {
  private config: LLMConfig;
  private openai: any;

  constructor(config: LLMConfig) {
    this.config = config;

    // Lazy import to avoid bundling if not used
    const OpenAI = require('openai');
    this.openai = new OpenAI({
      apiKey: config.apiKey,
      baseURL: config.baseURL,
    });
  }

  async chat(options: ChatOptions): Promise<ChatResponse> {
    const response = await this.openai.chat.completions.create({
      model: this.config.model || 'gpt-4o-mini',
      messages: options.messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      top_p: options.topP ?? this.config.topP,
      stop: options.stopSequences,
      stream: false,
    });

    return {
      content: response.choices[0].message.content || '',
      finishReason: this.mapFinishReason(response.choices[0].finish_reason),
      usage: {
        promptTokens: response.usage.prompt_tokens,
        completionTokens: response.usage.completion_tokens,
        totalTokens: response.usage.total_tokens,
      },
      model: response.model,
      provider: 'openai',
    };
  }

  async *chatStream(options: ChatOptions): AsyncGenerator<StreamChunk> {
    const stream = await this.openai.chat.completions.create({
      model: this.config.model || 'gpt-4o-mini',
      messages: options.messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      const done = chunk.choices[0]?.finish_reason !== null;

      yield { content, done };
    }
  }

  getProvider(): LLMProvider {
    return 'openai';
  }

  getModel(): string {
    return this.config.model || 'gpt-4o-mini';
  }

  private mapFinishReason(reason: string): ChatResponse['finishReason'] {
    switch (reason) {
      case 'stop': return 'stop';
      case 'length': return 'length';
      case 'content_filter': return 'content_filter';
      default: return 'stop';
    }
  }
}

/**
 * Azure OpenAI Client Implementation
 */
class AzureOpenAIClient implements LLMClient {
  private config: LLMConfig;
  private openai: any;

  constructor(config: LLMConfig) {
    this.config = config;

    const OpenAI = require('openai');
    this.openai = new OpenAI({
      apiKey: config.apiKey,
      baseURL: `${config.azureEndpoint}/openai/deployments/${config.azureDeployment}`,
      defaultQuery: { 'api-version': config.azureApiVersion || '2024-02-01' },
      defaultHeaders: { 'api-key': config.apiKey },
    });
  }

  async chat(options: ChatOptions): Promise<ChatResponse> {
    const response = await this.openai.chat.completions.create({
      model: '', // Azure uses deployment name in URL
      messages: options.messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      top_p: options.topP ?? this.config.topP,
      stop: options.stopSequences,
    });

    return {
      content: response.choices[0].message.content || '',
      finishReason: this.mapFinishReason(response.choices[0].finish_reason),
      usage: {
        promptTokens: response.usage.prompt_tokens,
        completionTokens: response.usage.completion_tokens,
        totalTokens: response.usage.total_tokens,
      },
      model: this.config.azureDeployment || 'azure-deployment',
      provider: 'azure',
    };
  }

  async *chatStream(options: ChatOptions): AsyncGenerator<StreamChunk> {
    const stream = await this.openai.chat.completions.create({
      model: '',
      messages: options.messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      const done = chunk.choices[0]?.finish_reason !== null;

      yield { content, done };
    }
  }

  getProvider(): LLMProvider {
    return 'azure';
  }

  getModel(): string {
    return this.config.azureDeployment || 'azure-deployment';
  }

  private mapFinishReason(reason: string): ChatResponse['finishReason'] {
    switch (reason) {
      case 'stop': return 'stop';
      case 'length': return 'length';
      case 'content_filter': return 'content_filter';
      default: return 'stop';
    }
  }
}

/**
 * Google Gemini Client Implementation
 */
class GeminiClient implements LLMClient {
  private config: LLMConfig;

  constructor(config: LLMConfig) {
    this.config = config;
  }

  async chat(options: ChatOptions): Promise<ChatResponse> {
    const model = this.config.model || 'gemini-2.0-flash-exp';
    const apiKey = this.config.apiKey;

    // Combine system messages with user messages for Gemini
    const systemMessage = options.messages.find(m => m.role === 'system')?.content || '';
    const userMessages = options.messages.filter(m => m.role !== 'system');

    const prompt = systemMessage
      ? `${systemMessage}\n\n${userMessages.map(m => `${m.role}: ${m.content}`).join('\n')}`
      : userMessages.map(m => m.content).join('\n');

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1/models/${model}:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: options.temperature ?? this.config.temperature ?? 0.7,
            maxOutputTokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
            topP: options.topP ?? this.config.topP,
            stopSequences: options.stopSequences,
          },
        }),
      }
    );

    const data = await response.json();
    const content = data.candidates?.[0]?.content?.parts?.[0]?.text || '';

    // Gemini doesn't provide token counts in the same way
    const estimatedTokens = Math.ceil(content.length / 4);

    return {
      content,
      finishReason: 'stop',
      usage: {
        promptTokens: Math.ceil(prompt.length / 4),
        completionTokens: estimatedTokens,
        totalTokens: Math.ceil((prompt.length + content.length) / 4),
      },
      model,
      provider: 'gemini',
    };
  }

  async *chatStream(options: ChatOptions): AsyncGenerator<StreamChunk> {
    // Gemini streaming implementation
    const response = await this.chat(options);
    yield { content: response.content, done: true };
  }

  getProvider(): LLMProvider {
    return 'gemini';
  }

  getModel(): string {
    return this.config.model || 'gemini-2.0-flash-exp';
  }
}

/**
 * Anthropic Claude (via AWS Bedrock) Client Implementation
 */
class ClaudeClient implements LLMClient {
  private config: LLMConfig;

  constructor(config: LLMConfig) {
    this.config = config;
  }

  async chat(options: ChatOptions): Promise<ChatResponse> {
    const { BedrockRuntimeClient, InvokeModelCommand } = require('@aws-sdk/client-bedrock-runtime');

    const client = new BedrockRuntimeClient({
      region: this.config.awsRegion || 'us-east-1',
      credentials: {
        accessKeyId: this.config.awsAccessKeyId!,
        secretAccessKey: this.config.awsSecretAccessKey!,
      },
    });

    const systemMessage = options.messages.find(m => m.role === 'system')?.content || '';
    const conversationMessages = options.messages.filter(m => m.role !== 'system');

    const command = new InvokeModelCommand({
      modelId: this.config.model || 'anthropic.claude-3-5-sonnet-20241022-v2:0',
      body: JSON.stringify({
        anthropic_version: 'bedrock-2023-05-31',
        system: systemMessage,
        messages: conversationMessages.map(m => ({
          role: m.role === 'assistant' ? 'assistant' : 'user',
          content: m.content,
        })),
        max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
        temperature: options.temperature ?? this.config.temperature ?? 0.7,
        top_p: options.topP ?? this.config.topP,
        stop_sequences: options.stopSequences,
      }),
    });

    const response = await client.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));

    return {
      content: responseBody.content[0].text,
      finishReason: responseBody.stop_reason === 'end_turn' ? 'stop' : 'length',
      usage: {
        promptTokens: responseBody.usage.input_tokens,
        completionTokens: responseBody.usage.output_tokens,
        totalTokens: responseBody.usage.input_tokens + responseBody.usage.output_tokens,
      },
      model: this.config.model || 'claude-3-5-sonnet',
      provider: 'claude',
    };
  }

  async *chatStream(options: ChatOptions): AsyncGenerator<StreamChunk> {
    // Claude streaming would require InvokeModelWithResponseStreamCommand
    const response = await this.chat(options);
    yield { content: response.content, done: true };
  }

  getProvider(): LLMProvider {
    return 'claude';
  }

  getModel(): string {
    return this.config.model || 'anthropic.claude-3-5-sonnet-20241022-v2:0';
  }
}

/**
 * Ollama Local Client Implementation
 */
class OllamaClient implements LLMClient {
  private config: LLMConfig;

  constructor(config: LLMConfig) {
    this.config = config;
  }

  async chat(options: ChatOptions): Promise<ChatResponse> {
    const baseUrl = this.config.baseURL || 'http://localhost:11434';
    const model = this.config.model || 'llama3.2:latest';

    // Format messages into a prompt for Ollama
    const prompt = options.messages
      .map(m => {
        if (m.role === 'system') return `System: ${m.content}`;
        if (m.role === 'user') return `User: ${m.content}`;
        return `Assistant: ${m.content}`;
      })
      .join('\n\n');

    const response = await fetch(`${baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        prompt: prompt + '\n\nAssistant:',
        stream: false,
        options: {
          temperature: options.temperature ?? this.config.temperature ?? 0.7,
          num_predict: options.maxTokens ?? this.config.maxTokens ?? 1000,
          top_p: options.topP ?? this.config.topP,
          stop: options.stopSequences,
        },
      }),
    });

    const data = await response.json();

    return {
      content: data.response,
      finishReason: data.done ? 'stop' : 'length',
      usage: {
        promptTokens: data.prompt_eval_count || 0,
        completionTokens: data.eval_count || 0,
        totalTokens: (data.prompt_eval_count || 0) + (data.eval_count || 0),
      },
      model,
      provider: 'ollama',
    };
  }

  async *chatStream(options: ChatOptions): AsyncGenerator<StreamChunk> {
    const baseUrl = this.config.baseURL || 'http://localhost:11434';
    const model = this.config.model || 'llama3.2:latest';

    const prompt = options.messages
      .map(m => `${m.role}: ${m.content}`)
      .join('\n\n');

    const response = await fetch(`${baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        prompt: prompt + '\n\nassistant:',
        stream: true,
        options: {
          temperature: options.temperature ?? this.config.temperature ?? 0.7,
          num_predict: options.maxTokens ?? this.config.maxTokens ?? 1000,
        },
      }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim());

      for (const line of lines) {
        const data = JSON.parse(line);
        yield {
          content: data.response || '',
          done: data.done,
        };
      }
    }
  }

  getProvider(): LLMProvider {
    return 'ollama';
  }

  getModel(): string {
    return this.config.model || 'llama3.2:latest';
  }
}

/**
 * Utility: Get provider pricing information
 */
export function getProviderPricing(provider: LLMProvider): {
  name: string;
  inputCostPer1M: number;
  outputCostPer1M: number;
  free: boolean;
} {
  switch (provider) {
    case 'openai':
      return {
        name: 'OpenAI gpt-4o-mini',
        inputCostPer1M: 0.15,
        outputCostPer1M: 0.60,
        free: false,
      };
    case 'azure':
      return {
        name: 'Azure OpenAI',
        inputCostPer1M: 0.15,
        outputCostPer1M: 0.60,
        free: false,
      };
    case 'gemini':
      return {
        name: 'Google Gemini 2.0 Flash',
        inputCostPer1M: 0.075,
        outputCostPer1M: 0.30,
        free: false,
      };
    case 'claude':
      return {
        name: 'Anthropic Claude 3.5 Sonnet',
        inputCostPer1M: 3.00,
        outputCostPer1M: 15.00,
        free: false,
      };
    case 'ollama':
      return {
        name: 'Ollama (Local)',
        inputCostPer1M: 0,
        outputCostPer1M: 0,
        free: true,
      };
  }
}

/**
 * Utility: Calculate cost for a response
 */
export function calculateCost(response: ChatResponse): number {
  const pricing = getProviderPricing(response.provider);

  const inputCost = (response.usage.promptTokens / 1_000_000) * pricing.inputCostPer1M;
  const outputCost = (response.usage.completionTokens / 1_000_000) * pricing.outputCostPer1M;

  return inputCost + outputCost;
}
