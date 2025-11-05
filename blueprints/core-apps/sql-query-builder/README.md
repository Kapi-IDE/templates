# SQL Query Builder

AI-powered natural language to SQL converter with query validation, execution, and visualization.

**Core App #7** - Demonstrates AI-powered data analysis and SQL generation.

## ✨ Features

- **Natural Language to SQL**: Ask questions in plain English, get SQL queries
- **Multi-Database Support**: PostgreSQL, MySQL, SQLite
- **Schema-Aware**: AI understands your database structure
- **Query Validation**: Syntax checking before execution
- **Safety Controls**: Prevent destructive queries, limit result sizes
- **Monaco Editor**: VS Code-style SQL editor with syntax highlighting
- **Query Execution**: Run queries directly against your database
- **Result Visualization**: Tables, charts, and export to CSV/JSON
- **Query History**: Save and reuse successful queries
- **Share Queries**: Generate shareable links with results
- **Schema Visualization**: Visual database diagram
- **Query Explanation**: AI explains what the SQL query does

## 🚀 Quick Start (22 minutes)

### Prerequisites
- Node.js 18+
- PostgreSQL, MySQL, or SQLite database
- OpenAI API key

### Setup

```bash
# 1. Clone/copy this directory
cd sql-query-builder

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env.local

# 4. Edit .env.local with your credentials:
#    - OPENAI_API_KEY (required)
#    - DATABASE_URL (required)
#    - OPENAI_MODEL (optional, defaults to gpt-4o-mini)

# 5. Setup database (if needed)
npx prisma db push

# 6. Start development server
npm run dev
```

Visit http://localhost:3000

## 🔐 API Key Setup (REQUIRED)

### Step 1: Get Your OpenAI API Key

**⚠️ IMPORTANT: This app REQUIRES an OpenAI API key to function**

1. **Create OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Sign up with email or Google/Microsoft account
   - Verify your email address

2. **Add Payment Method** (Required for API access)
   - Go to https://platform.openai.com/account/billing
   - Click "Add payment method"
   - **Cost**: $0.10-$1.65 per 1,000 queries (see pricing below)
   - Free tier: $5 in credits (expires after 3 months)

3. **Create API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - **Copy immediately**: The key is only shown once
   - **Format**: Starts with `sk-proj-`

4. **Add to .env.local**
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

### Step 2: Configure Database Connection

**PostgreSQL (Recommended)**

```bash
# Local PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/myapp
DB_TYPE=postgresql

# Vercel Postgres
DATABASE_URL=postgresql://user:pass@region.postgres.vercel.com:5432/database

# Supabase
DATABASE_URL=postgresql://user:pass@db.xxx.supabase.co:5432/postgres

# Railway
DATABASE_URL=postgresql://user:pass@containers-us-west-xxx.railway.app:5432/railway
```

**MySQL**

```bash
DATABASE_URL=mysql://user:password@localhost:3306/myapp
DB_TYPE=mysql
```

**SQLite (Development Only)**

```bash
DATABASE_URL=file:./dev.db
DB_TYPE=sqlite
```

### Step 3: Configure Safety Settings (Optional)

```bash
# Recommended production settings
ENABLE_QUERY_VALIDATION=true
ALLOW_DESTRUCTIVE_QUERIES=false
MAX_RESULT_ROWS=1000
QUERY_TIMEOUT_MS=30000
```

## 💰 Pricing

### OpenAI Models (Per 1M Tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| **gpt-4o-mini** | $0.15 | $0.60 | **RECOMMENDED** - Fast, accurate SQL |
| gpt-4o | $2.50 | $10.00 | Complex queries, multiple tables |
| gpt-3.5-turbo | $0.50 | $1.50 | Simple queries, budget option |

### Cost Per Query

**Typical SQL query generation:**
- Schema context: ~500 tokens (input)
- User question: ~50 tokens (input)
- SQL output: ~100 tokens (output)
- **Total**: ~650 tokens

**Cost with gpt-4o-mini**:
- Per query: ~$0.0001 (1/100th of a cent)
- 1,000 queries: ~$0.10
- 10,000 queries: ~$1.00

**Cost with gpt-4o** (for complex queries):
- Per query: ~$0.0017 (1/6th of a cent)
- 1,000 queries: ~$1.65
- 10,000 queries: ~$16.50

### Monthly Cost Examples

| Usage Level | Queries/Month | gpt-4o-mini | gpt-4o |
|-------------|---------------|-------------|--------|
| Personal | 100 | $0.01 | $0.17 |
| Small Team | 1,000 | $0.10 | $1.65 |
| Department | 10,000 | $1.00 | $16.50 |
| Enterprise | 100,000 | $10.00 | $165.00 |

**Recommendation**: Start with gpt-4o-mini. Upgrade to gpt-4o only if you need higher accuracy for complex multi-table queries.

## 🏗️ Architecture

```
sql-query-builder/
├── app/
│   ├── page.tsx                    # Main query interface
│   ├── api/
│   │   ├── generate-sql/route.ts   # Natural language → SQL
│   │   ├── execute-query/route.ts  # Run SQL against database
│   │   ├── validate-query/route.ts # Check SQL syntax
│   │   ├── explain-query/route.ts  # AI explains SQL
│   │   └── schema/route.ts         # Fetch database schema
│   └── components/
│       ├── QueryInput.tsx          # Natural language input
│       ├── SQLEditor.tsx           # Monaco editor for SQL
│       ├── ResultsTable.tsx        # Display query results
│       ├── ResultsChart.tsx        # Visualize data
│       ├── SchemaViewer.tsx        # Database schema diagram
│       └── QueryHistory.tsx        # Saved queries
├── lib/
│   ├── sql-generator.ts            # OpenAI SQL generation
│   ├── query-validator.ts          # SQL validation logic
│   ├── db-introspection.ts         # Schema extraction
│   └── query-executor.ts           # Safe query execution
└── prisma/
    └── schema.prisma               # Query history storage
```

## 🎯 How It Works

### 1. Schema Introspection

The app automatically reads your database schema:

```typescript
// Extracts tables, columns, types, relationships
const schema = await introspectDatabase(databaseUrl);
// Returns: { tables, columns, foreignKeys, indexes }
```

### 2. Natural Language → SQL

User asks a question, AI generates SQL using schema context:

```typescript
const sql = await generateSQL({
  question: "Show me top 10 customers by order value",
  schema: schema,
  database: "postgresql"
});

// Returns:
// SELECT c.name, SUM(o.total) as total_value
// FROM customers c
// JOIN orders o ON c.id = o.customer_id
// GROUP BY c.id, c.name
// ORDER BY total_value DESC
// LIMIT 10;
```

### 3. Query Validation

Before execution, check for:
- ✅ SQL syntax errors
- ✅ Destructive operations (DELETE, DROP, TRUNCATE)
- ✅ Table/column existence
- ✅ Dangerous patterns (SELECT * FROM huge_table)

### 4. Safe Execution

Execute with safety limits:
```typescript
const results = await executeQuery(sql, {
  maxRows: 1000,
  timeout: 30000,
  readOnly: true
});
```

### 5. Visualization

Display results as:
- **Table**: Sortable, filterable, paginated
- **Chart**: Auto-detect chart type based on data
- **Export**: CSV, JSON, or copy to clipboard

## 🔒 Security Best Practices

### 1. Read-Only Database User (Recommended)

Create a dedicated database user with SELECT-only permissions:

```sql
-- PostgreSQL
CREATE USER query_builder_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE myapp TO query_builder_readonly;
GRANT USAGE ON SCHEMA public TO query_builder_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO query_builder_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO query_builder_readonly;

-- Then use in .env.local:
DATABASE_URL=postgresql://query_builder_readonly:secure_password@localhost:5432/myapp
```

```sql
-- MySQL
CREATE USER 'query_builder_readonly'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT ON myapp.* TO 'query_builder_readonly'@'%';
FLUSH PRIVILEGES;
```

### 2. Disable Destructive Queries

```bash
# .env.local
ALLOW_DESTRUCTIVE_QUERIES=false  # Blocks DELETE, DROP, TRUNCATE
```

### 3. Limit Result Sizes

```bash
MAX_RESULT_ROWS=1000  # Prevents accidentally returning millions of rows
```

### 4. Query Timeout

```bash
QUERY_TIMEOUT_MS=30000  # Kill queries after 30 seconds
```

### 5. IP Whitelisting (Production)

```bash
ALLOWED_IPS=203.0.113.0,198.51.100.0  # Comma-separated
```

### 6. API Key Rotation

- Rotate OpenAI API keys every 90 days
- Use separate keys for dev/staging/production
- Set usage limits in OpenAI dashboard

### 7. Monitor Usage

**OpenAI Dashboard**: https://platform.openai.com/usage
- Set up budget alerts
- Monitor token consumption
- Track costs by project

**Database Monitoring**:
- Log all executed queries
- Monitor query performance
- Alert on slow queries

## 🚢 Production Deployment

### Vercel (Recommended)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Set environment variables
vercel env add OPENAI_API_KEY
vercel env add DATABASE_URL
vercel env add OPENAI_MODEL

# 4. Deploy to production
vercel --prod
```

**Environment Variables in Vercel Dashboard**:
1. Go to Project Settings → Environment Variables
2. Add all required variables
3. Redeploy

### Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Link project
railway link

# 4. Set variables
railway variables set OPENAI_API_KEY=sk-proj-...
railway variables set DATABASE_URL=postgresql://...

# 5. Deploy
railway up
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Build
docker build -t sql-query-builder .

# Run
docker run -e OPENAI_API_KEY=sk-proj-... \
           -e DATABASE_URL=postgresql://... \
           -p 3000:3000 \
           sql-query-builder
```

## 🐛 Troubleshooting

### "Invalid API Key" Error

**Problem**: OpenAI API key not working

**Solution**:
```bash
# 1. Verify key format (should start with sk-proj-)
echo $OPENAI_API_KEY

# 2. Check key is active
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 3. Regenerate key if needed
# Go to https://platform.openai.com/api-keys
```

### "Database Connection Failed"

**Problem**: Cannot connect to database

**Solution**:
```bash
# 1. Test connection string
psql "$DATABASE_URL"  # PostgreSQL
mysql --uri="$DATABASE_URL"  # MySQL

# 2. Check firewall/network
nc -zv your-db-host 5432  # PostgreSQL
nc -zv your-db-host 3306  # MySQL

# 3. Verify credentials
# - Username correct?
# - Password correct?
# - Database exists?
# - IP whitelisted?
```

### "Generated SQL is Incorrect"

**Problem**: AI generates wrong SQL for your schema

**Solution**:
1. **Check schema introspection**: Verify the app correctly reads your tables/columns
2. **Use gpt-4o**: More accurate for complex schemas
3. **Provide examples**: Add sample queries to train the AI
4. **Simplify question**: Break complex questions into smaller queries
5. **Manual edit**: Use Monaco editor to fix SQL before running

### "Query Timeout"

**Problem**: Query takes too long to execute

**Solution**:
```bash
# 1. Increase timeout
QUERY_TIMEOUT_MS=60000  # 60 seconds

# 2. Add database indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

# 3. Limit result size
MAX_RESULT_ROWS=100  # Fetch fewer rows

# 4. Optimize query
# - Add WHERE clauses
# - Use proper indexes
# - Avoid SELECT *
```

### "Rate Limit Exceeded"

**Problem**: Too many OpenAI API requests

**Solution**:
1. **Check usage**: https://platform.openai.com/usage
2. **Implement caching**: Store generated SQL for common questions
3. **Increase rate limit**: Upgrade OpenAI account tier
4. **Batch requests**: Generate multiple queries in one call

## 📊 Example Queries

### Simple Queries

**Question**: "Show me all customers from California"
```sql
SELECT * FROM customers WHERE state = 'CA';
```

**Question**: "Count total orders by status"
```sql
SELECT status, COUNT(*) as count
FROM orders
GROUP BY status
ORDER BY count DESC;
```

### Complex Queries

**Question**: "Top 10 products by revenue in the last 30 days"
```sql
SELECT
  p.name,
  SUM(oi.quantity * oi.price) as revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.created_at >= NOW() - INTERVAL '30 days'
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 10;
```

**Question**: "Customer lifetime value (CLV) for active customers"
```sql
SELECT
  c.id,
  c.name,
  c.email,
  COUNT(o.id) as order_count,
  SUM(o.total) as lifetime_value,
  AVG(o.total) as avg_order_value
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.status = 'active'
GROUP BY c.id, c.name, c.email
HAVING COUNT(o.id) > 0
ORDER BY lifetime_value DESC;
```

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build**:

1. ✅ **Specification**: Natural language to SQL with safety controls
2. ✅ **Architecture**: Schema introspection → AI generation → Validation → Execution
3. ✅ **Implementation**: OpenAI integration + Monaco editor + Result visualization
4. ✅ **Quality Gates**: Query validation, safety limits, error handling

**Component Reuse**:
- Monaco Editor (NEW - VS Code-style SQL editor)
- OpenAI integration (EXISTING - similar to ai-chat-interface)
- Query result visualization (NEW - tables + charts)

**Token Savings**: ~60% by using existing OpenAI patterns and Monaco editor library.

## 📚 Resources

**OpenAI**:
- [API Documentation](https://platform.openai.com/docs)
- [Pricing](https://openai.com/pricing)
- [Usage Dashboard](https://platform.openai.com/usage)
- [Best Practices](https://platform.openai.com/docs/guides/best-practices)

**Monaco Editor**:
- [Documentation](https://microsoft.github.io/monaco-editor/)
- [SQL Language Support](https://microsoft.github.io/monaco-editor/playground.html#extending-language-services-sql-support)

**Database Drivers**:
- [PostgreSQL (pg)](https://node-postgres.com/)
- [MySQL (mysql2)](https://github.com/sidorares/node-mysql2)
- [SQLite (better-sqlite3)](https://github.com/WiseLibs/better-sqlite3)

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.
