import { BedrockRuntimeClient, InvokeModelCommand, InvokeModelWithResponseStreamCommand } from "@aws-sdk/client-bedrock-runtime";
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Simplified Claude Service using AWS Bedrock
 * Based on official AWS documentation patterns
 */
class ClaudeSimpleService {
  private client: BedrockRuntimeClient;

  // Claude model mapping - simplified with correct 2025 identifiers
  private readonly claudeModelMap: Record<string, string> = {
    'haiku': 'anthropic.claude-3-haiku-20240307-v1:0',
    'sonnet': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'opus': 'anthropic.claude-3-opus-20240229-v1:0',
    '3.5-haiku': 'us.anthropic.claude-3-5-haiku-20241022-v1:0',
    // Updated to Sonnet 4.5, Sonnet 4, and Opus 4.1
    'sonnet-4-5': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
    'sonnet-4': 'anthropic.claude-sonnet-4-20250514-v1:0',
    'opus-4': 'anthropic.claude-opus-4-1-20250805-v1:0',
    'opus-4.1': 'anthropic.claude-opus-4-1-20250805-v1:0',
    // Legacy aliases (deprecated, use sonnet-4-5 instead)
    '3.5-sonnet': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
    '3.7-sonnet': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
    'sonnet-4.0': 'anthropic.claude-sonnet-4-20250514-v1:0',
    'default': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
  };

  constructor() {
    const region = process.env['AWS_REGION'] || 'us-east-1';
    
    this.client = new BedrockRuntimeClient({ 
      region,
      credentials: {
        accessKeyId: process.env['AWS_ACCESS_KEY_ID'] || '',
        secretAccessKey: process.env['AWS_SECRET_ACCESS_KEY'] || ''
      }
    });
  }

  /**
   * Generate text using Claude via AWS Bedrock
   * Simple, clean implementation matching AWS docs
   */
  async generateText(options: {
    prompt: string;
    model?: string;
    systemPrompt?: string;
    maxTokens?: number;
    temperature?: number;
  }): Promise<string> {
    const {
      prompt,
      model = 'default',
      systemPrompt,
      maxTokens = 4096,
      temperature = 0.7
    } = options;

    // Get the correct model ID
    const modelId = this.claudeModelMap[model] || this.claudeModelMap['default'];

    // Prepare the payload - following AWS Bedrock Claude format
    const payload: any = {
      anthropic_version: "bedrock-2023-05-31",
      max_tokens: maxTokens,
      messages: [
        {
          role: "user",
          content: [{ type: "text", text: prompt }]
        }
      ]
    };

    // Add system prompt if provided
    if (systemPrompt) {
      payload.system = [{ type: "text", text: systemPrompt }];
    }

    // Add temperature if supported
    if (temperature !== 0.7) {
      payload.temperature = temperature;
    }

    // Create and send the command
    const command = new InvokeModelCommand({
      contentType: "application/json",
      body: JSON.stringify(payload),
      modelId: modelId
    });

    const response = await this.client.send(command);
    
    // Decode and parse response
    const decodedResponseBody = new TextDecoder().decode(response.body);
    const responseBody = JSON.parse(decodedResponseBody);
    
    return responseBody.content[0].text;
  }

  /**
   * Stream text using Claude via AWS Bedrock
   */
  async streamText(options: {
    prompt: string;
    model?: string;
    systemPrompt?: string;
    maxTokens?: number;
    temperature?: number;
  }): Promise<AsyncIterable<string>> {
    const {
      prompt,
      model = 'default',
      systemPrompt,
      maxTokens = 4096,
      temperature = 0.7
    } = options;

    // Get the correct model ID
    const modelId = this.claudeModelMap[model] || this.claudeModelMap['default'];

    // Prepare the payload - same format as non-streaming
    const payload: any = {
      anthropic_version: "bedrock-2023-05-31",
      max_tokens: maxTokens,
      messages: [
        {
          role: "user",
          content: [{ type: "text", text: prompt }]
        }
      ]
    };

    // Add system prompt if provided
    if (systemPrompt) {
      payload.system = [{ type: "text", text: systemPrompt }];
    }

    // Add temperature if supported
    if (temperature !== 0.7) {
      payload.temperature = temperature;
    }

    // Create streaming command
    const command = new InvokeModelWithResponseStreamCommand({
      contentType: "application/json",
      body: JSON.stringify(payload),
      modelId: modelId
    });

    const response = await this.client.send(command);
    
    if (!response.body) {
      throw new Error('No response stream received from Claude model');
    }

    // Return async generator for streaming
    return this.transformStream(response.body);
  }

  /**
   * Transform Claude streaming response to simple text chunks
   */
  private async *transformStream(stream: AsyncIterable<any>): AsyncGenerator<string> {
    for await (const item of stream) {
      if (item.chunk?.bytes) {
        const chunk = JSON.parse(new TextDecoder().decode(item.chunk.bytes));
        const chunkType = chunk.type;
        
        if (chunkType === "content_block_delta" && chunk.delta?.text) {
          yield chunk.delta.text;
        }
      }
    }
  }

  /**
   * Test if Claude service is properly configured
   */
  async test(): Promise<boolean> {
    try {
      const response = await this.generateText({
        prompt: "Hello! Just say 'OK' to confirm you're working.",
        maxTokens: 10
      });
      return response.trim().length > 0;
    } catch (error) {
      console.error('Claude service test failed:', error);
      return false;
    }
  }
}

export default new ClaudeSimpleService();