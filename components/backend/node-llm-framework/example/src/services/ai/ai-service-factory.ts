import azureSimple from './azure-simple.service';
import geminiSimple from './gemini-simple.service';
import claudeSimple from './claude-simple.service';
import novaSimple from './nova-simple.service';
import { BaseAIService } from './base-ai.interface';
import { modelCapabilities } from '../../config/model-capabilities';

export class AIServiceFactory {
  static getService(modelId: string): BaseAIService {
    const provider = modelCapabilities.getProvider(modelId);

    switch (provider) {
      case 'azure':
        return azureSimple;
      case 'google':
        return geminiSimple;
      case 'bedrock':
        if (modelId.includes('claude')) {
          return claudeSimple;
        }
        if (modelId.includes('nova')) {
          return novaSimple;
        }
        throw new Error(`Unknown Bedrock model: ${modelId}`);
      default:
        throw new Error(`Unknown provider for model: ${modelId}`);
    }
  }

  static isSupported(modelId: string): boolean {
    return ['azure', 'google', 'bedrock'].includes(modelCapabilities.getProvider(modelId));
  }

  static getSupportedModels(): string[] {
    return modelCapabilities.getAllModels().filter((id) => this.isSupported(id));
  }
}

export default AIServiceFactory;
