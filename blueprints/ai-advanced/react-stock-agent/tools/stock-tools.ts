/**
 * Stock Trading Tools
 * Based on Modern AI Pro ReAct Framework
 *
 * Tools:
 * 1. stock_price - Get stock prices via Polygon.io
 * 2. ddgs_news - Search news via DuckDuckGo
 * 3. calculate - Python-style calculator
 */

import fetch from 'node-fetch';

/**
 * Get stock price from Polygon.io
 * Requires: POLYGON_API_KEY environment variable
 */
export async function getStockPrice(ticker: string): Promise<string> {
  try {
    const apiKey = process.env.POLYGON_API_KEY;

    if (!apiKey) {
      throw new Error('POLYGON_API_KEY not set');
    }

    // Get previous day's closing price
    const response = await fetch(
      `https://api.polygon.io/v2/aggs/ticker/${ticker.toUpperCase()}/prev?apiKey=${apiKey}`
    );

    if (!response.ok) {
      throw new Error(`Polygon API error: ${response.statusText}`);
    }

    const data: any = await response.json();

    if (!data.results || data.results.length === 0) {
      throw new Error(`No price data found for ${ticker}`);
    }

    const closePrice = data.results[0].c;
    return String(closePrice);

  } catch (error) {
    return `Error getting stock price: ${error instanceof Error ? error.message : String(error)}`;
  }
}

/**
 * Search news using DuckDuckGo
 * Free, no API key needed!
 */
export async function searchNews(query: string): Promise<string> {
  try {
    // Use duck-duck-scrape package for news search
    const { search } = await import('duck-duck-scrape');

    const results = await search(query, {
      safeSearch: 'off'
    });

    if (!results.results || results.results.length === 0) {
      return `No recent news found for ${query}.`;
    }

    // Format news results
    let newsText = '';
    const maxResults = Math.min(5, results.results.length);

    for (let i = 0; i < maxResults; i++) {
      const article = results.results[i];
      newsText += `${article.title}\n${article.description}\n\n--Next News--\n\n`;
    }

    return newsText;

  } catch (error) {
    return `Error searching news: ${error instanceof Error ? error.message : String(error)}`;
  }
}

/**
 * Calculate mathematical expressions
 * Supports Python-style syntax: result = expression
 */
export async function calculate(expression: string): Promise<string> {
  try {
    // Remove dollar signs
    let cleanExpr = expression.replace(/\$/g, '').trim();

    // Handle "result = " pattern
    if (cleanExpr.includes('result')) {
      const match = cleanExpr.match(/result\s*=\s*(.+)/);
      if (match) {
        cleanExpr = match[1];
      }
    }

    // Safe evaluation with Math support
    const safeEval = (expr: string): number => {
      // Replace common math operations
      expr = expr.replace(/\^/g, '**'); // Power operator

      // Evaluate using Function constructor (safer than eval)
      const fn = new Function('Math', `return ${expr}`);
      return fn(Math);
    };

    const result = safeEval(cleanExpr);

    // Round to 2 decimal places
    return typeof result === 'number'
      ? result.toFixed(2)
      : String(result);

  } catch (error) {
    return `Error in calculation: ${error instanceof Error ? error.message : String(error)}`;
  }
}

/**
 * Combined tool registry
 * Export this for use in ReAct agent
 */
export const stockTools = {
  stock_price: getStockPrice,
  ddgs_news: searchNews,
  calculate: calculate
};
