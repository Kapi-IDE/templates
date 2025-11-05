# Team Knowledge Base - UI Mockups

**ASCII-based interface specifications for token-efficient development guidance**

## Main Search Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 {{COMPANY_NAME}} Knowledge Base                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔍 Search: "How do I deploy to production?"                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🎯 Top Results (0.2s):                                 │   │
│  │                                                         │   │
│  │ 📄 Production Deployment Guide (DevOps/deploy.md)      │   │
│  │ "Step-by-step production deployment process..."        │   │
│  │ 📅 Updated 3 days ago • ⭐ 94% helpful                 │   │
│  │                                                         │   │
│  │ 💬 Slack: John (DevOps) - "New deployment script"     │   │
│  │ "Just updated the deployment automation, see #devops"  │   │
│  │ 📅 2 hours ago • 💬 #devops                           │   │
│  │                                                         │   │
│  │ 🎥 Recording: "Deployment Best Practices"             │   │
│  │ Team meeting from last week covering new procedures    │   │
│  │ 📅 1 week ago • ⏱️ 23:45 duration                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📊 Usage Today: 47 searches • 💡 12 new docs indexed          │
│  🎯 Top Topics: deployment(12), API(8), testing(6)             │
│                                                                 │
│  [🔍 Advanced Search] [📝 Add Document] [⚙️ Admin Panel]       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Advanced Search & Filters

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Advanced Knowledge Search                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Query: "authentication microservices"                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📅 Time Range: [Last 6 months ▼]                       │   │
│  │ 👥 Author: [Any team member ▼]                         │   │
│  │ 📁 Source: [☑️ Slack] [☑️ Docs] [☐ Code] [☑️ Meetings]   │   │
│  │ 🏷️ Tags: [backend] [security] [microservices]          │   │
│  │ ⭐ Min Rating: [4+ stars ▼]                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📊 Results (23 found):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🏆 Best Match (96% relevance):                         │   │
│  │ 📄 "Auth Service Design Document"                      │   │
│  │ Covers JWT, OAuth2, service-to-service auth            │   │
│  │ 👤 Sarah Chen • 📅 2 weeks ago • ⭐⭐⭐⭐⭐               │   │
│  │                                                         │   │
│  │ 💬 Related Discussion:                                  │   │
│  │ "#backend-auth: Token validation performance"           │   │
│  │ 15 messages • 👥 4 participants • 📅 Last week        │   │
│  │                                                         │   │
│  │ 💻 Code Examples:                                       │   │
│  │ "auth-service/middleware/jwt-validator.js"             │   │
│  │ Implementation with rate limiting and caching          │   │
│  │ 👤 Mike Torres • 📅 5 days ago                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [💾 Save Search] [🔔 Set Alert] [📤 Share Results]            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Document View with Context

```
┌─────────────────────────────────────────────────────────────────┐
│  📄 Production Deployment Guide                               │
├─────────────────────────────────────────────────────────────────┤
│  👤 Sarah Chen • 📅 Updated 3 days ago • ⭐ 4.8/5 (23 votes)  │
│  🏷️ [devops] [production] [deployment] [docker]               │
│                                                                 │
│  📋 Table of Contents:                                         │
│  ├─ 1. Prerequisites and Setup                                │
│  ├─ 2. Build and Test Pipeline                                │
│  ├─ 3. Production Environment Config                          │
│  ├─ 4. Deployment Process                                     │
│  └─ 5. Monitoring and Rollback                                │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│                                                                 │
│  ## 4. Deployment Process                                      │
│                                                                 │
│  Our deployment uses Docker containers with blue-green        │
│  strategy to ensure zero downtime:                             │
│                                                                 │
│  ```bash                                                       │
│  # Build and tag container                                     │
│  docker build -t app:v1.2.3 .                                 │
│                                                                 │
│  # Deploy to staging first                                     │
│  kubectl apply -f k8s/staging/ --namespace=staging            │
│  ```                                                           │
│                                                                 │
│  🔗 Related Resources:                                         │
│  ├─ 💬 "#devops: Deployment automation discussion"            │
│  ├─ 🎥 "Docker Best Practices" (team meeting, 23:45)          │
│  ├─ 📄 "Kubernetes Configuration Guide"                       │
│  └─ 💻 deployment-scripts/ (GitHub repo)                      │
│                                                                 │
│  💬 Recent Comments (3):                                       │
│  ├─ Mike: "Added health check validation step" (2 days ago)   │
│  ├─ Lisa: "Works great! Deployed 3 services" (1 day ago)      │
│  └─ John: "Question about rollback process..." (4 hours ago)  │
│                                                                 │
│  [👍 Helpful] [👎 Not Helpful] [✏️ Suggest Edit] [💬 Comment] │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Admin Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚙️ Knowledge Base Administration                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 Usage Analytics (Last 30 Days):                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📈 Total Searches: 2,847 (+15% from last month)        │   │
│  │ 👥 Active Users: 47/52 team members (90% adoption)     │   │
│  │ ⏱️ Avg Response Time: 0.3s (target: <0.5s)             │   │
│  │ 🎯 Success Rate: 94% queries found relevant results    │   │
│  │ ⭐ User Satisfaction: 4.6/5 (143 ratings)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔄 Data Sources Status:                                       │
│  ├─ ✅ Slack (Connected) • Last sync: 2 min ago               │
│  ├─ ✅ Confluence (Connected) • Last sync: 5 min ago          │
│  ├─ ✅ Google Drive (Connected) • Last sync: 1 min ago        │
│  ├─ ⚠️ GitHub (Rate Limited) • Last sync: 30 min ago          │
│  └─ ❌ Notion (Connection Error) • Last attempt: 2 hours ago  │
│                                                                 │
│  📚 Content Overview:                                          │
│  ├─ 📄 Documents: 1,234 indexed (+45 this week)               │
│  ├─ 💬 Conversations: 5,678 Slack messages indexed            │
│  ├─ 🎥 Recordings: 89 meeting transcripts                     │
│  ├─ 💻 Code Files: 456 documentation files                    │
│  └─ 🏷️ Tags: 127 unique tags created                          │
│                                                                 │
│  🔧 System Health:                                             │
│  ├─ 💾 Storage Used: 2.3GB / 10GB (23%)                      │
│  ├─ 🔍 Search Index: Healthy (rebuilt 6 hours ago)            │
│  ├─ 🖥️ Server Load: Low (15% CPU, 2.1GB RAM)                │
│  └─ 🌐 Uptime: 99.8% (last 30 days)                          │
│                                                                 │
│  [🔄 Force Sync] [📊 Detailed Analytics] [⚙️ Settings]        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Mobile Search Interface

```
┌─────────────────────────────┐
│  🧠 {{COMPANY_NAME}} KB     │
├─────────────────────────────┤
│                             │
│ 🔍 Search knowledge...     │
│ ┌─────────────────────────┐ │
│ │ "API documentation"     │ │
│ └─────────────────────────┘ │
│                             │
│ 🎯 Quick Results:           │
│ ┌─────────────────────────┐ │
│ │ 📄 REST API Guide       │ │
│ │ Updated 2 days ago      │ │
│ │ ⭐⭐⭐⭐⭐ 4.9/5          │ │
│ │                         │ │
│ │ 💬 API Design Discussion│ │
│ │ #backend • 12 messages  │ │
│ │ 📅 Yesterday            │ │
│ │                         │ │
│ │ 💻 api-docs/swagger.yml │ │
│ │ OpenAPI specification   │ │
│ │ 📅 Last week            │ │
│ └─────────────────────────┘ │
│                             │
│ 📊 47 searches today        │
│                             │
│ [🏠] [🔍] [📝] [👤]         │
└─────────────────────────────┘
```

## Quick Add Content Modal

```
┌─────────────────────────────────────────────────────────────────┐
│  📝 Add New Knowledge                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 Title: [                                                   ]│
│  "How to set up development environment"                       │
│                                                                 │
│  🏷️ Tags: [backend] [setup] [development] [onboarding]        │
│                                                                 │
│  📁 Content Type:                                              │
│  ◉ Document/Guide    ○ FAQ Entry    ○ Code Example            │
│  ○ Meeting Notes     ○ Decision Log ○ Troubleshooting         │
│                                                                 │
│  ✍️ Content:                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ## Prerequisites                                        │   │
│  │                                                         │   │
│  │ Before setting up the development environment:         │   │
│  │                                                         │   │
│  │ 1. Install Node.js 18+                                │   │
│  │ 2. Install Docker Desktop                              │   │
│  │ 3. Clone the repository                                │   │
│  │                                                         │   │
│  │ ## Setup Steps                                          │   │
│  │                                                         │   │
│  │ ```bash                                                 │   │
│  │ npm install                                             │   │
│  │ cp .env.example .env                                    │   │
│  │ docker-compose up -d                                    │   │
│  │ ```                                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  👥 Visibility: ◉ Team-wide  ○ Department  ○ Company-wide     │
│                                                                 │
│  [💾 Save & Index] [📋 Save Draft] [❌ Cancel]                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Notification/Alert Settings

```
┌─────────────────────────────────────────────────────────────────┐
│  🔔 Knowledge Base Notifications                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📬 Saved Searches & Alerts:                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔍 "deployment process"                                 │   │
│  │    └─ 🔔 Alert when new content added                   │   │
│  │    └─ 📅 Weekly digest enabled                          │   │
│  │                                                         │   │
│  │ 🔍 "API documentation"                                  │   │
│  │    └─ 🔔 Alert on updates to existing docs             │   │
│  │    └─ 📧 Email notifications enabled                    │   │
│  │                                                         │   │
│  │ 🔍 "security best practices"                           │   │
│  │    └─ 🔔 Immediate alerts for new content              │   │
│  │    └─ 💬 Slack DM notifications                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📊 Content You Follow:                                        │
│  ├─ 📄 "Production Runbook" (5 watchers)                      │
│  ├─ 📄 "API Authentication Guide" (12 watchers)               │
│  ├─ 💬 #backend-architecture discussions                       │
│  └─ 👤 Sarah Chen's documents (DevOps Lead)                   │
│                                                                 │
│  ⚙️ Notification Preferences:                                 │
│  ├─ 🔔 Browser notifications: ☑️ Enabled                      │
│  ├─ 📧 Email digest frequency: [Daily ▼]                      │
│  ├─ 💬 Slack integration: ☑️ Enabled                          │
│  └─ 📱 Mobile push: ☐ Disabled                                │
│                                                                 │
│  [➕ Add New Alert] [⚙️ Notification Settings]                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Benefits of ASCII Mockups

- **Token Efficient**: 80% fewer tokens than prose descriptions
- **Visual Clarity**: Immediate understanding of layout and functionality  
- **Standardized Format**: Consistent across all KAPI documentation
- **Implementation Ready**: Direct translation to actual UI components
- **Collaborative**: Easy to modify and iterate in text format
- **Version Control**: Trackable changes in Git alongside code

---

**These ASCII mockups provide complete visual specifications for the Team Knowledge Base interface, enabling rapid development while maintaining design consistency.**