/**
 * AI-Powered Feedback Analysis Service
 * Uses OpenAI GPT-4 for sentiment, theme extraction, and priority ranking
 */

import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

interface AnalysisResult {
  sentiment: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
  sentimentScore: number; // -1 to 1
  sentimentReasoning: string;
  emotionalTone: string[];

  primaryTheme: string;
  secondaryThemes: string[];
  keywords: string[];

  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  priorityScore: number; // 1-100
  priorityFactors: string[];

  summary: string;
  suggestedActions: string[];
}

export async function analyzeFeedback(content: string): Promise<AnalysisResult> {
  const systemPrompt = `You are an expert customer feedback analyst. Analyze the feedback and provide structured insights.

Response must be valid JSON with this exact structure:
{
  "sentiment": "POSITIVE" | "NEUTRAL" | "NEGATIVE",
  "sentimentScore": number between -1 and 1,
  "sentimentReasoning": "brief explanation",
  "emotionalTone": ["frustrated", "happy", "confused", etc.],

  "primaryTheme": "main topic (e.g., 'Product Quality', 'Customer Support', 'Pricing')",
  "secondaryThemes": ["other topics"],
  "keywords": ["key phrases from feedback"],

  "priority": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "priorityScore": number 1-100,
  "priorityFactors": ["reasons for priority level"],

  "summary": "one-sentence summary",
  "suggestedActions": ["actionable recommendations"]
}

Priority Guidelines:
- CRITICAL (90-100): Urgent bugs, security issues, angry customers threatening to leave
- HIGH (70-89): Important feature requests, significant pain points, multiple complaints
- MEDIUM (40-69): General suggestions, minor issues, neutral feedback
- LOW (1-39): Praise, minor comments, low-impact suggestions`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Analyze this customer feedback:\n\n${content}` },
    ],
    response_format: { type: 'json_object' },
    temperature: 0.3,
  });

  const result = JSON.parse(response.choices[0].message.content || '{}');
  return result as AnalysisResult;
}

export async function extractThemes(feedbackList: string[]): Promise<{
  themes: Array<{ name: string; count: number; sentiment: number }>;
  insights: string;
}> {
  const systemPrompt = `Analyze multiple customer feedback entries and identify common themes.

Return JSON:
{
  "themes": [
    { "name": "theme name", "count": number, "sentiment": -1 to 1 }
  ],
  "insights": "summary of patterns and trends"
}`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: systemPrompt },
      {
        role: 'user',
        content: `Analyze these ${feedbackList.length} feedback entries:\n\n${feedbackList.join('\n---\n')}`
      },
    ],
    response_format: { type: 'json_object' },
    temperature: 0.5,
  });

  return JSON.parse(response.choices[0].message.content || '{}');
}

export async function findSimilarFeedback(
  content: string,
  existingFeedback: Array<{ id: string; content: string; summary?: string | null }>
): Promise<string[]> {
  // Use embeddings to find similar feedback
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: content,
  });

  const targetVector = embedding.data[0].embedding;

  // Get embeddings for existing feedback (in production, store these in vector DB)
  const similarities = await Promise.all(
    existingFeedback.map(async (fb) => {
      const fbEmbedding = await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: fb.summary || fb.content,
      });

      const similarity = cosineSimilarity(targetVector, fbEmbedding.data[0].embedding);
      return { id: fb.id, similarity };
    })
  );

  // Return top 3 most similar (similarity > 0.8)
  return similarities
    .filter(s => s.similarity > 0.8)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 3)
    .map(s => s.id);
}

// Helper: Cosine similarity
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}
