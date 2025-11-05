/**
 * ReAct Agent Pattern - Reusable Component
 *
 * Based on the ReAct (Reasoning + Acting) framework
 * Reference: https://arxiv.org/abs/2210.03629
 *
 * Pattern: Thought → Action → PAUSE → Observation → Repeat
 *
 * Usage:
 * ```typescript
 * const agent = new ReActAgent({
 *   llm: createLLMClient({ provider: 'openai', apiKey: '...' }),
 *   tools: {
 *     stock_price: async (ticker) => getStockPrice(ticker),
 *     calculate: async (expr) => eval(expr)
 *   },
 *   systemPrompt: 'You are a helpful assistant...'
 * });
 *
 * const result = await agent.run('What is the price of AAPL?');
 * ```
 */

import { LLMClient, Message } from '../../universal-llm-client/lib/universal-llm';

export interface Tool {
  (input: string): Promise<string> | string;
}

export interface ReActConfig {
  /** LLM client (from Universal LLM Component) */
  llm: LLMClient;

  /** Available tools the agent can use */
  tools: Record<string, Tool>;

  /** System prompt defining agent behavior */
  systemPrompt: string;

  /** Maximum reasoning steps (default: 10) */
  maxSteps?: number;

  /** Enable debug logging (default: false) */
  debug?: boolean;
}

export interface ReActStep {
  step: number;
  thought: string;
  action?: string;
  actionInput?: string;
  observation?: string;
  answer?: string;
}

export interface ReActResult {
  answer: string;
  steps: ReActStep[];
  totalSteps: number;
  success: boolean;
  error?: string;
}

/**
 * ReAct Agent - Reasoning + Acting pattern
 *
 * The agent follows this loop:
 * 1. THOUGHT: Reason about what to do next
 * 2. ACTION: Call a tool with input
 * 3. PAUSE: Wait for tool result
 * 4. OBSERVATION: Receive tool output
 * 5. Repeat until Answer is reached
 */
export class ReActAgent {
  private config: Required<ReActConfig>;
  private messages: Message[];

  constructor(config: ReActConfig) {
    this.config = {
      ...config,
      maxSteps: config.maxSteps ?? 10,
      debug: config.debug ?? false,
    };

    this.messages = [
      { role: 'system', content: config.systemPrompt }
    ];
  }

  /**
   * Run the agent with a question
   */
  async run(question: string): Promise<ReActResult> {
    const steps: ReActStep[] = [];
    let currentStep = 0;

    // Reset messages for new question
    this.messages = [
      { role: 'system', content: this.config.systemPrompt }
    ];

    // Add initial question
    this.messages.push({
      role: 'user',
      content: question
    });

    try {
      while (currentStep < this.config.maxSteps) {
        currentStep++;

        // Get LLM response
        const response = await this.config.llm.chat({
          messages: this.messages
        });

        const content = response.content;

        // Add to conversation history
        this.messages.push({
          role: 'assistant',
          content
        });

        // Parse the response
        const step = this.parseResponse(content, currentStep);
        steps.push(step);

        if (this.config.debug) {
          console.log(`\n=== Step ${currentStep} ===`);
          console.log('Thought:', step.thought);
          if (step.action) {
            console.log(`Action: ${step.action}: ${step.actionInput}`);
          }
          if (step.answer) {
            console.log('Answer:', step.answer);
          }
        }

        // Check if agent has final answer
        if (step.answer) {
          return {
            answer: step.answer,
            steps,
            totalSteps: currentStep,
            success: true
          };
        }

        // Execute action if present
        if (step.action && step.actionInput !== undefined) {
          const observation = await this.executeAction(
            step.action,
            step.actionInput
          );

          step.observation = observation;

          if (this.config.debug) {
            console.log('Observation:', observation);
          }

          // Add observation to conversation
          this.messages.push({
            role: 'user',
            content: `Observation: ${observation}`
          });
        } else {
          // No action found, likely an error
          break;
        }
      }

      // Max steps reached without answer
      return {
        answer: 'Maximum reasoning steps reached without finding an answer.',
        steps,
        totalSteps: currentStep,
        success: false,
        error: 'MAX_STEPS_EXCEEDED'
      };

    } catch (error) {
      return {
        answer: '',
        steps,
        totalSteps: currentStep,
        success: false,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Parse LLM response into structured step
   */
  private parseResponse(content: string, stepNumber: number): ReActStep {
    const step: ReActStep = {
      step: stepNumber,
      thought: '',
      action: undefined,
      actionInput: undefined,
      observation: undefined,
      answer: undefined
    };

    // Extract Thought
    const thoughtMatch = content.match(/Thought:\s*(.+?)(?=\n|Action:|Answer:|$)/s);
    if (thoughtMatch) {
      step.thought = thoughtMatch[1].trim();
    }

    // Extract Answer (final response)
    const answerMatch = content.match(/Answer:\s*(.+?)$/s);
    if (answerMatch) {
      step.answer = answerMatch[1].trim();
      return step; // If we have an answer, we're done
    }

    // Extract Action
    const actionMatch = content.match(/Action:\s*(\w+):\s*(.+?)(?=\n|PAUSE|$)/s);
    if (actionMatch) {
      step.action = actionMatch[1].trim();
      step.actionInput = actionMatch[2].trim();
    }

    return step;
  }

  /**
   * Execute a tool action
   */
  private async executeAction(action: string, input: string): Promise<string> {
    const tool = this.config.tools[action];

    if (!tool) {
      return `Error: Unknown action "${action}". Available actions: ${Object.keys(this.config.tools).join(', ')}`;
    }

    try {
      const result = await tool(input);
      return String(result);
    } catch (error) {
      return `Error executing ${action}: ${error instanceof Error ? error.message : String(error)}`;
    }
  }

  /**
   * Get conversation history
   */
  getHistory(): Message[] {
    return [...this.messages];
  }

  /**
   * Clear conversation history
   */
  clearHistory(): void {
    this.messages = [
      { role: 'system', content: this.config.systemPrompt }
    ];
  }
}

/**
 * Create a ReAct system prompt
 *
 * Helper function to generate standard ReAct prompts
 */
export function createReActPrompt(config: {
  role: string;
  tools: Record<string, { description: string; example: string }>;
  examples?: string;
}): string {
  const { role, tools, examples } = config;

  const toolDescriptions = Object.entries(tools)
    .map(([name, info]) => `${name}:\n\n${info.description}\n\ne.g. ${info.example}`)
    .join('\n\n');

  return `
You are ${role}.

You operate in a loop consisting of Thought, Action, PAUSE, and Observation.
At the end of the loop, you provide an Answer.

Use Thought to describe your reasoning about the task you have been asked to complete.
Use Action to execute one of the actions available to you, then return PAUSE.
Observation will contain the result of the action.

Your available actions are:

${toolDescriptions}

${examples ? `Example session:\n\n${examples}` : ''}

Always follow this format:
Thought: [Your reasoning]
Action: [action_name]: [action_input]
PAUSE

You will be called again with:
Observation: [result]

When you have enough information to answer, provide:
Answer: [Your final answer]
`.trim();
}

/**
 * Common ReAct tools
 */

export const commonTools = {
  /**
   * Calculator tool
   */
  calculate: async (expression: string): Promise<string> => {
    try {
      // Clean the expression
      const cleanExpr = expression.replace(/\$/g, '').trim();

      // Safe evaluation using Function constructor
      const namespace: any = {
        Math,
        result: undefined
      };

      // Execute the expression
      const fn = new Function(...Object.keys(namespace), cleanExpr);
      fn(...Object.values(namespace));

      // If expression used 'result=' pattern
      if (cleanExpr.includes('result')) {
        const resultMatch = cleanExpr.match(/result\s*=\s*(.+)/);
        if (resultMatch) {
          const evalResult = eval(resultMatch[1]);
          return String(typeof evalResult === 'number' ? evalResult.toFixed(2) : evalResult);
        }
      }

      // Direct evaluation
      const result = eval(cleanExpr);
      return String(typeof result === 'number' ? result.toFixed(2) : result);

    } catch (error) {
      return `Error in calculation: ${error instanceof Error ? error.message : String(error)}`;
    }
  },

  /**
   * Web search tool (using DuckDuckGo)
   */
  webSearch: async (query: string): Promise<string> => {
    try {
      // Use duck-duck-scrape or similar library
      // For now, return placeholder
      return `Search results for: ${query}\n[Implement with duck-duck-scrape package]`;
    } catch (error) {
      return `Error in web search: ${error instanceof Error ? error.message : String(error)}`;
    }
  }
};
