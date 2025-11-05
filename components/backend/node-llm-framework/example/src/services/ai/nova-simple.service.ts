import { BedrockRuntimeClient, InvokeModelCommand, InvokeModelWithResponseStreamCommand } from "@aws-sdk/client-bedrock-runtime";
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Simplified Nova Service using AWS Bedrock
 * Based on official AWS documentation patterns for Nova models
 */
class NovaSimpleService {
  private client: BedrockRuntimeClient;

  // Nova model mapping - simplified
  private readonly novaModelMap: Record<string, string> = {
    'micro': 'us.amazon.nova-micro-v1:0',
    'lite': 'us.amazon.nova-lite-v1:0', 
    'pro': 'us.amazon.nova-pro-v1:0',
    'premier': 'us.amazon.nova-premier-v1:0',
    'default': 'us.amazon.nova-pro-v1:0'
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
   * Generate text using Nova via AWS Bedrock
   * Simple, clean implementation following AWS Nova patterns
   */
  async generateText(options: {
    prompt: string;
    model?: string;
    systemPrompt?: string;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
  }): Promise<string> {
    const {
      prompt,
      model = 'default',
      systemPrompt = 'You are a helpful, harmless, and honest AI assistant.',
      maxTokens = 4000,
      temperature = 0.7,
      topP = 0.9
    } = options;

    // Get the correct model ID
    const modelId = this.novaModelMap[model] || this.novaModelMap['default'];

    // Prepare the payload - following AWS Bedrock Nova format
    const payload = {
      schemaVersion: 'messages-v1',
      messages: [
        {
          role: 'user',
          content: [{ text: prompt }]
        }
      ],
      system: [
        {
          text: systemPrompt
        }
      ],
      inferenceConfig: {
        maxTokens: maxTokens,
        temperature: temperature,
        topP: topP
      }
    };

    // Create and send the command
    const command = new InvokeModelCommand({
      contentType: "application/json",
      accept: "application/json",
      modelId: modelId,
      body: JSON.stringify(payload)
    });

    const response = await this.client.send(command);
    
    // Decode and parse response
    const decodedResponseBody = new TextDecoder().decode(response.body);
    const responseBody = JSON.parse(decodedResponseBody);
    
    return responseBody.output.message.content[0].text;
  }

  /**
   * Stream text using Nova via AWS Bedrock
   */
  async streamText(options: {
    prompt: string;
    model?: string;
    systemPrompt?: string;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
  }): Promise<AsyncIterable<string>> {
    const {
      prompt,
      model = 'default',
      systemPrompt = 'You are a helpful, harmless, and honest AI assistant.',
      maxTokens = 4000,
      temperature = 0.7,
      topP = 0.9
    } = options;

    // Get the correct model ID
    const modelId = this.novaModelMap[model] || this.novaModelMap['default'];

    // Prepare the payload - same format as non-streaming
    const payload = {
      schemaVersion: 'messages-v1',
      messages: [
        {
          role: 'user',
          content: [{ text: prompt }]
        }
      ],
      system: [
        {
          text: systemPrompt
        }
      ],
      inferenceConfig: {
        maxTokens: maxTokens,
        temperature: temperature,
        topP: topP
      }
    };

    // Create streaming command
    const command = new InvokeModelWithResponseStreamCommand({
      contentType: "application/json",
      accept: "application/json",
      modelId: modelId,
      body: JSON.stringify(payload)
    });

    const response = await this.client.send(command);
    
    if (!response.body) {
      throw new Error('No response stream received from Nova model');
    }

    // Return async generator for streaming
    return this.transformStream(response.body);
  }

  /**
   * Transform Nova streaming response to simple text chunks
   */
  private async *transformStream(stream: AsyncIterable<any>): AsyncGenerator<string> {
    for await (const chunk of stream) {
      if (chunk.chunk?.bytes) {
        try {
          const textResponse = new TextDecoder().decode(chunk.chunk.bytes);
          const jsonResponse = JSON.parse(textResponse);

          // Nova streaming format has contentBlockDelta with text chunks
          if (jsonResponse.contentBlockDelta?.delta?.text) {
            yield jsonResponse.contentBlockDelta.delta.text;
          }
        } catch (parseError) {
          console.error('Error parsing Nova stream chunk:', parseError);
        }
      }
    }
  }

  /**
   * Test if Nova service is properly configured
   */
  async test(): Promise<boolean> {
    try {
      const response = await this.generateText({
        prompt: "Hello! Just say 'OK' to confirm you're working.",
        maxTokens: 10
      });
      return response.trim().length > 0;
    } catch (error) {
      console.error('Nova service test failed:', error);
      return false;
    }
  }
}

export default new NovaSimpleService();