import { AzureOpenAI } from 'openai';
import * as dotenv from 'dotenv';
import { BaseAIService, AIGenerateOptions, AIStructuredOptions, AIMessageContent } from './base-ai.interface';

// Load environment variables
dotenv.config();

/**
 * Simplified Azure OpenAI Service - implements BaseAIService interface
 */
class AzureSimpleService implements BaseAIService {
  private createClient(model: string): AzureOpenAI {
    const apiKey = process.env['AZURE_API_KEY'];
    const endpoint = process.env['AZURE_ENDPOINT'] || "https://kapi1585655068.cognitiveservices.azure.com/";

    if (!apiKey) {
      throw new Error("AZURE_API_KEY not found in environment variables");
    }

    return new AzureOpenAI({
      apiVersion: "2024-12-01-preview",
      endpoint,
      apiKey,
      deployment: model
    });
  }

  /**
   * Convert AIMessageContent to OpenAI message format
   */
  private formatMessageContent(content: AIMessageContent): any {
    if (typeof content === 'string') {
      return content;
    }
    
    // Multimodal content - array of text and images
    return content.map(item => {
      if (item.type === 'text') {
        return {
          type: 'text',
          text: item.text
        };
      } else if (item.type === 'image_url') {
        return {
          type: 'image_url',
          image_url: {
            url: item.image_url.url,
            detail: item.image_url.detail || 'auto'
          }
        };
      }
      return item;
    });
  }

  /**
   * Generate text using any Azure OpenAI model
   * Implements BaseAIService interface with multimodal support
   */
  async generateText(options: AIGenerateOptions): Promise<string> {
    const {
      prompt,
      model = "gpt-4.1",
      systemPrompt = "You are a helpful assistant.",
      maxTokens = 16384,
      temperature = 0.7
    } = options;

    const apiKey = process.env['AZURE_API_KEY'];
    const endpoint = process.env['AZURE_ENDPOINT'] || "https://kapi1585655068.cognitiveservices.azure.com/";
    const client = this.createClient(model);

    const messages: any[] = [
      { role: "system", content: systemPrompt },
      { role: "user", content: this.formatMessageContent(prompt) }
    ];

    // Pass model as deployment name - matching Python: model=deployment
    // Build request parameters
    const requestParams: any = {
      messages,
      max_completion_tokens: maxTokens,
      model: model  // This acts as the deployment name
    };

    // Only add temperature for models that support it
    const { modelCapabilities } = await import('../../config/model-capabilities');
    if (modelCapabilities.supportsTemperature(model)) {
      requestParams.temperature = temperature;
    }

    try {
      const response = await client.chat.completions.create(requestParams);
      return response.choices[0].message.content || '';
    } catch (error: any) {
      const maskedKey = apiKey ? `${apiKey.slice(0, 2)}***${apiKey.slice(-2)}` : 'undefined';
      console.error('[AzureSimpleService] generateText error', {
        endpoint,
        model,
        maskedKey,
        status: error?.status,
        code: error?.code,
        type: error?.type,
        message: error?.message,
      });
      throw error;
    }
  }

  /**
   * Stream text using any Azure OpenAI model
   */
  /**
   * Generate structured response using function calling
   */
  async generateStructuredResponse<T>(options: AIStructuredOptions): Promise<T> {
    const {
      prompt,
      model = "gpt-4.1",
      systemPrompt = "You are a helpful assistant.",
      maxTokens = 16384,
      temperature = 0.7,
      schema
    } = options;

    const apiKey = process.env['AZURE_API_KEY'];
    const endpoint = process.env['AZURE_ENDPOINT'] || "https://kapi1585655068.cognitiveservices.azure.com/";
    const client = this.createClient(model);

    const messages: any[] = [
      { role: "system", content: systemPrompt },
      { role: "user", content: this.formatMessageContent(prompt) }
    ];

    // Build request parameters
    const requestParams: any = {
      messages,
      max_completion_tokens: maxTokens,
      model: model,
      functions: [{
        name: "structured_response",
        description: "Return structured response",
        parameters: schema
      }],
      function_call: { name: "structured_response" }
    };

    // Only add temperature for models that support it
    const { modelCapabilities } = await import('../../config/model-capabilities');
    if (modelCapabilities.supportsTemperature(model)) {
      requestParams.temperature = temperature;
    }

    let response;
    try {
      response = await client.chat.completions.create(requestParams);
    } catch (error: any) {
      const maskedKey = apiKey ? `${apiKey.slice(0, 2)}***${apiKey.slice(-2)}` : 'undefined';
      console.error('[AzureSimpleService] generateStructuredResponse error', {
        endpoint,
        model,
        maskedKey,
        status: error?.status,
        code: error?.code,
        type: error?.type,
        message: error?.message,
      });
      throw error;
    }

    const functionCall = response.choices[0].message.function_call;
    if (functionCall && functionCall.arguments) {
      return JSON.parse(functionCall.arguments);
    }
    
    throw new Error("No structured response received");
  }

  /**
   * Stream text using any Azure OpenAI model
   */
  async streamText(options: AIGenerateOptions): Promise<AsyncIterable<string>> {
    const {
      prompt,
      model = "gpt-4.1",
      systemPrompt = "You are a helpful assistant.",
      maxTokens = 16384,
      temperature = 0.7
    } = options;

    const messages: any[] = [
      { role: "system", content: systemPrompt },
      { role: "user", content: this.formatMessageContent(prompt) }
    ];

    // Build request parameters
    const requestParams: any = {
      messages,
      max_completion_tokens: maxTokens,
      model,
      stream: true
    };

    // Only add temperature for models that support it
    const { modelCapabilities } = await import('../../config/model-capabilities');
    if (modelCapabilities.supportsTemperature(model)) {
      requestParams.temperature = temperature;
    }

    const apiKey = process.env['AZURE_API_KEY'];
    const endpoint = process.env['AZURE_ENDPOINT'] || "https://kapi1585655068.cognitiveservices.azure.com/";
    const client = this.createClient(model);

    const stream = await client.chat.completions.create(requestParams);

    return this.transformStream(stream);
  }

  /**
   * Simple stream transformer - yields just the text content
   */
  private async *transformStream(stream: AsyncIterable<any>): AsyncGenerator<string> {
    for await (const chunk of stream) {
      const content = chunk.choices?.[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  }

  /**
   * Generate embeddings using Azure OpenAI embedding models
   */
  async generateEmbedding(
    text: string,
    model: string = 'text-embedding-3-small'
  ): Promise<number[]> {
    const apiKey = process.env['AZURE_API_KEY'];
    const endpoint = process.env['AZURE_ENDPOINT'] || "https://kapi1585655068.cognitiveservices.azure.com/";
    const client = this.createClient(model);

    try {
      const response = await client.embeddings.create({
        model: model,
        input: text
      });

      if (!response.data || response.data.length === 0) {
        throw new Error('No embedding data received from Azure OpenAI');
      }

      return response.data[0].embedding;
    } catch (error: any) {
      const maskedKey = apiKey ? `${apiKey.slice(0, 2)}***${apiKey.slice(-2)}` : 'undefined';
      console.error('[AzureSimpleService] generateEmbedding error', {
        endpoint,
        model,
        maskedKey,
        status: error?.status,
        code: error?.code,
        type: error?.type,
        message: error?.message,
      });
      throw error;
    }
  }

  /**
   * Check if model supports thinking tokens
   */
  supportsThinking(): boolean {
    // Azure OpenAI models don't support thinking tokens yet
    return false;
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
    return ['gpt-5', 'gpt-5-mini', 'gpt-5-nano', 'gpt-4.1', 'o3', 'o4-mini', 'text-embedding-3-small'];
  }
}

export default new AzureSimpleService();
