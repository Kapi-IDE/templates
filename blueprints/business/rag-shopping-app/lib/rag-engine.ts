/**
 * RAG Engine for Semantic Product Search
 * Minimal implementation with OpenAI embeddings and cosine similarity
 */

import OpenAI from 'openai';
import products from '../data/products.json';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  tags: string[];
  image: string;
}

export interface ProductWithScore extends Product {
  similarity: number;
  reasoning?: string;
}

// Cosine similarity between two vectors
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

// Generate embedding for text
export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  return response.data[0].embedding;
}

// Semantic product search using RAG
export async function semanticProductSearch(
  query: string,
  limit: number = 5
): Promise<ProductWithScore[]> {
  // 1. Generate query embedding
  const queryEmbedding = await generateEmbedding(query);

  // 2. Calculate similarity for each product
  const productsWithScores: ProductWithScore[] = [];

  for (const product of products as Product[]) {
    // Create searchable text from product
    const productText = `${product.name} ${product.description} ${product.tags.join(' ')} ${product.category}`;

    // Generate product embedding
    const productEmbedding = await generateEmbedding(productText);

    // Calculate similarity
    const similarity = cosineSimilarity(queryEmbedding, productEmbedding);

    productsWithScores.push({
      ...product,
      similarity,
    });
  }

  // 3. Sort by similarity and return top results
  return productsWithScores
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);
}

// AI-powered shopping assistant
export async function shoppingAssistant(
  query: string,
  conversationHistory: Array<{ role: 'user' | 'assistant'; content: string }> = []
): Promise<string> {
  // 1. Find relevant products using semantic search
  const relevantProducts = await semanticProductSearch(query, 5);

  // 2. Build context from products
  const productsContext = relevantProducts
    .map(p => `- ${p.name} ($${p.price}): ${p.description}`)
    .join('\n');

  // 3. Generate AI response with product context
  const systemPrompt = `You are a helpful shopping assistant. Use the provided product catalog to answer customer questions.

Available Products:
${productsContext}

Guidelines:
- Recommend products that match the customer's needs
- Mention specific product names and prices
- Be concise but helpful
- If no products match well, suggest alternatives
- Don't make up products not in the list`;

  const messages: any[] = [
    { role: 'system', content: systemPrompt },
    ...conversationHistory,
    { role: 'user', content: query },
  ];

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages,
    temperature: 0.7,
    max_tokens: 300,
  });

  return response.choices[0].message.content || 'I could not generate a response.';
}

// Generate product recommendations based on user preferences
export async function getRecommendations(
  preferences: string,
  excludeIds: string[] = [],
  limit: number = 4
): Promise<ProductWithScore[]> {
  // Use semantic search with preferences
  const results = await semanticProductSearch(preferences, limit * 2);

  // Filter out excluded products and limit
  return results
    .filter(p => !excludeIds.includes(p.id))
    .slice(0, limit);
}

// Explain why a product matches a query (for transparency)
export async function explainMatch(
  product: Product,
  query: string
): Promise<string> {
  const prompt = `Explain in 1-2 sentences why "${product.name}" is a good match for someone looking for "${query}".

Product: ${product.name}
Description: ${product.description}
Tags: ${product.tags.join(', ')}

Keep the explanation customer-friendly and focus on how it meets their needs.`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.5,
    max_tokens: 100,
  });

  return response.choices[0].message.content || 'This product matches your search.';
}
