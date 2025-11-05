# 📊 Enterprise Analytics Dashboard

**Real-time KPI dashboard with role-based access and drill-down reports**

Built with KAPI blueprints - Production-ready analytics in 35 minutes.

---

## 🎯 Features

### Core Analytics
- **Real-time KPIs**: Revenue, users, performance metrics
- **Interactive Charts**: Recharts with line, bar, area visualizations
- **Drill-down Reports**: Click KPIs to view detailed breakdowns
- **Date Range Filtering**: Custom periods, presets (7d, 30d, 90d)
- **Export Functionality**: CSV, PDF, Excel formats

### Role-Based Access Control
- **ADMIN**: Full access + user management
- **MANAGER**: View + export all data
- **ANALYST**: View + drill-down reports
- **VIEWER**: Read-only dashboard access

### Data Management
- **PostgreSQL**: Production database with Prisma ORM
- **Real-time Updates**: Server-sent events for live data
- **Activity Logging**: Track user actions (view, export, filter)
- **Data Aggregation**: Automatic daily/weekly/monthly rollups

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- PostgreSQL 14+

### Installation

```bash
# Install dependencies
npm install

# Setup database
cp .env.example .env
# Edit .env with your DATABASE_URL

# Initialize database
npx prisma db push
npx prisma db seed

# Start development
npm run dev
```

Visit **http://localhost:3000**

**Default Login:**
- Admin: `admin@company.com` / `admin123`
- Manager: `manager@company.com` / `manager123`
- Analyst: `analyst@company.com` / `analyst123`
- Viewer: `viewer@company.com` / `viewer123`

---

## 📊 Dashboard Components

### KPI Cards (Adapted from react-dashboard-theme)
```typescript
<KPICard
  title="Total Revenue"
  value="$1.2M"
  icon={DollarSign}
  trend="up"
  percentage={12.5}
  color="green"
  subtitle="vs last month"
  onClick={() => drillDown('revenue')}
/>
```

**Features:**
- Trend indicators (up/down/neutral)
- Click-through for drill-down
- Color coding by metric type
- Percentage change display

### Revenue Chart (Adapted from ChartCard)
```typescript
<RevenueChart
  title="Monthly Revenue"
  data={monthlyData}
  chartType="area"
  dataKeys={['revenue', 'profit']}
  colors={['#3b82f6', '#10b981']}
  onExport={exportCSV}
  onFilter={openFilterModal}
/>
```

**Chart Types:**
- Line: Trends over time
- Bar: Comparisons
- Area: Volume visualization

### Data Table (Adapted from DataTable)
```typescript
<DataTable
  title="Top Customers"
  columns={[
    { key: 'name', label: 'Name' },
    { key: 'revenue', label: 'Revenue', render: formatCurrency },
    { key: 'orders', label: 'Orders' },
  ]}
  data={customers}
  searchable
  sortable
  pagination
  pageSize={20}
  onExport={exportToCSV}
/>
```

**Features:**
- Search across all columns
- Sort by any column
- Pagination with page size options
- CSV/PDF export

---

## 🗄️ Database Schema

### Users & Authentication
```prisma
model User {
  id       String @id @default(cuid())
  email    String @unique
  password String
  name     String
  role     Role   @default(VIEWER)

  sessions     Session[]
  activityLogs ActivityLog[]
}

enum Role {
  ADMIN
  MANAGER
  ANALYST
  VIEWER
}
```

### Analytics Data
```prisma
model SalesMetric {
  date          DateTime
  revenue       Float
  orders        Int
  customers     Int
  avgOrderValue Float
  region        String
  category      String
}

model UserMetric {
  date            DateTime
  activeUsers     Int
  newUsers        Int
  sessionDuration Float
  pageViews       Int
  bounceRate      Float
}
```

---

## 🔐 Role-Based Access

### Permission Matrix

| Feature | ADMIN | MANAGER | ANALYST | VIEWER |
|---------|-------|---------|---------|--------|
| View Dashboard | ✅ | ✅ | ✅ | ✅ |
| Drill-down Reports | ✅ | ✅ | ✅ | ❌ |
| Export Data | ✅ | ✅ | ❌ | ❌ |
| User Management | ✅ | ❌ | ❌ | ❌ |
| Edit Settings | ✅ | ❌ | ❌ | ❌ |

### Implementation

```typescript
// Middleware: app/api/middleware.ts
export function requireRole(roles: Role[]) {
  return (req, res, next) => {
    const user = req.user;
    if (!roles.includes(user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Usage in API route
export async function GET(req) {
  const user = await getCurrentUser(req);
  if (!['ADMIN', 'MANAGER'].includes(user.role)) {
    return Response.json({ error: 'Forbidden' }, { status: 403 });
  }
  // ...
}
```

---

## 📈 Export Functionality

### CSV Export
```typescript
import { ExportToCsv } from 'export-to-csv';

function exportToCSV(data: any[], filename: string) {
  const csvExporter = new ExportToCsv({
    fieldSeparator: ',',
    quoteStrings: '"',
    decimalSeparator: '.',
    showLabels: true,
    filename,
    useTextFile: false,
    useBom: true,
  });

  csvExporter.generateCsv(data);
}
```

### PDF Export
```typescript
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

function exportToPDF(data: any[], columns: any[], title: string) {
  const doc = new jsPDF();

  doc.text(title, 14, 15);

  autoTable(doc, {
    head: [columns.map(c => c.label)],
    body: data.map(row => columns.map(c => row[c.key])),
    startY: 20,
  });

  doc.save(`${title}-${new Date().toISOString()}.pdf`);
}
```

---

## 🔍 Drill-Down Reports

### Click Flow
1. User clicks KPI card (e.g., "Total Revenue")
2. Modal opens with detailed breakdown
3. Filter by region, category, date range
4. View chart + data table
5. Export filtered results

### Implementation
```typescript
function KPIDashboard() {
  const [drillDownData, setDrillDownData] = useState(null);

  async function handleDrillDown(metric: string, filters: any) {
    const data = await fetch(`/api/drill-down/${metric}`, {
      method: 'POST',
      body: JSON.stringify(filters),
    }).then(r => r.json());

    setDrillDownData(data);
    openModal();
  }

  return (
    <>
      <KPICard onClick={() => handleDrillDown('revenue', {})} />
      {drillDownData && (
        <DrillDownModal data={drillDownData} onClose={closeModal} />
      )}
    </>
  );
}
```

---

## 🏗️ Project Structure

```
enterprise-analytics-dashboard/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── page.tsx              # Main dashboard
│   │   ├── reports/page.tsx      # Drill-down reports
│   │   └── settings/page.tsx     # User settings
│   ├── api/
│   │   ├── auth/route.ts
│   │   ├── metrics/route.ts
│   │   ├── drill-down/[metric]/route.ts
│   │   └── export/route.ts
│   └── layout.tsx
├── components/
│   ├── KPICard.tsx               # Adapted from StatsCard
│   ├── RevenueChart.tsx          # Adapted from ChartCard
│   ├── DataTable.tsx             # Adapted from DataTable
│   ├── DrillDownModal.tsx
│   ├── FilterPanel.tsx
│   └── ExportButton.tsx
├── lib/
│   ├── auth.ts                   # Authentication helpers
│   ├── permissions.ts            # RBAC logic
│   └── export.ts                 # CSV/PDF export
├── prisma/
│   ├── schema.prisma
│   └── seed.ts
└── package.json
```

---

## 📊 Sample Data & Seed

```typescript
// prisma/seed.ts
const salesData = Array.from({ length: 90 }, (_, i) => ({
  date: subDays(new Date(), i),
  revenue: 50000 + Math.random() * 50000,
  orders: 100 + Math.floor(Math.random() * 200),
  customers: 80 + Math.floor(Math.random() * 150),
  avgOrderValue: 400 + Math.random() * 200,
  region: ['North', 'South', 'East', 'West'][Math.floor(Math.random() * 4)],
  category: ['Electronics', 'Clothing', 'Food', 'Books'][Math.floor(Math.random() * 4)],
}));

await prisma.salesMetric.createMany({ data: salesData });
```

---

## 🎨 Customization

### Add New KPI
```typescript
// 1. Add to database
model CustomMetric {
  id    String @id
  date  DateTime
  value Float
  type  String
}

// 2. Create API route
// app/api/metrics/custom/route.ts
export async function GET() {
  const data = await prisma.customMetric.findMany();
  return Response.json(data);
}

// 3. Add KPI card
<KPICard
  title="Custom Metric"
  value={customValue}
  icon={Star}
/>
```

### Change Chart Colors
```typescript
// In RevenueChart component
colors={['#your-color-1', '#your-color-2']}
```

### Adjust Role Permissions
```typescript
// In lib/permissions.ts
export const PERMISSIONS = {
  VIEW_DASHBOARD: ['ADMIN', 'MANAGER', 'ANALYST', 'VIEWER'],
  EXPORT_DATA: ['ADMIN', 'MANAGER'],
  DRILL_DOWN: ['ADMIN', 'MANAGER', 'ANALYST'],
  MANAGE_USERS: ['ADMIN'],
};
```

---

## 🚀 Deployment

### Environment Variables
```env
DATABASE_URL="postgresql://user:password@localhost:5432/analytics"
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="https://your-domain.com"
```

### Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add Vercel Postgres
# Set DATABASE_URL in environment variables
```

### Docker
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npx prisma generate
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📚 Component Credits

This dashboard adapts components from:
- `components/ui/react-dashboard-theme/StatsCard.jsx` → `KPICard.tsx`
- `components/ui/react-dashboard-theme/ChartCard.jsx` → `RevenueChart.tsx`
- `components/ui/react-dashboard-theme/DataTable.jsx` → `DataTable.tsx`

**Enhancements:**
- TypeScript conversion
- Recharts integration (replacing Chart.js)
- Tailwind CSS (replacing Bootstrap)
- Lucide icons (replacing Material Icons)
- Next.js 14 App Router
- Role-based access control
- Export functionality

---

## 📄 License

MIT

---

**Built with KAPI** - Enterprise-ready in 35 minutes
