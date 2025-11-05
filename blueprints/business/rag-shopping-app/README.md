# 🛍️ RAG-Powered Shopping App

**Semantic product search meets e-commerce** - A lightweight Next.js shopping app with AI-powered product discovery using RAG (Retrieval-Augmented Generation).

**Setup Time:** 18 min | **Token Budget:** 2.3K (77% under budget!) | **Difficulty:** Intermediate

---

## 🎯 What Makes This Different

Traditional e-commerce search is keyword-based and frustrating. This blueprint uses **RAG** to understand intent:

❌ **Traditional:** Search "running shoes" → Only finds exact "running shoes"
✅ **RAG-Powered:** Search "shoes for marathon training" → Finds running shoes, compression socks, hydration gear

**Key Features:**
- 🔍 **Semantic Product Search** - Natural language queries
- 🤖 **AI Shopping Assistant** - Chat with AI about products
- 💬 **Context-Aware Responses** - GPT-4 powered recommendations
- 🛒 **Simple Cart** - Minimal checkout flow
- 📦 **Product Catalog** - 20 sample products across 7 categories

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- OpenAI API key

### Installation

```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Add OPENAI_API_KEY=sk-...

# Start development
npm run dev
```

Visit **http://localhost:3000**

### Example Queries
Try these semantic searches:
- "shoes for marathon training on pavement"
- "eco-friendly workout gear"
- "gear for winter hiking"
- "gadgets for outdoor camping"

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│         (Next.js App Router + Tailwind CSS)             │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Product    │  │  Semantic    │  │  Shopping    │ │
│  │   Grid       │  │  Search Bar  │  │  Cart        │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   API Routes                             │
│                                                          │
│  /api/products/search → Semantic product search          │
│  /api/chat → Shopping assistant chatbot                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  RAG Engine (lib/rag-engine.ts)          │
│                                                          │
│  1. Query Embedding (OpenAI text-embedding-3-small)     │
│  2. Vector Search (cosine similarity)                   │
│  3. Context Assembly (Top 5 products)                   │
│  4. LLM Response (GPT-4 with product context)           │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Product Data Store                          │
│                                                          │
│  data/products.json → 20 sample products                 │
│  Real-time embedding generation                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Features

### 1. Semantic Product Search

**Traditional Keyword Search:**
```
User: "running shoes"
Results: Products with exact "running shoes" in title
```

**RAG-Powered Semantic Search:**
```
User: "shoes for marathon training on pavement"
AI Understanding:
  - Intent: long-distance running
  - Surface: road running
  - Need: cushioning, durability
Results:
  1. Road Running Shoes - CloudFlex Pro (95% match)
  2. Compression Running Socks (73% match)
  3. Smart Fitness Watch (65% match)
```

**How It Works:**
1. User enters natural language query
2. Query is converted to embedding vector (1536 dimensions)
3. Each product is embedded using name + description + tags
4. Cosine similarity calculates relevance
5. Top matches returned with similarity scores

### 2. AI Shopping Assistant

Chat with AI about products in natural language:

**Example Conversation:**
```
User: "I need gear for winter hiking"
Assistant: "For winter hiking, I'd recommend:
1. Trail Hiking Boots - MountainGrip ($159.99) - Waterproof with
   ankle support, perfect for winter trails
2. Insulated Winter Jacket ($189.99) - Lightweight down with
   water-resistant shell
3. Thermal Sleeping Bag ($89.99) - Rated for 20°F

Would you like more details on any of these?"

User: "Tell me more about the boots"
Assistant: "The MountainGrip boots feature..."
```

**How It Works:**
1. User message triggers semantic search
2. Top 5 relevant products retrieved
3. Product context injected into GPT-4 prompt
4. AI responds with personalized recommendations
5. Conversation history maintained for context

### 3. Product Catalog

**20 Sample Products Across 7 Categories:**
- **Footwear:** Running shoes, hiking boots
- **Electronics:** Headphones, fitness watch, speaker, solar charger
- **Fitness:** Yoga mat, resistance bands, dumbbells, foam roller
- **Apparel:** Winter jacket, t-shirt, compression socks
- **Outdoor Gear:** Tent, sleeping bag, backpack, lantern
- **Accessories:** Water bottle
- **Home:** Memory foam pillow, air purifier

Each product includes:
- Name, category, price
- Detailed description
- Searchable tags
- Image placeholder (category emoji)

### 4. Simple Shopping Cart

- Add/remove products
- Real-time total calculation
- Minimal checkout UI
- Sidebar modal for quick access

---

## 💻 Code Structure

```
rag-shopping-app/
├── app/
│   ├── page.tsx                  # Main page with product grid
│   ├── layout.tsx                # Root layout
│   ├── globals.css               # Tailwind imports
│   └── api/
│       ├── products/search/route.ts  # Semantic search endpoint
│       └── chat/route.ts             # AI assistant endpoint
├── components/
│   ├── ProductGrid.tsx           # Product display with search
│   ├── SearchBar.tsx             # Semantic search input
│   ├── ShoppingAssistant.tsx    # AI chat sidebar
│   └── Cart.tsx                  # Shopping cart sidebar
├── lib/
│   └── rag-engine.ts             # Core RAG implementation
├── data/
│   └── products.json             # Product catalog
├── package.json
└── .env.example
```

### Key Files

**`lib/rag-engine.ts` (555 tokens)** - Core RAG Engine
```typescript
// Functions:
- generateEmbedding(text) → Generate OpenAI embedding
- semanticProductSearch(query, limit) → Find matching products
- shoppingAssistant(query, history) → Chat with context
- getRecommendations(preferences) → AI recommendations
- explainMatch(product, query) → Explain relevance
```

**`app/api/products/search/route.ts`** - Search API
```typescript
POST /api/products/search
Body: { query: "winter hiking gear" }
Response: { products: [...] }  // With similarity scores
```

**`app/api/chat/route.ts`** - Chat API
```typescript
POST /api/chat
Body: { query: "...", history: [...] }
Response: { response: "..." }
```

---

## 🔧 Configuration

### Environment Variables

```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-...
```

### Customization

**Add More Products:**
Edit `data/products.json`:
```json
{
  "id": "prod_021",
  "name": "Your Product Name",
  "category": "Category",
  "price": 99.99,
  "description": "Detailed description...",
  "tags": ["tag1", "tag2"],
  "image": "/products/image.jpg"
}
```

**Adjust Search Sensitivity:**
In `lib/rag-engine.ts`, modify similarity threshold:
```typescript
// More strict matching (higher threshold)
return productsWithScores
  .filter(p => p.similarity > 0.7)  // Default: no filter
  .slice(0, limit);
```

**Change AI Model:**
```typescript
// In shoppingAssistant() function
const response = await openai.chat.completions.create({
  model: 'gpt-3.5-turbo',  // Cheaper option
  // or 'gpt-4-turbo' for better responses
  ...
});
```

---

## 📊 Performance & Cost

### Token Usage
- **Total Blueprint:** 2,264 tokens (77% under 10K budget)
- **Largest File:** `lib/rag-engine.ts` (555 tokens)

### API Costs (Approximate)

**Per Search Query:**
- Embedding generation: ~$0.00001 per query (text-embedding-3-small)
- Total per search: ~$0.0002

**Per Chat Message:**
- Query embedding: ~$0.00001
- Product embeddings (5 products): ~$0.00005
- GPT-4 response (300 tokens): ~$0.003
- Total per message: ~$0.0035

**With 1000 Users/Day:**
- 1000 searches: ~$0.20
- 500 chat messages: ~$1.75
- **Daily cost:** ~$2/day or $60/month

**Cost Optimization:**
- Use `gpt-3.5-turbo` instead of `gpt-4`: 10x cheaper
- Cache embeddings in database: Eliminate re-computation
- Use cheaper embedding model: `text-embedding-ada-002`

---

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add OPENAI_API_KEY
```

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

```bash
docker build -t rag-shopping-app .
docker run -p 3000:3000 -e OPENAI_API_KEY=sk-... rag-shopping-app
```

---

## 🎯 Use Cases

### 1. E-Commerce with Complex Products
**Example:** Outdoor gear, sports equipment, technical products
- Customers struggle with keyword search
- Natural language describes needs better
- AI explains why products match

### 2. Internal Product Catalog
**Example:** Enterprise software catalog, hardware inventory
- Employees search by use case, not product name
- "Find me tools for data migration"
- Reduces support tickets

### 3. Marketplace with Diverse Inventory
**Example:** Multi-vendor marketplace
- Products from different sellers with inconsistent naming
- Semantic search unifies discovery
- AI assistant answers pre-sale questions

### 4. Educational Product Catalog
**Example:** Learning resources, courses
- Students search by learning goal
- "I want to learn React for job interviews"
- AI recommends relevant courses

---

## 🔍 How RAG Works (Technical Deep Dive)

### 1. Embedding Generation
```
Text: "shoes for marathon training"
↓ OpenAI API
Vector: [0.182, -0.045, 0.392, ...] (1536 dimensions)
```

### 2. Similarity Calculation
```
Query Vector:    [0.182, -0.045, 0.392, ...]
Product Vector:  [0.190, -0.039, 0.385, ...]
                         ↓
           Cosine Similarity = 0.95 (95% match)
```

### 3. Context Assembly
```
Top 5 Products Retrieved:
- Road Running Shoes (0.95 similarity)
- Compression Socks (0.73 similarity)
- Fitness Watch (0.65 similarity)
- Water Bottle (0.58 similarity)
- Foam Roller (0.52 similarity)
```

### 4. LLM Response Generation
```
System Prompt: "You are a shopping assistant. Here are relevant products..."
User Query: "shoes for marathon training"
Context: [5 products with details]
                ↓
GPT-4: "I recommend the Road Running Shoes - CloudFlex Pro ($129.99).
        They're specifically designed for marathon training with..."
```

---

## 🧪 Testing

### Test Semantic Search

```bash
curl -X POST http://localhost:3000/api/products/search \
  -H "Content-Type: application/json" \
  -d '{"query": "winter hiking gear"}'
```

### Test AI Assistant

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What do you have for camping?", "history": []}'
```

---

## 🛠️ Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:** Check `.env` file exists and contains `OPENAI_API_KEY=sk-...`

### Issue: Search returns no results
**Solution:**
- Ensure OpenAI API key is valid
- Check network connectivity
- Verify products.json is loaded correctly

### Issue: Slow search performance
**Solution:**
- Cache embeddings in database (Redis/PostgreSQL)
- Use batch embedding generation
- Implement debouncing on search input

### Issue: High API costs
**Solution:**
- Switch to `gpt-3.5-turbo` (10x cheaper)
- Use `text-embedding-ada-002` (cheaper embedding model)
- Cache frequent queries
- Implement rate limiting

---

## 📚 Learning Resources

### RAG Concepts
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Vector Search Fundamentals](https://www.pinecone.io/learn/vector-search/)
- [Building RAG Applications](https://www.anthropic.com/news/retrieval-augmented-generation)

### Next.js
- [Next.js App Router](https://nextjs.org/docs/app)
- [API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)

### Related KAPI Blueprints
- `deep-document-analysis` - Full RAG workbench with ChromaDB
- `fastapi-rag-starter` - Production RAG with auth and database
- `perplexity-clone` - Web search + RAG

---

## 🎓 Educational Value

This blueprint teaches:
1. **RAG Architecture** - Retrieval-Augmented Generation patterns
2. **Vector Embeddings** - Text-to-vector conversion and similarity
3. **Semantic Search** - Beyond keyword matching
4. **Context-Aware AI** - Injecting dynamic context into LLM prompts
5. **API Design** - Clean separation of UI and AI logic
6. **Real-Time UX** - Streaming responses and loading states

---

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with KAPI** - Production-ready in 18 minutes
**Token Efficient** - 2.3K tokens (77% under budget)
**Cost Effective** - ~$2/day for 1000 users