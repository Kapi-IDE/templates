/**
 * API Client for AI Governance Backend
 * Connects Next.js frontend to FastAPI backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_V1 = `${API_URL}/api/v1`;

// ----- Types -----

export interface AIModel {
  id: string;
  name: string;
  type: string;
  version: string;
  description?: string;
  bias_score?: number;
  risk_level?: string;
  compliance_status?: string;
  last_checked?: string;
  created_at?: string;
}

export interface DashboardStats {
  total_models: number;
  bias_checks_today: number;
  compliance_rate: number;
  high_risk_models: number;
  trends: {
    models_growth: number;
    bias_checks_growth: number;
    compliance_growth: number;
    risk_reduction: number;
  };
}

export interface BiasAnalysis {
  model_id: string;
  bias_score: number;
  fairness_metrics: {
    demographic_parity: number;
    equal_opportunity: number;
    predictive_parity: number;
  };
  group_comparisons: Array<{
    group: string;
    acceptance_rate: number;
    count: number;
  }>;
  recommendations: string[];
  timestamp: string;
}

export interface RiskAssessment {
  model_id: string;
  risk_level: string;
  risk_score: number;
  risk_factors: Array<{
    factor: string;
    score: number;
    severity: string;
    description: string;
  }>;
  mitigations: string[];
  timestamp: string;
}

export interface ComplianceCheck {
  model_id: string;
  compliance_status: string;
  compliance_rate: number;
  gaps: Array<{
    regulation: string;
    requirement: string;
    status: string;
    details: string;
  }>;
  recommendations: string[];
  timestamp: string;
}

// ----- API Client -----

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // ----- Dashboard Stats -----

  async getDashboardStats(): Promise<DashboardStats> {
    return this.request('/governance/stats');
  }

  // ----- Models -----

  async listModels(params?: {
    skip?: number;
    limit?: number;
    risk_level?: string;
    compliance_status?: string;
  }): Promise<AIModel[]> {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.risk_level) queryParams.append('risk_level', params.risk_level);
    if (params?.compliance_status) queryParams.append('compliance_status', params.compliance_status);

    const endpoint = `/governance/models${queryParams.toString() ? '?' + queryParams : ''}`;
    return this.request(endpoint);
  }

  async getModel(modelId: string): Promise<AIModel> {
    return this.request(`/governance/models/${modelId}`);
  }

  async registerModel(model: Partial<AIModel>): Promise<AIModel> {
    return this.request('/governance/models', {
      method: 'POST',
      body: JSON.stringify(model),
    });
  }

  // ----- Bias Detection -----

  async analyzeBias(
    modelId: string,
    protectedAttributes?: string[]
  ): Promise<BiasAnalysis> {
    return this.request('/governance/bias/analyze', {
      method: 'POST',
      body: JSON.stringify({
        model_id: modelId,
        protected_attributes: protectedAttributes || ['gender', 'race', 'age'],
      }),
    });
  }

  // ----- Risk Assessment -----

  async assessRisk(modelId: string): Promise<RiskAssessment> {
    return this.request('/governance/risk/assess', {
      method: 'POST',
      body: JSON.stringify({ model_id: modelId }),
    });
  }

  // ----- Compliance -----

  async checkCompliance(
    modelId: string,
    regulations?: string[]
  ): Promise<ComplianceCheck> {
    return this.request('/governance/compliance/check', {
      method: 'POST',
      body: JSON.stringify({
        model_id: modelId,
        regulations: regulations || ['EU_AI_ACT', 'GDPR'],
      }),
    });
  }

  // ----- Analytics -----

  async getBiasTrend(): Promise<any> {
    return this.request('/governance/analytics/bias-trend');
  }

  async getRiskDistribution(): Promise<any> {
    return this.request('/governance/analytics/risk-distribution');
  }
}

// Export singleton instance
export const apiClient = new APIClient(API_V1);

// Export convenience functions
export const {
  getDashboardStats,
  listModels,
  getModel,
  registerModel,
  analyzeBias,
  assessRisk,
  checkCompliance,
  getBiasTrend,
  getRiskDistribution,
} = apiClient;
