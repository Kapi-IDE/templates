# Prisma Schema Patterns

Curated collection of production-ready Prisma schema patterns extracted from official Prisma examples.

## 📚 Patterns Included

### 1. Basic Blog (`01-basic-blog.prisma`)
**Use Case:** Simple blog with users and posts
**Features:**
- One-to-many relationships
- Timestamps (createdAt, updatedAt)
- Optional fields
- Default values
- View counter

**Best For:**
- Content management systems
- Simple blogs
- Learning Prisma basics

---

### 2. NextAuth.js Authentication (`02-auth-nextauth.prisma`)
**Use Case:** Full OAuth authentication with NextAuth.js
**Features:**
- Multi-provider OAuth (Google, GitHub, etc.)
- Session management
- Email verification tokens
- Refresh tokens and access tokens

**Best For:**
- SaaS applications
- Multi-tenant platforms
- Apps requiring OAuth integration

**Reference:** https://authjs.dev/getting-started/adapters/prisma

---

### 3. Clerk Authentication (`03-auth-clerk.prisma`)
**Use Case:** Clerk-based authentication
**Features:**
- External auth provider integration
- Clerk ID mapping
- Simplified user model

**Best For:**
- Next.js applications
- Rapid prototyping with managed auth
- Teams wanting to outsource auth

**Reference:** https://clerk.com/docs

---

### 4. Better Auth (`04-auth-betterauth.prisma`)
**Use Case:** Modern authentication with better-auth
**Features:**
- Session tracking with IP and user agent
- Account linking across providers
- Email verification
- Password and OAuth support

**Best For:**
- Modern web applications
- Apps needing detailed session tracking
- Custom authentication flows

**Reference:** https://www.better-auth.com/

---

### 5. GraphQL with Pothos (`05-graphql-pothos.prisma`)
**Use Case:** GraphQL API with code-first approach
**Features:**
- Automatic GraphQL type generation
- Pothos generator integration
- Type-safe GraphQL development

**Best For:**
- GraphQL APIs
- Type-safe backend development
- Code-first GraphQL schemas

**Reference:** https://pothos-graphql.dev/

---

### 6. MongoDB (`06-mongodb.prisma`)
**Use Case:** NoSQL database with Prisma
**Features:**
- ObjectId handling
- MongoDB-specific directives
- Document-based relationships

**Best For:**
- Flexible schema requirements
- High-volume write operations
- Document-oriented data models

**Note:** MongoDB requires special ID handling with `@map("_id")` and `@db.ObjectId`

---

## 🔧 How to Use These Patterns

### 1. Copy Pattern to Your Project
```bash
# Copy the pattern you need
cp 01-basic-blog.prisma your-project/prisma/schema.prisma
```

### 2. Update Database Connection
```env
# In your .env file
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

### 3. Generate Prisma Client
```bash
npx prisma generate
```

### 4. Run Migrations
```bash
npx prisma migrate dev --name init
```

### 5. Use in Your Code
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create a user
const user = await prisma.user.create({
  data: {
    email: 'john@example.com',
    name: 'John Doe'
  }
})
```

---

## 🗄️ Database Providers

All patterns support multiple providers (change `provider` in datasource block):

- `postgresql` - PostgreSQL (recommended)
- `mysql` - MySQL/MariaDB
- `sqlite` - SQLite (local development)
- `mongodb` - MongoDB (pattern 06 only)
- `sqlserver` - Microsoft SQL Server
- `cockroachdb` - CockroachDB

---

## 🎯 Pattern Selection Guide

| Need | Use Pattern |
|------|-------------|
| Simple app, learning | `01-basic-blog` |
| OAuth (Google, GitHub) | `02-auth-nextauth` |
| Managed auth (Next.js) | `03-auth-clerk` |
| Custom auth with tracking | `04-auth-betterauth` |
| GraphQL API | `05-graphql-pothos` |
| NoSQL/Document store | `06-mongodb` |

---

## 🔒 Security Best Practices

### Passwords
Never store plaintext passwords. Use bcrypt or argon2:
```typescript
import * as bcrypt from 'bcrypt'

const hashedPassword = await bcrypt.hash(password, 10)
```

### Environment Variables
Always use environment variables for sensitive data:
```env
DATABASE_URL="postgresql://..."
NEXTAUTH_SECRET="your-secret-here"
```

### Session Security
- Set appropriate session expiry times
- Rotate session tokens on privilege escalation
- Store only necessary data in sessions

---

## 📖 Advanced Patterns

### Many-to-Many Relationships
```prisma
model Post {
  id         Int        @id @default(autoincrement())
  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  posts Post[]
}
```

### Explicit Join Tables
```prisma
model PostCategory {
  post       Post     @relation(fields: [postId], references: [id])
  postId     Int
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId Int

  @@id([postId, categoryId])
}
```

### Cascading Deletes
```prisma
model Post {
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId Int
}
```

### Indexes for Performance
```prisma
model User {
  email String @unique
  name  String

  @@index([name]) // Speed up name searches
}
```

---

## 🚀 Common Migrations

### Adding a Field
```bash
# 1. Add to schema.prisma
# 2. Create migration
npx prisma migrate dev --name add_field_name
```

### Renaming a Field
```prisma
// Use @map for database backward compatibility
model User {
  fullName String @map("name")
}
```

### Changing Field Type
```bash
# 1. Update schema.prisma
# 2. Generate migration (may require data migration)
npx prisma migrate dev --name change_field_type
```

---

## 📊 Comparison with Other ORMs

| Feature | Prisma | TypeORM | Sequelize |
|---------|--------|---------|-----------|
| Type Safety | ✅ Excellent | ✅ Good | ❌ Weak |
| Schema Definition | Prisma Schema | TypeScript Decorators | JavaScript Models |
| Migrations | Built-in | Built-in | Built-in |
| Query Builder | Type-safe | SQL-like | JavaScript Methods |
| Learning Curve | Easy | Medium | Medium |

---

## 🔗 Resources

- **Official Docs:** https://www.prisma.io/docs
- **Examples Repo:** https://github.com/prisma/prisma-examples
- **Community:** https://www.prisma.io/community
- **Blog:** https://www.prisma.io/blog

---

## 📝 License

These patterns are extracted from Prisma's official examples repository.
Original source: https://github.com/prisma/prisma-examples

MIT License - Free to use in your projects.

---

**Built for KAPI Blueprint System - Production-ready patterns for rapid development**
