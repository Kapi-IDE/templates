/**
 * LLM Selector Component
 *
 * React component for selecting and configuring LLM providers
 * Supports: OpenAI, Azure OpenAI, Gemini, Claude (Bedrock), Ollama
 *
 * Usage:
 * ```tsx
 * import { LLMSelector } from '@/components/LLMSelector';
 *
 * function MyApp() {
 *   const [config, setConfig] = useState<LLMConfig | null>(null);
 *
 *   return (
 *     <LLMSelector
 *       onConfigChange={setConfig}
 *       showPricing={true}
 *       allowedProviders={['openai', 'gemini', 'ollama']}
 *     />
 *   );
 * }
 * ```
 */

'use client';

import React, { useState, useEffect } from 'react';
import type { LLMProvider, LLMConfig } from '../../../backend/universal-llm-client/lib/universal-llm';

export interface LLMSelectorProps {
  /** Callback when configuration changes */
  onConfigChange?: (config: LLMConfig | null) => void;

  /** Initial provider selection */
  defaultProvider?: LLMProvider;

  /** Initial configuration */
  defaultConfig?: Partial<LLMConfig>;

  /** Show pricing information */
  showPricing?: boolean;

  /** Show model selection dropdown */
  showModelSelection?: boolean;

  /** Show advanced settings (temperature, maxTokens, etc.) */
  showAdvancedSettings?: boolean;

  /** Allowed providers (default: all) */
  allowedProviders?: LLMProvider[];

  /** Custom styling */
  className?: string;

  /** Compact mode (smaller UI) */
  compact?: boolean;
}

interface ProviderInfo {
  name: string;
  description: string;
  cost: string;
  freeOption: boolean;
  requiresSetup: string[];
  models: { value: string; label: string; cost?: string }[];
  docs: string;
}

const PROVIDER_INFO: Record<LLMProvider, ProviderInfo> = {
  openai: {
    name: 'OpenAI',
    description: 'Most reliable, best documentation',
    cost: '$0.15-$30 per 1M tokens',
    freeOption: false,
    requiresSetup: ['OPENAI_API_KEY'],
    models: [
      { value: 'gpt-4o-mini', label: 'GPT-4o Mini (Recommended)', cost: '$0.15/$0.60 per 1M' },
      { value: 'gpt-4o', label: 'GPT-4o (Best Quality)', cost: '$2.50/$10 per 1M' },
      { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo (Budget)', cost: '$0.50/$1.50 per 1M' },
    ],
    docs: 'https://platform.openai.com/docs',
  },
  azure: {
    name: 'Azure OpenAI',
    description: 'Enterprise SLA, data residency',
    cost: 'Same as OpenAI',
    freeOption: false,
    requiresSetup: ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT'],
    models: [
      { value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
      { value: 'gpt-4o', label: 'GPT-4o' },
      { value: 'gpt-35-turbo', label: 'GPT-3.5 Turbo' },
    ],
    docs: 'https://learn.microsoft.com/azure/ai-services/openai/',
  },
  gemini: {
    name: 'Google Gemini',
    description: 'Cheapest cloud option',
    cost: '$0.075-$7 per 1M tokens',
    freeOption: true,
    requiresSetup: ['GEMINI_API_KEY'],
    models: [
      { value: 'gemini-2.0-flash-exp', label: 'Gemini 2.0 Flash (Fastest)', cost: '$0.075/$0.30 per 1M' },
      { value: 'gemini-1.5-pro', label: 'Gemini 1.5 Pro (Best)', cost: '$1.25/$5 per 1M' },
    ],
    docs: 'https://ai.google.dev/docs',
  },
  claude: {
    name: 'Anthropic Claude',
    description: 'Best reasoning, long context',
    cost: '$3-$15 per 1M tokens',
    freeOption: false,
    requiresSetup: ['AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'],
    models: [
      { value: 'anthropic.claude-3-5-sonnet-20241022-v2:0', label: 'Claude 3.5 Sonnet', cost: '$3/$15 per 1M' },
      { value: 'anthropic.claude-3-haiku-20240307-v1:0', label: 'Claude 3 Haiku (Fastest)', cost: '$0.25/$1.25 per 1M' },
    ],
    docs: 'https://docs.anthropic.com/',
  },
  ollama: {
    name: 'Ollama (Local)',
    description: 'FREE, runs on your computer',
    cost: 'FREE',
    freeOption: true,
    requiresSetup: [],
    models: [
      { value: 'llama3.2:latest', label: 'Llama 3.2 (3B - Fast)', cost: 'FREE' },
      { value: 'llama3.2:7b', label: 'Llama 3.2 7B (Better)', cost: 'FREE' },
      { value: 'llama3.2:70b', label: 'Llama 3.2 70B (Best)', cost: 'FREE' },
      { value: 'mistral:latest', label: 'Mistral 7B', cost: 'FREE' },
      { value: 'codellama:latest', label: 'CodeLlama (Code)', cost: 'FREE' },
    ],
    docs: 'https://ollama.ai/docs',
  },
};

export function LLMSelector({
  onConfigChange,
  defaultProvider = 'openai',
  defaultConfig,
  showPricing = true,
  showModelSelection = true,
  showAdvancedSettings = false,
  allowedProviders,
  className = '',
  compact = false,
}: LLMSelectorProps) {
  const [provider, setProvider] = useState<LLMProvider>(defaultProvider);
  const [config, setConfig] = useState<Partial<LLMConfig>>({
    provider: defaultProvider,
    model: PROVIDER_INFO[defaultProvider].models[0].value,
    temperature: 0.7,
    maxTokens: 1000,
    ...defaultConfig,
  });

  const providers = allowedProviders || (['openai', 'azure', 'gemini', 'claude', 'ollama'] as LLMProvider[]);
  const info = PROVIDER_INFO[provider];

  // Update parent when config changes
  useEffect(() => {
    if (onConfigChange) {
      // Only emit if we have required fields
      const isValid = validateConfig(config);
      onConfigChange(isValid ? (config as LLMConfig) : null);
    }
  }, [config, onConfigChange]);

  const validateConfig = (cfg: Partial<LLMConfig>): boolean => {
    if (!cfg.provider) return false;

    switch (cfg.provider) {
      case 'openai':
        return !!cfg.apiKey && !!cfg.model;
      case 'azure':
        return !!cfg.apiKey && !!cfg.azureEndpoint && !!cfg.azureDeployment;
      case 'gemini':
        return !!cfg.apiKey && !!cfg.model;
      case 'claude':
        return !!cfg.awsAccessKeyId && !!cfg.awsSecretAccessKey && !!cfg.model;
      case 'ollama':
        return !!cfg.model;
      default:
        return false;
    }
  };

  const handleProviderChange = (newProvider: LLMProvider) => {
    setProvider(newProvider);
    setConfig({
      provider: newProvider,
      model: PROVIDER_INFO[newProvider].models[0].value,
      temperature: config.temperature || 0.7,
      maxTokens: config.maxTokens || 1000,
    });
  };

  const updateConfig = (updates: Partial<LLMConfig>) => {
    setConfig(prev => ({ ...prev, ...updates }));
  };

  return (
    <div className={`llm-selector ${compact ? 'compact' : ''} ${className}`}>
      {/* Provider Selection */}
      <div className="provider-select">
        <label className="label">LLM Provider</label>
        <select
          value={provider}
          onChange={(e) => handleProviderChange(e.target.value as LLMProvider)}
          className="select"
        >
          {providers.map((p) => (
            <option key={p} value={p}>
              {PROVIDER_INFO[p].name}
              {PROVIDER_INFO[p].freeOption && ' (FREE)'}
            </option>
          ))}
        </select>

        {!compact && (
          <p className="description">{info.description}</p>
        )}

        {showPricing && !compact && (
          <p className="pricing">
            {info.freeOption ? '✅ FREE' : `💰 ${info.cost}`}
          </p>
        )}
      </div>

      {/* Model Selection */}
      {showModelSelection && (
        <div className="model-select">
          <label className="label">Model</label>
          <select
            value={config.model || info.models[0].value}
            onChange={(e) => updateConfig({ model: e.target.value })}
            className="select"
          >
            {info.models.map((model) => (
              <option key={model.value} value={model.value}>
                {model.label}
                {showPricing && model.cost && ` - ${model.cost}`}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Provider-Specific Configuration */}
      {provider === 'openai' && (
        <div className="config-section">
          <label className="label">API Key</label>
          <input
            type="password"
            placeholder="sk-proj-..."
            value={config.apiKey || ''}
            onChange={(e) => updateConfig({ apiKey: e.target.value })}
            className="input"
          />
          <a
            href="https://platform.openai.com/api-keys"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Get API Key →
          </a>
        </div>
      )}

      {provider === 'azure' && (
        <div className="config-section">
          <label className="label">API Key</label>
          <input
            type="password"
            placeholder="Azure OpenAI API Key"
            value={config.apiKey || ''}
            onChange={(e) => updateConfig({ apiKey: e.target.value })}
            className="input"
          />

          <label className="label">Endpoint</label>
          <input
            type="text"
            placeholder="https://your-resource.openai.azure.com"
            value={config.azureEndpoint || ''}
            onChange={(e) => updateConfig({ azureEndpoint: e.target.value })}
            className="input"
          />

          <label className="label">Deployment Name</label>
          <input
            type="text"
            placeholder="your-deployment"
            value={config.azureDeployment || ''}
            onChange={(e) => updateConfig({ azureDeployment: e.target.value })}
            className="input"
          />

          <a
            href="https://portal.azure.com"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Azure Portal →
          </a>
        </div>
      )}

      {provider === 'gemini' && (
        <div className="config-section">
          <label className="label">API Key</label>
          <input
            type="password"
            placeholder="Gemini API Key"
            value={config.apiKey || ''}
            onChange={(e) => updateConfig({ apiKey: e.target.value })}
            className="input"
          />
          <a
            href="https://makersuite.google.com/app/apikey"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Get API Key →
          </a>
        </div>
      )}

      {provider === 'claude' && (
        <div className="config-section">
          <label className="label">AWS Region</label>
          <input
            type="text"
            placeholder="us-east-1"
            value={config.awsRegion || 'us-east-1'}
            onChange={(e) => updateConfig({ awsRegion: e.target.value })}
            className="input"
          />

          <label className="label">AWS Access Key ID</label>
          <input
            type="password"
            placeholder="AKIAIOSFODNN7EXAMPLE"
            value={config.awsAccessKeyId || ''}
            onChange={(e) => updateConfig({ awsAccessKeyId: e.target.value })}
            className="input"
          />

          <label className="label">AWS Secret Access Key</label>
          <input
            type="password"
            placeholder="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
            value={config.awsSecretAccessKey || ''}
            onChange={(e) => updateConfig({ awsSecretAccessKey: e.target.value })}
            className="input"
          />

          <a
            href="https://aws.amazon.com/bedrock"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            AWS Bedrock →
          </a>
        </div>
      )}

      {provider === 'ollama' && (
        <div className="config-section">
          <label className="label">Ollama URL</label>
          <input
            type="text"
            placeholder="http://localhost:11434"
            value={config.baseURL || 'http://localhost:11434'}
            onChange={(e) => updateConfig({ baseURL: e.target.value })}
            className="input"
          />

          {!compact && (
            <div className="info-box">
              <p><strong>Setup Ollama:</strong></p>
              <ol>
                <li>Install: <code>brew install ollama</code> (macOS)</li>
                <li>Start: <code>ollama serve</code></li>
                <li>Pull model: <code>ollama pull llama3.2</code></li>
              </ol>
            </div>
          )}

          <a
            href="https://ollama.ai"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Ollama Docs →
          </a>
        </div>
      )}

      {/* Advanced Settings */}
      {showAdvancedSettings && (
        <details className="advanced-settings">
          <summary>Advanced Settings</summary>

          <label className="label">
            Temperature ({config.temperature})
            <span className="hint">Higher = more creative</span>
          </label>
          <input
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={config.temperature || 0.7}
            onChange={(e) => updateConfig({ temperature: parseFloat(e.target.value) })}
            className="slider"
          />

          <label className="label">
            Max Tokens ({config.maxTokens})
          </label>
          <input
            type="number"
            min="100"
            max="4000"
            value={config.maxTokens || 1000}
            onChange={(e) => updateConfig({ maxTokens: parseInt(e.target.value) })}
            className="input"
          />
        </details>
      )}

      {/* Documentation Link */}
      {!compact && (
        <div className="docs-link">
          <a href={info.docs} target="_blank" rel="noopener noreferrer">
            📚 View {info.name} Documentation →
          </a>
        </div>
      )}
    </div>
  );
}

// Default styles (can be overridden)
const defaultStyles = `
.llm-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: white;
}

.llm-selector.compact {
  gap: 0.5rem;
  padding: 0.75rem;
}

.label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #374151;
}

.description {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.pricing {
  font-size: 0.875rem;
  font-weight: 600;
  color: #059669;
}

.select,
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.select:focus,
.input:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.link {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #3b82f6;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.config-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 0.5rem;
}

.info-box {
  padding: 0.75rem;
  background: #f3f4f6;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.info-box code {
  background: #e5e7eb;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.advanced-settings {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e5e7eb;
}

.advanced-settings summary {
  cursor: pointer;
  font-weight: 600;
  color: #374151;
}

.slider {
  width: 100%;
}

.hint {
  margin-left: 0.5rem;
  font-weight: normal;
  font-size: 0.75rem;
  color: #6b7280;
}

.docs-link {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}
`;

// Inject default styles if not already present
if (typeof document !== 'undefined' && !document.getElementById('llm-selector-styles')) {
  const styleEl = document.createElement('style');
  styleEl.id = 'llm-selector-styles';
  styleEl.textContent = defaultStyles;
  document.head.appendChild(styleEl);
}
