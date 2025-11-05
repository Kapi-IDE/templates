import React from 'react';
import {
  DashboardLayout,
  StatsCard,
  ChartCard,
  DataTable
} from '../index';

/**
 * AI Governance Dashboard - Complete Example
 */
export function AIGovernanceDashboard() {
  // Sample data for charts
  const biasChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Bias Score',
        data: [0.65, 0.59, 0.52, 0.48, 0.45, 0.42],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4
      }
    ]
  };

  const riskDistribution = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical'],
    datasets: [
      {
        data: [65, 25, 8, 2],
        backgroundColor: [
          'rgba(75, 192, 192, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(255, 99, 132, 0.8)',
        ],
      }
    ]
  };

  // AI Models table data
  const modelColumns = [
    {
      key: 'id',
      label: 'Model ID',
      render: (value) => <span className="badge bg-light text-dark">{value}</span>
    },
    { key: 'name', label: 'Model Name' },
    {
      key: 'type',
      label: 'Type',
      render: (value) => <span className="badge bg-info">{value}</span>
    },
    {
      key: 'biasScore',
      label: 'Bias Score',
      render: (value) => {
        const color = value < 0.3 ? 'success' : value < 0.6 ? 'warning' : 'danger';
        return <span className={`badge bg-${color}`}>{value}</span>;
      }
    },
    {
      key: 'riskLevel',
      label: 'Risk Level',
      render: (value) => {
        const color = value === 'Low' ? 'success' :
                      value === 'Medium' ? 'warning' : 'danger';
        return <span className={`badge bg-${color}`}>{value}</span>;
      }
    },
    {
      key: 'compliance',
      label: 'Compliance',
      render: (value) => (
        <span className={`badge bg-${value === 'Compliant' ? 'success' : 'danger'}`}>
          {value}
        </span>
      )
    },
    { key: 'lastChecked', label: 'Last Checked' }
  ];

  const modelsData = [
    {
      id: 'MDL-001',
      name: 'Credit Scoring Model',
      type: 'Classification',
      biasScore: 0.42,
      riskLevel: 'Low',
      compliance: 'Compliant',
      lastChecked: '2024-10-01'
    },
    {
      id: 'MDL-002',
      name: 'Fraud Detection',
      type: 'Anomaly Detection',
      biasScore: 0.58,
      riskLevel: 'Medium',
      compliance: 'Compliant',
      lastChecked: '2024-10-01'
    },
    {
      id: 'MDL-003',
      name: 'Loan Approval',
      type: 'Classification',
      biasScore: 0.73,
      riskLevel: 'High',
      compliance: 'Non-Compliant',
      lastChecked: '2024-09-30'
    },
    {
      id: 'MDL-004',
      name: 'Customer Churn',
      type: 'Prediction',
      biasScore: 0.35,
      riskLevel: 'Low',
      compliance: 'Compliant',
      lastChecked: '2024-10-02'
    },
    {
      id: 'MDL-005',
      name: 'Product Recommendation',
      type: 'Recommendation',
      biasScore: 0.48,
      riskLevel: 'Medium',
      compliance: 'Compliant',
      lastChecked: '2024-10-01'
    }
  ];

  const menuItems = [
    {
      title: 'Dashboard',
      icon: 'dashboard',
      path: '/',
    },
    {
      title: 'AI Models',
      icon: 'model_training',
      submenu: [
        { title: 'All Models', path: '/models' },
        { title: 'Register Model', path: '/models/register' },
        { title: 'Performance', path: '/models/performance' }
      ]
    },
    {
      title: 'Governance',
      icon: 'verified_user',
      submenu: [
        { title: 'Bias Detection', path: '/governance/bias' },
        { title: 'Risk Assessment', path: '/governance/risk' },
        { title: 'Compliance Check', path: '/governance/compliance' },
        { title: 'Audit Trail', path: '/governance/audit' }
      ]
    },
    {
      title: 'Analytics',
      icon: 'analytics',
      path: '/analytics'
    },
    {
      title: 'Reports',
      icon: 'assessment',
      path: '/reports'
    },
    {
      title: 'Settings',
      icon: 'settings',
      path: '/settings'
    }
  ];

  const notifications = [
    {
      id: 1,
      title: 'High bias detected in MDL-003',
      message: 'Loan Approval model shows bias score of 0.73',
      time: '5 min ago',
      type: 'warning'
    },
    {
      id: 2,
      title: 'Compliance check completed',
      message: '15 models passed compliance verification',
      time: '1 hour ago',
      type: 'success'
    },
    {
      id: 3,
      title: 'New model registered',
      message: 'Customer Churn model added to registry',
      time: '2 hours ago',
      type: 'info'
    }
  ];

  const user = {
    name: 'AI Governance Admin',
    email: 'admin@aigovernance.com',
    avatar: '/assets/images/avatars/01.png'
  };

  const tableActions = (row) => (
    <>
      <button className="btn btn-sm btn-primary">
        <i className="material-icons-outlined">visibility</i>
      </button>
      <button className="btn btn-sm btn-warning">
        <i className="material-icons-outlined">analytics</i>
      </button>
      <button className="btn btn-sm btn-info">
        <i className="material-icons-outlined">edit</i>
      </button>
    </>
  );

  return (
    <DashboardLayout
      theme="blue-theme"
      menuItems={menuItems}
      user={user}
      notifications={notifications}
    >
      {/* Page Title */}
      <div className="row mb-4">
        <div className="col">
          <h4 className="mb-0">AI Governance Dashboard</h4>
          <p className="mb-0 text-muted">Monitor and manage AI models compliance and fairness</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-3 mb-4">
        <StatsCard
          title="Total Models"
          value="1,245"
          icon="model_training"
          trend="up"
          percentage={12.5}
          color="primary"
          subtitle="Active models in registry"
        />
        <StatsCard
          title="Bias Checks Today"
          value="345"
          icon="verified"
          trend="up"
          percentage={8.3}
          color="success"
          subtitle="Automated bias scans"
        />
        <StatsCard
          title="Compliance Rate"
          value="94%"
          icon="check_circle"
          trend="up"
          percentage={2.1}
          color="info"
          subtitle="Models meeting standards"
        />
        <StatsCard
          title="High Risk Models"
          value="23"
          icon="warning"
          trend="down"
          percentage={-15.2}
          color="danger"
          subtitle="Requiring immediate attention"
        />
      </div>

      {/* Charts Row */}
      <div className="row g-3 mb-4">
        <div className="col-lg-8">
          <ChartCard
            title="Bias Trend Analysis"
            subtitle="Average bias score over time"
            chartType="line"
            chartData={biasChartData}
            height={350}
          />
        </div>
        <div className="col-lg-4">
          <ChartCard
            title="Risk Distribution"
            subtitle="Models by risk category"
            chartType="doughnut"
            chartData={riskDistribution}
            height={350}
          />
        </div>
      </div>

      {/* Data Table */}
      <div className="row">
        <div className="col-12">
          <DataTable
            title="AI Models Registry"
            columns={modelColumns}
            data={modelsData}
            searchable
            sortable
            pagination
            pageSize={5}
            actions={tableActions}
          />
        </div>
      </div>

      {/* Recent Activity */}
      <div className="row mt-4">
        <div className="col-lg-6">
          <div className="card">
            <div className="card-header bg-transparent">
              <h5 className="mb-0">Recent Compliance Checks</h5>
            </div>
            <div className="card-body">
              <div className="timeline">
                <div className="timeline-item">
                  <div className="timeline-marker bg-success"></div>
                  <div className="timeline-content">
                    <h6>Credit Scoring Model - Passed</h6>
                    <p className="mb-0 text-muted small">Compliance check completed successfully</p>
                    <span className="text-muted small">2 hours ago</span>
                  </div>
                </div>
                <div className="timeline-item">
                  <div className="timeline-marker bg-warning"></div>
                  <div className="timeline-content">
                    <h6>Loan Approval - Warning</h6>
                    <p className="mb-0 text-muted small">High bias detected, review required</p>
                    <span className="text-muted small">4 hours ago</span>
                  </div>
                </div>
                <div className="timeline-item">
                  <div className="timeline-marker bg-info"></div>
                  <div className="timeline-content">
                    <h6>Fraud Detection - Updated</h6>
                    <p className="mb-0 text-muted small">Model retrained with new data</p>
                    <span className="text-muted small">6 hours ago</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-6">
          <div className="card">
            <div className="card-header bg-transparent">
              <h5 className="mb-0">Recommended Actions</h5>
            </div>
            <div className="card-body">
              <div className="d-flex flex-column gap-3">
                <div className="alert alert-danger border-0 mb-0">
                  <div className="d-flex align-items-center gap-2">
                    <i className="material-icons-outlined">error</i>
                    <div className="flex-grow-1">
                      <strong>Critical:</strong> MDL-003 requires immediate bias mitigation
                    </div>
                    <button className="btn btn-sm btn-danger">Review</button>
                  </div>
                </div>
                <div className="alert alert-warning border-0 mb-0">
                  <div className="d-flex align-items-center gap-2">
                    <i className="material-icons-outlined">warning</i>
                    <div className="flex-grow-1">
                      <strong>Warning:</strong> 5 models pending compliance verification
                    </div>
                    <button className="btn btn-sm btn-warning">Check</button>
                  </div>
                </div>
                <div className="alert alert-info border-0 mb-0">
                  <div className="d-flex align-items-center gap-2">
                    <i className="material-icons-outlined">info</i>
                    <div className="flex-grow-1">
                      <strong>Info:</strong> EU AI Act compliance deadline in 30 days
                    </div>
                    <button className="btn btn-sm btn-info">Prepare</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default AIGovernanceDashboard;
