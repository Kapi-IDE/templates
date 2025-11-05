# 🎨 React Dashboard Theme - Maxton Conversion

**Professional Bootstrap 5 Admin Dashboard converted to React Components**

Converted from: `/templates/temp/vertical-menu/` (Maxton Theme)

---

## 📦 Components Included

### Layout Components
- `DashboardLayout` - Main layout with sidebar and header
- `Sidebar` - Vertical navigation menu
- `Header` - Top navigation bar with search, notifications, profile
- `Footer` - Dashboard footer

### Navigation Components
- `NavMenu` - Metis menu navigation
- `Breadcrumb` - Page breadcrumbs
- `TopNav` - Horizontal navigation

### UI Components
- `Card` - Dashboard card wrapper
- `StatsCard` - Statistics display card
- `ChartCard` - Card with chart integration
- `DataTable` - Advanced data table
- `SearchBar` - Global search with dropdown
- `NotificationDropdown` - Notification bell with list
- `UserDropdown` - Profile dropdown menu
- `LanguageDropdown` - Language selector

### Widgets
- `SalesChart` - Sales/revenue charts
- `RecentOrders` - Order list widget
- `TopProducts` - Product performance widget
- `UserActivity` - Activity timeline
- `TaskList` - Todo/task widget

---

## 🚀 Quick Start

### Installation

```bash
npm install react react-dom bootstrap
npm install react-router-dom prop-types classnames
npm install chart.js react-chartjs-2  # For charts
npm install react-table  # For data tables
```

### Basic Usage

```jsx
import { DashboardLayout, Card, StatsCard } from './components/ui/react-dashboard-theme';

function App() {
  return (
    <DashboardLayout>
      <div className="row">
        <div className="col-md-3">
          <StatsCard
            title="Total Sales"
            value="$45,650"
            icon="shopping_cart"
            trend="up"
            percentage={12.5}
          />
        </div>
        <div className="col-md-3">
          <StatsCard
            title="Total Users"
            value="8,456"
            icon="people"
            trend="up"
            percentage={8.3}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
```

---

## 📁 File Structure

```
react-dashboard-theme/
├── components/
│   ├── layout/
│   │   ├── DashboardLayout.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   ├── navigation/
│   │   ├── NavMenu.jsx
│   │   ├── Breadcrumb.jsx
│   │   └── TopNav.jsx
│   ├── ui/
│   │   ├── Card.jsx
│   │   ├── StatsCard.jsx
│   │   ├── ChartCard.jsx
│   │   ├── DataTable.jsx
│   │   ├── SearchBar.jsx
│   │   ├── NotificationDropdown.jsx
│   │   ├── UserDropdown.jsx
│   │   └── LanguageDropdown.jsx
│   └── widgets/
│       ├── SalesChart.jsx
│       ├── RecentOrders.jsx
│       ├── TopProducts.jsx
│       ├── UserActivity.jsx
│       └── TaskList.jsx
├── layouts/
│   ├── AuthLayout.jsx
│   ├── FullLayout.jsx
│   └── MinimalLayout.jsx
├── assets/
│   ├── css/          # Bootstrap CSS (from original theme)
│   ├── js/           # JavaScript utilities
│   ├── images/       # Images and icons
│   └── plugins/      # Third-party plugins
├── hooks/
│   ├── useSidebar.js
│   ├── useTheme.js
│   └── useBreakpoint.js
├── utils/
│   ├── helpers.js
│   └── constants.js
├── README.md
└── package.json
```

---

## 🎨 Theme Features

### Color Themes
- Blue Theme (default)
- Dark Theme
- Light Theme
- Semi-dark Theme
- Bordered Theme

### Layout Options
- Vertical Sidebar (default)
- Horizontal Menu
- Boxed Layout
- Full Width

### Components
- 80+ HTML pages converted to React
- Material Icons integration
- Bootstrap 5 components
- Responsive design
- RTL support ready

---

## 📊 Converting HTML to React

### Example: Converting a Card

**Original HTML:**
```html
<div class="card rounded-4">
  <div class="card-body">
    <div class="d-flex align-items-center gap-3 mb-2">
      <div class="widget-icon rounded-circle">
        <i class="material-icons-outlined">shopping_cart</i>
      </div>
      <div class="flex-grow-1">
        <p class="mb-0 text-secondary">Total Sales</p>
        <h4 class="my-1">$45,650</h4>
      </div>
    </div>
    <div class="d-flex align-items-center gap-1">
      <span class="text-success me-1">
        <i class="material-icons-outlined">arrow_drop_up</i>
      </span>
      <p class="mb-0">12.5%</p>
    </div>
  </div>
</div>
```

**Converted React Component:**
```jsx
export function StatsCard({ title, value, icon, trend, percentage }) {
  return (
    <div className="card rounded-4">
      <div className="card-body">
        <div className="d-flex align-items-center gap-3 mb-2">
          <div className="widget-icon rounded-circle">
            <i className="material-icons-outlined">{icon}</i>
          </div>
          <div className="flex-grow-1">
            <p className="mb-0 text-secondary">{title}</p>
            <h4 className="my-1">{value}</h4>
          </div>
        </div>
        <div className="d-flex align-items-center gap-1">
          <span className={`text-${trend === 'up' ? 'success' : 'danger'} me-1`}>
            <i className="material-icons-outlined">
              {trend === 'up' ? 'arrow_drop_up' : 'arrow_drop_down'}
            </i>
          </span>
          <p className="mb-0">{percentage}%</p>
        </div>
      </div>
    </div>
  );
}
```

---

## 🔧 Available Components

### Core Layout Components

#### DashboardLayout
```jsx
<DashboardLayout
  theme="blue-theme"
  sidebarCollapsed={false}
  onSidebarToggle={() => {}}
>
  {children}
</DashboardLayout>
```

#### Sidebar
```jsx
<Sidebar
  collapsed={false}
  onToggle={() => {}}
  menuItems={menuConfig}
/>
```

#### Header
```jsx
<Header
  user={userData}
  notifications={[]}
  onSearch={(query) => {}}
/>
```

### UI Components

#### StatsCard
```jsx
<StatsCard
  title="Total Sales"
  value="$45,650"
  icon="shopping_cart"
  trend="up"
  percentage={12.5}
  color="primary"
/>
```

#### ChartCard
```jsx
<ChartCard
  title="Revenue Overview"
  subtitle="Monthly earnings"
  chartData={chartData}
  chartType="line"
/>
```

#### DataTable
```jsx
<DataTable
  columns={columns}
  data={data}
  pagination={true}
  searchable={true}
  sortable={true}
/>
```

---

## 🎯 Use Cases

### 1. Admin Dashboard
```jsx
import { DashboardLayout, StatsCard, ChartCard, DataTable } from './components';

function AdminDashboard() {
  return (
    <DashboardLayout>
      <div className="row row-cols-1 row-cols-lg-2 row-cols-xl-4">
        <StatsCard title="Users" value="8,456" icon="people" />
        <StatsCard title="Orders" value="1,245" icon="shopping_bag" />
        <StatsCard title="Revenue" value="$45,650" icon="payments" />
        <StatsCard title="Products" value="563" icon="inventory" />
      </div>

      <div className="row mt-4">
        <div className="col-md-8">
          <ChartCard title="Sales Overview" chartData={salesData} />
        </div>
        <div className="col-md-4">
          <RecentOrders orders={recentOrders} />
        </div>
      </div>
    </DashboardLayout>
  );
}
```

### 2. E-commerce Dashboard
```jsx
function EcommerceDashboard() {
  return (
    <DashboardLayout>
      <TopProducts products={topProducts} />
      <DataTable columns={orderColumns} data={orders} />
    </DashboardLayout>
  );
}
```

### 3. Analytics Dashboard
```jsx
function AnalyticsDashboard() {
  return (
    <DashboardLayout>
      <SalesChart data={salesData} />
      <UserActivity activities={activities} />
    </DashboardLayout>
  );
}
```

---

## 🎨 Theming

### Switch Theme
```jsx
import { useTheme } from './hooks/useTheme';

function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();

  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
      <option value="blue-theme">Blue</option>
      <option value="dark-theme">Dark</option>
      <option value="light-theme">Light</option>
      <option value="semi-dark">Semi Dark</option>
    </select>
  );
}
```

### Custom Colors
```css
/* Override theme colors */
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
  --success-color: #198754;
  --danger-color: #dc3545;
}
```

---

## 📱 Responsive Design

All components are fully responsive:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

```jsx
import { useBreakpoint } from './hooks/useBreakpoint';

function ResponsiveComponent() {
  const { isMobile, isTablet, isDesktop } = useBreakpoint();

  return (
    <div>
      {isMobile && <MobileView />}
      {isTablet && <TabletView />}
      {isDesktop && <DesktopView />}
    </div>
  );
}
```

---

## 🔌 Integration with Existing Apps

### With Next.js
```jsx
// pages/_app.js
import '../components/ui/react-dashboard-theme/assets/css/bootstrap.min.css';
import '../components/ui/react-dashboard-theme/assets/css/main.css';

function MyApp({ Component, pageProps }) {
  return (
    <DashboardLayout>
      <Component {...pageProps} />
    </DashboardLayout>
  );
}
```

### With Create React App
```jsx
// App.js
import './components/ui/react-dashboard-theme/assets/css/bootstrap.min.css';
import { DashboardLayout } from './components/ui/react-dashboard-theme';

function App() {
  return (
    <DashboardLayout>
      <YourContent />
    </DashboardLayout>
  );
}
```

### With AI Governance Platform
```jsx
// AI Governance Dashboard
import { DashboardLayout, StatsCard, DataTable } from './components/ui/react-dashboard-theme';

function AIGovernanceDashboard() {
  return (
    <DashboardLayout>
      <StatsCard title="Models Tracked" value="1,245" icon="model_training" />
      <StatsCard title="Bias Checks" value="345" icon="rule" />
      <StatsCard title="Compliance Rate" value="98%" icon="verified" />

      <DataTable
        title="AI Models"
        columns={modelColumns}
        data={models}
      />
    </DashboardLayout>
  );
}
```

---

## 📦 Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.0",
    "bootstrap": "^5.3.0",
    "prop-types": "^15.8.1",
    "classnames": "^2.3.2",
    "chart.js": "^4.3.0",
    "react-chartjs-2": "^5.2.0",
    "react-table": "^7.8.0"
  }
}
```

---

## 🛠️ Customization

### Add New Menu Item
```jsx
const menuItems = [
  {
    title: 'Dashboard',
    icon: 'dashboard',
    path: '/',
  },
  {
    title: 'AI Models',
    icon: 'model_training',
    path: '/models',
    badge: { text: 'New', variant: 'success' }
  },
  {
    title: 'Settings',
    icon: 'settings',
    submenu: [
      { title: 'Profile', path: '/settings/profile' },
      { title: 'Security', path: '/settings/security' }
    ]
  }
];
```

### Create Custom Widget
```jsx
export function CustomWidget({ data }) {
  return (
    <div className="card">
      <div className="card-header">
        <h5 className="card-title">Your Custom Widget</h5>
      </div>
      <div className="card-body">
        {/* Your custom content */}
      </div>
    </div>
  );
}
```

---

## 🚀 Performance

- **Lazy Loading**: Components loaded on demand
- **Code Splitting**: Automatic with React.lazy()
- **Optimized Assets**: Minified CSS/JS
- **Tree Shaking**: Unused code eliminated

```jsx
// Lazy load dashboard
const Dashboard = React.lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

---

## 📝 License

MIT License - Free to use in commercial and personal projects

---

## 🔗 Original Theme

**Maxton** - Bootstrap 5 Admin Dashboard Template
- 80+ HTML pages
- Material Icons
- Bootstrap 5.3
- Responsive design
- Multiple color themes

---

**Converted to React by KAPI Components Team** 🎨
**Production-ready dashboard components for modern web apps** 🚀
