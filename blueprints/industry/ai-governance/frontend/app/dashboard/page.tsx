'use client';

import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import {
  getDashboardStats,
  listModels,
  getBiasTrend,
  getRiskDistribution,
  analyzeBias,
  assessRisk,
  type AIModel,
  type DashboardStats as Stats,
} from '@/lib/api';

// Dynamically import dashboard components (client-side only)
const DashboardLayout = dynamic(
  () => import('@/components/react-dashboard-theme/components/layout/DashboardLayout').then(mod => mod.DashboardLayout),
  { ssr: false }
);

const StatsCard = dynamic(
  () => import('@/components/react-dashboard-theme/components/ui/StatsCard').then(mod => mod.StatsCard),
  { ssr: false }
);

const ChartCard = dynamic(
  () => import('@/components/react-dashboard-theme/components/ui/ChartCard').then(mod => mod.ChartCard),
  { ssr: false }
);

const DataTable = dynamic(
  () => import('@/components/react-dashboard-theme/components/ui/DataTable').then(mod => mod.DataTable),
  { ssr: false }
);

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [models, setModels] = useState<AIModel[]>([]);
  const [biasChartData, setBiasChartData] = useState<any>(null);
  const [riskChartData, setRiskChartData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch dashboard data
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);

        // Fetch all data in parallel
        const [statsData, modelsData, biasData, riskData] = await Promise.all([
          getDashboardStats(),
          listModels({ limit: 10 }),
          getBiasTrend(),
          getRiskDistribution(),
        ]);

        setStats(statsData);
        setModels(modelsData);
        setBiasChartData(biasData);
        setRiskChartData(riskData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Make sure the backend is running on http://localhost:8000');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // Table columns configuration
  const modelColumns = [
    {
      key: 'id',
      label: 'Model ID',
      render: (value: string) => (
        <span className="badge bg-light text-dark">{value}</span>
      ),
    },
    { key: 'name', label: 'Model Name' },
    {
      key: 'type',
      label: 'Type',
      render: (value: string) => (
        <span className="badge bg-info">{value}</span>
      ),
    },
    {
      key: 'bias_score',
      label: 'Bias Score',
      render: (value: number) => {
        const color = value < 0.3 ? 'success' : value < 0.6 ? 'warning' : 'danger';
        return <span className={`badge bg-${color}`}>{value?.toFixed(2)}</span>;
      },
    },
    {
      key: 'risk_level',
      label: 'Risk Level',
      render: (value: string) => {
        const color = value === 'Low' ? 'success' :
                      value === 'Medium' ? 'warning' : 'danger';
        return <span className={`badge bg-${color}`}>{value}</span>;
      },
    },
    {
      key: 'compliance_status',
      label: 'Compliance',
      render: (value: string) => (
        <span className={`badge bg-${value === 'Compliant' ? 'success' : 'danger'}`}>
          {value}
        </span>
      ),
    },
    { key: 'last_checked', label: 'Last Checked' },
  ];

  const tableActions = (row: AIModel) => (
    <>
      <button className="btn btn-sm btn-primary" title="View Details">
        <i className="material-icons-outlined">visibility</i>
      </button>
      <button
        className="btn btn-sm btn-warning"
        title="Analyze Bias"
        onClick={async () => {
          try {
            const result = await analyzeBias(row.id);
            alert(`Bias Score: ${result.bias_score}\nRecommendations: ${result.recommendations[0]}`);
          } catch (err) {
            alert('Failed to analyze bias');
          }
        }}
      >
        <i className="material-icons-outlined">analytics</i>
      </button>
      <button
        className="btn btn-sm btn-info"
        title="Assess Risk"
        onClick={async () => {
          try {
            const result = await assessRisk(row.id);
            alert(`Risk Level: ${result.risk_level}\nRisk Score: ${result.risk_score}`);
          } catch (err) {
            alert('Failed to assess risk');
          }
        }}
      >
        <i className="material-icons-outlined">warning</i>
      </button>
    </>
  );

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger m-4" role="alert">
        <h4 className="alert-heading">Error Loading Dashboard</h4>
        <p>{error}</p>
        <hr />
        <p className="mb-0">
          <strong>Quick Fix:</strong> Run <code>cd backend && uvicorn app.main:app --reload</code>
        </p>
      </div>
    );
  }

  return (
    <DashboardLayout theme="blue-theme">
      {/* Page Title */}
      <div className="row mb-4">
        <div className="col">
          <h4 className="mb-0">AI Governance Dashboard</h4>
          <p className="mb-0 text-muted">
            Monitor and manage AI models compliance and fairness
          </p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-3 mb-4">
        <StatsCard
          title="Total Models"
          value={stats?.total_models.toString() || '0'}
          icon="model_training"
          trend="up"
          percentage={stats?.trends.models_growth || 0}
          color="primary"
          subtitle="Active models in registry"
        />
        <StatsCard
          title="Bias Checks Today"
          value={stats?.bias_checks_today.toString() || '0'}
          icon="verified"
          trend="up"
          percentage={stats?.trends.bias_checks_growth || 0}
          color="success"
          subtitle="Automated bias scans"
        />
        <StatsCard
          title="Compliance Rate"
          value={`${stats?.compliance_rate.toFixed(1)}%` || '0%'}
          icon="check_circle"
          trend="up"
          percentage={stats?.trends.compliance_growth || 0}
          color="info"
          subtitle="Models meeting standards"
        />
        <StatsCard
          title="High Risk Models"
          value={stats?.high_risk_models.toString() || '0'}
          icon="warning"
          trend="down"
          percentage={Math.abs(stats?.trends.risk_reduction || 0)}
          color="danger"
          subtitle="Requiring immediate attention"
        />
      </div>

      {/* Charts Row */}
      <div className="row g-3 mb-4">
        <div className="col-lg-8">
          {biasChartData && (
            <ChartCard
              title="Bias Trend Analysis"
              subtitle="Average bias score over time"
              chartType="line"
              chartData={biasChartData}
              height={350}
            />
          )}
        </div>
        <div className="col-lg-4">
          {riskChartData && (
            <ChartCard
              title="Risk Distribution"
              subtitle="Models by risk category"
              chartType="doughnut"
              chartData={riskChartData}
              height={350}
            />
          )}
        </div>
      </div>

      {/* Data Table */}
      <div className="row">
        <div className="col-12">
          <DataTable
            title="AI Models Registry"
            columns={modelColumns}
            data={models}
            searchable
            sortable
            pagination
            pageSize={5}
            actions={tableActions}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
