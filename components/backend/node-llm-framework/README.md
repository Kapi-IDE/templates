# Node.js LLM Framework

Production-ready TypeScript services for calling Azure OpenAI, Google Gemini, Anthropic Claude, and Amazon Nova through a unified `BaseAIService` interface.

## What's Included
- `BaseAIService` interface and task-analysis schema
- Provider-specific services (`azure`, `gemini`, `claude`, `nova`)
- `AIServiceFactory` for route-by-model logic
- `model-capabilities.ts` + `models.tsv` lookup table
- Example project with TypeScript config and dependencies

## Installation
```bash
# copy component into your project using the installer
kapi components install backend/node-llm-framework --target src

# install runtime dependencies
npm install @google/genai @aws-sdk/client-bedrock-runtime openai dotenv
```

## Usage
```ts
import AIServiceFactory from './services/ai/ai-service-factory';

const ai = AIServiceFactory.getService('gemini-2.5-pro');
const response = await ai.generateText({
  prompt: 'Summarise the patient symptoms',
  systemPrompt: 'You triage medical requests safely.',
});
```

See the `example/` folder for a ready-to-run TypeScript project.
