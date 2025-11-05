import { GoogleGenAI } from '@google/genai';
import * as dotenv from 'dotenv';
import { BaseAIService, AIGenerateOptions, AIStructuredOptions } from './base-ai.interface';
import { modelCapabilities } from '../../config/model-capabilities';

// Load environment variables
dotenv.config();

/**
 * Simplified Gemini Service - implements BaseAIService interface
 * Supports thinking tokens for Gemini 2.5+ models
 */
class GeminiSimpleService implements BaseAIService {
  private client: GoogleGenAI;

  // Gemini model mapping - simplified with 2025 models
  private readonly geminiModelMap: Record<string, string> = {
    'flash': 'gemini-2.0-flash-001',
    '2.0-flash': 'gemini-2.0-flash-001',
    '2.0-flash-lite': 'gemini-2.0-flash-lite',
    'flash-lite': 'gemini-2.0-flash-lite',
    '2.5-pro': 'gemini-2.5-pro',
    '2.5-flash': 'gemini-2.5-flash',
    'pro': 'gemini-2.5-pro',
    'default': 'gemini-2.0-flash-001'
  };

  constructor() {
    const apiKey = process.env['GEMINI_API_KEY'];
    
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY not found in environment variables');
    }

    this.client = new GoogleGenAI({ 
      apiKey: apiKey,
      // Use v1alpha for latest features
      apiVersion: 'v1alpha'
    });
  }

  /**
   * Generate text using Gemini - implements BaseAIService interface
   */
  async generateText(options: AIGenerateOptions): Promise<string> {
    const {
      prompt,
      model = 'default',
      systemPrompt,
      maxTokens = 8192,
      temperature = 0.7,
      thinkingBudget
    } = options;

    // Get the correct model ID
    const modelId = this.geminiModelMap[model] || this.geminiModelMap['default'];

    // Prepare the content - simple format
    let content = prompt;
    if (systemPrompt) {
      content = `${systemPrompt}\n\nUser: ${prompt}`;
    }

    // Build generation config with thinking budget support
    const generationConfig: any = {
      maxOutputTokens: maxTokens,
      temperature: temperature
    };

    // Add thinking budget for models that support it
    if (modelCapabilities.supportsThinking(model) && thinkingBudget !== undefined) {
      generationConfig.thinkingBudget = thinkingBudget;
    }

    // Generate content using the new SDK
    const response = await this.client.models.generateContent({
      model: modelId,
      contents: [{ role: 'user', parts: [{ text: content }] }],
      ...generationConfig
    });

    return response.text || '';
  }

  /**
   * Generate structured response using function calling
   */
  async generateStructuredResponse<T>(options: AIStructuredOptions): Promise<T> {
    const {
      prompt,
      model = 'default',
      systemPrompt,
      maxTokens = 8192,
      temperature = 0.7,
      thinkingBudget,
      schema
    } = options;

    // Get the correct model ID
    const modelId = this.geminiModelMap[model] || this.geminiModelMap['default'];

    // Prepare the content with structured output instruction
    let content = `${prompt}\n\nRespond with a JSON object matching this schema: ${JSON.stringify(schema)}`;
    if (systemPrompt) {
      content = `${systemPrompt}\n\nUser: ${content}`;
    }

    // Build generation config with thinking budget support
    const generationConfig: any = {
      maxOutputTokens: maxTokens,
      temperature: temperature
    };

    if (modelCapabilities.supportsThinking(model) && thinkingBudget !== undefined) {
      generationConfig.thinkingBudget = thinkingBudget;
    }

    // Generate content using the new SDK
    const response = await this.client.models.generateContent({
      model: modelId,
      contents: [{ role: 'user', parts: [{ text: content }] }],
      ...generationConfig
    });

    try {
      let jsonText = response.text || '{}';
      
      // Clean up markdown formatting if present
      if (jsonText.includes('```json')) {
        jsonText = jsonText.replace(/```json\s*/, '').replace(/```\s*$/, '');
      }
      
      return JSON.parse(jsonText.trim());
    } catch (error) {
      throw new Error(`Failed to parse structured response: ${error}`);
    }
  }

  /**
   * Stream text using Gemini via Google GenAI SDK
   */
  async streamText(options: AIGenerateOptions): Promise<AsyncIterable<string>> {
    const {
      prompt,
      model = 'default',
      systemPrompt,
      maxTokens = 8192,
      temperature = 0.7,
      thinkingBudget
    } = options;

    // Get the correct model ID
    const modelId = this.geminiModelMap[model] || this.geminiModelMap['default'];

    // Prepare the content - simple format
    let content = prompt;
    if (systemPrompt) {
      content = `${systemPrompt}\n\nUser: ${prompt}`;
    }

    // Build generation config with thinking budget support
    const generationConfig: any = {
      maxOutputTokens: maxTokens,
      temperature: temperature
    };

    if (modelCapabilities.supportsThinking(model) && thinkingBudget !== undefined) {
      generationConfig.thinkingBudget = thinkingBudget;
    }

    // Generate streaming content using the new SDK
    const response = await this.client.models.generateContentStream({
      model: modelId,
      contents: [{ role: 'user', parts: [{ text: content }] }],
      ...generationConfig
    });

    // Return async generator for streaming
    return this.transformStream(response);
  }

  /**
   * Generate embeddings using Gemini embedding models
   */
  async generateEmbedding(
    text: string,
    model: string = 'text-embedding-004'
  ): Promise<number[]> {
    // Remove unused parameter warnings
    void text;
    void model;
    
    try {
      // Note: Embedding generation might require different API calls
      // This is a placeholder for the actual embedding implementation
      throw new Error('Embedding generation not yet implemented with new SDK');
    } catch (error) {
      throw new Error(`Gemini embedding failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Transform Gemini streaming response to simple text chunks
   */
  private async *transformStream(stream: AsyncIterable<any>): AsyncGenerator<string> {
    try {
      for await (const chunk of stream) {
        if (chunk.text) {
          yield chunk.text;
        }
      }
    } catch (error) {
      console.error('Error in Gemini stream transformation:', error);
      yield `Error: ${error instanceof Error ? error.message : String(error)}`;
    }
  }

  /**
   * Check if model supports thinking tokens
   */
  supportsThinking(): boolean {
    // Gemini 2.5+ models support thinking tokens
    return true; // Service supports thinking, but checked per model
  }

  /**
   * Check if model supports structured output
   */
  supportsStructuredOutput(): boolean {
    return true;
  }

  /**
   * Get available models for this service
   */
  getAvailableModels(): string[] {
    return Object.keys(this.geminiModelMap);
  }

  /**
   * Test if Gemini service is properly configured
   */
  async test(): Promise<boolean> {
    try {
      const response = await this.generateText({
        prompt: "Hello! Just say 'OK' to confirm you're working.",
        maxTokens: 10
      });
      return response.trim().length > 0;
    } catch (error) {
      console.error('Gemini service test failed:', error);
      return false;
    }
  }
}

export default new GeminiSimpleService();