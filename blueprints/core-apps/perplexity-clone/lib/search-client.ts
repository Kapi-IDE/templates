/**
 * Universal Search Client
 * Supports: Brave Search, Serper.dev, Google Custom Search, Bing Search
 */

export type SearchProvider = 'brave' | 'serper' | 'google' | 'bing';

export interface SearchConfig {
  provider: SearchProvider;
  maxResults?: number;
  freshness?: 'day' | 'week' | 'month' | 'year';
}

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  publishedDate?: string;
}

export interface SearchResponse {
  results: SearchResult[];
  totalResults?: number;
}

/**
 * Search web using configured provider
 */
export async function searchWeb(
  query: string,
  config: SearchConfig
): Promise<SearchResponse> {
  const provider = config.provider || (process.env.SEARCH_PROVIDER as SearchProvider) || 'brave';

  switch (provider) {
    case 'brave':
      return searchWithBrave(query, config);
    case 'serper':
      return searchWithSerper(query, config);
    case 'google':
      return searchWithGoogle(query, config);
    case 'bing':
      return searchWithBing(query, config);
    default:
      throw new Error(`Unsupported search provider: ${provider}`);
  }
}

/**
 * Brave Search Implementation
 */
async function searchWithBrave(
  query: string,
  config: SearchConfig
): Promise<SearchResponse> {
  const apiKey = process.env.BRAVE_SEARCH_API_KEY;
  if (!apiKey) {
    throw new Error('BRAVE_SEARCH_API_KEY not configured');
  }

  const params = new URLSearchParams({
    q: query,
    count: (config.maxResults || 10).toString(),
  });

  if (config.freshness) {
    params.set('freshness', config.freshness);
  }

  const response = await fetch(
    `https://api.search.brave.com/res/v1/web/search?${params}`,
    {
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': apiKey,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Brave Search API error: ${response.statusText}`);
  }

  const data = await response.json();

  return {
    results: (data.web?.results || []).map((result: any) => ({
      title: result.title,
      url: result.url,
      snippet: result.description,
      publishedDate: result.age,
    })),
    totalResults: data.query?.total,
  };
}

/**
 * Serper.dev Implementation
 */
async function searchWithSerper(
  query: string,
  config: SearchConfig
): Promise<SearchResponse> {
  const apiKey = process.env.SERPER_API_KEY;
  if (!apiKey) {
    throw new Error('SERPER_API_KEY not configured');
  }

  const response = await fetch('https://google.serper.dev/search', {
    method: 'POST',
    headers: {
      'X-API-KEY': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      q: query,
      num: config.maxResults || 10,
    }),
  });

  if (!response.ok) {
    throw new Error(`Serper API error: ${response.statusText}`);
  }

  const data = await response.json();

  return {
    results: (data.organic || []).map((result: any) => ({
      title: result.title,
      url: result.link,
      snippet: result.snippet,
      publishedDate: result.date,
    })),
    totalResults: data.searchInformation?.totalResults,
  };
}

/**
 * Google Custom Search Implementation
 */
async function searchWithGoogle(
  query: string,
  config: SearchConfig
): Promise<SearchResponse> {
  const apiKey = process.env.GOOGLE_SEARCH_API_KEY;
  const engineId = process.env.GOOGLE_SEARCH_ENGINE_ID;

  if (!apiKey || !engineId) {
    throw new Error('GOOGLE_SEARCH_API_KEY or GOOGLE_SEARCH_ENGINE_ID not configured');
  }

  const params = new URLSearchParams({
    key: apiKey,
    cx: engineId,
    q: query,
    num: (config.maxResults || 10).toString(),
  });

  if (config.freshness) {
    const dateRestrict: Record<string, string> = {
      day: 'd1',
      week: 'w1',
      month: 'm1',
      year: 'y1',
    };
    params.set('dateRestrict', dateRestrict[config.freshness]);
  }

  const response = await fetch(
    `https://www.googleapis.com/customsearch/v1?${params}`
  );

  if (!response.ok) {
    throw new Error(`Google Custom Search API error: ${response.statusText}`);
  }

  const data = await response.json();

  return {
    results: (data.items || []).map((result: any) => ({
      title: result.title,
      url: result.link,
      snippet: result.snippet,
    })),
    totalResults: parseInt(data.searchInformation?.totalResults || '0'),
  };
}

/**
 * Bing Search Implementation
 */
async function searchWithBing(
  query: string,
  config: SearchConfig
): Promise<SearchResponse> {
  const apiKey = process.env.BING_SEARCH_API_KEY;
  if (!apiKey) {
    throw new Error('BING_SEARCH_API_KEY not configured');
  }

  const params = new URLSearchParams({
    q: query,
    count: (config.maxResults || 10).toString(),
  });

  if (config.freshness) {
    params.set('freshness', config.freshness);
  }

  const response = await fetch(
    `https://api.bing.microsoft.com/v7.0/search?${params}`,
    {
      headers: {
        'Ocp-Apim-Subscription-Key': apiKey,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Bing Search API error: ${response.statusText}`);
  }

  const data = await response.json();

  return {
    results: (data.webPages?.value || []).map((result: any) => ({
      title: result.name,
      url: result.url,
      snippet: result.snippet,
      publishedDate: result.dateLastCrawled,
    })),
    totalResults: data.webPages?.totalEstimatedMatches,
  };
}
