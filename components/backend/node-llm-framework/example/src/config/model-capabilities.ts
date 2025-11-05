/**
 * Model Capabilities - reads from models.tsv to determine what each model supports
 */

import fs from 'fs';
import path from 'path';

interface ModelCapability {
  modelId: string;
  provider: string;
  supportsTemperature: boolean;
  supportsThinking: boolean;
  supportsToolCalling: boolean;
}

class ModelCapabilities {
  private capabilities: Map<string, ModelCapability> = new Map();

  constructor() {
    this.loadCapabilities();
  }

  private loadCapabilities(): void {
    try {
      const tsvPath = path.join(__dirname, 'models.tsv');
      const content = fs.readFileSync(tsvPath, 'utf-8');
      const lines = content.split('\n').filter(line => line.trim());
      
      // Skip header line
      for (let i = 1; i < lines.length; i++) {
        const parts = lines[i].split('\t');
        if (parts.length >= 8) {
          const capability: ModelCapability = {
            modelId: parts[0],
            provider: parts[1],
            supportsTemperature: parts[5] === 'true',
            supportsThinking: parts[6] === 'true',
            supportsToolCalling: parts[7] === 'true'
          };
          this.capabilities.set(parts[0], capability);
        }
      }
    } catch (error) {
      console.error('Error loading model capabilities:', error);
    }
  }

  supportsThinking(modelId: string): boolean {
    return this.capabilities.get(modelId)?.supportsThinking || false;
  }

  supportsToolCalling(modelId: string): boolean {
    return this.capabilities.get(modelId)?.supportsToolCalling || false;
  }

  supportsTemperature(modelId: string): boolean {
    return this.capabilities.get(modelId)?.supportsTemperature || false;
  }

  getProvider(modelId: string): string {
    return this.capabilities.get(modelId)?.provider || 'unknown';
  }

  getAllModels(): string[] {
    return Array.from(this.capabilities.keys());
  }
}

// Export singleton
export const modelCapabilities = new ModelCapabilities();
export default modelCapabilities;