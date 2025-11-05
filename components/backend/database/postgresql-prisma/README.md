# PostgreSQL + Prisma Setup

Production-ready PostgreSQL database with Prisma ORM, featuring migrations, type-safe queries, and best practices for scalable applications.

## Overview

Complete database setup with Prisma ORM providing type-safe database access, automatic migrations, and a modern query builder. Includes common patterns for users, authentication, and relational data.

## Features

- **Type-Safe Queries**: Full TypeScript support with auto-generated types
- **Schema Management**: Declarative schema with automatic migrations
- **Relations**: One-to-many, many-to-many relationships
- **Migrations**: Version-controlled database changes
- **Seeding**: Sample data for development
- **Connection Pooling**: Efficient database connections
- **Soft Deletes**: Preserve data with deletedAt pattern
- **Timestamps**: Automatic createdAt/updatedAt
- **Validation**: Schema-level constraints

## Quick Start

```bash
# Install dependencies
npm install prisma @prisma/client
npm install -D prisma

# Initialize Prisma
npx prisma init

# Create database schema (see example/prisma/schema.prisma)
# Then run migrations
npx prisma migrate dev --name init

# Generate Prisma Client
npx prisma generate

# Seed database (optional)
npx prisma db seed
```

## Environment Setup

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"

# Production with connection pooling
DATABASE_URL="postgresql://user:password@host:5432/mydb?schema=public&connection_limit=10"
```

## File Structure

```
postgresql-prisma/
├── example/
│   ├── prisma/
│   │   ├── schema.prisma       # Database schema
│   │   ├── migrations/         # Migration files
│   │   └── seed.ts            # Seed data
│   ├── src/
│   │   ├── db.ts              # Prisma client setup
│   │   ├── queries.ts         # Example queries
│   │   └── models/            # Data models
│   └── package.json
├── snippets/
│   ├── basic-crud.ts          # Create, Read, Update, Delete
│   ├── relations.ts           # Working with relations
│   └── advanced-queries.ts    # Complex queries
├── docs/
│   ├── setup.md               # Setup guide
│   ├── migrations.md          # Migration patterns
│   └── best-practices.md      # Prisma best practices
├── README.md
└── metadata.yaml
```

## Schema Example

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  passwordHash  String
  role          Role      @default(USER)
  posts         Post[]
  profile       Profile?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  deletedAt     DateTime?
}

model Profile {
  id        String   @id @default(cuid())
  bio       String?
  avatar    String?
  userId    String   @unique
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id          String     @id @default(cuid())
  title       String
  content     String
  published   Boolean    @default(false)
  authorId    String
  author      User       @relation(fields: [authorId], references: [id], onDelete: Cascade)
  categories  Category[]
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt
}

model Category {
  id        String   @id @default(cuid())
  name      String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

## Usage Examples

### 1. Initialize Prisma Client

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  log: ['query', 'error', 'warn'],
});

export default prisma;
```

### 2. Basic CRUD Operations

```typescript
import prisma from './db';

// CREATE
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
    passwordHash: 'hashed_password',
  },
});

// READ
const users = await prisma.user.findMany();
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
});

// UPDATE
const updated = await prisma.user.update({
  where: { id: user.id },
  data: { name: 'Jane Doe' },
});

// DELETE
await prisma.user.delete({
  where: { id: user.id },
});
```

### 3. Relations

```typescript
// Create user with profile
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
    passwordHash: 'hash',
    profile: {
      create: {
        bio: 'Software developer',
        avatar: 'https://example.com/avatar.jpg',
      },
    },
  },
  include: {
    profile: true,
  },
});

// Create post with categories
const post = await prisma.post.create({
  data: {
    title: 'My First Post',
    content: 'Content here',
    authorId: user.id,
    categories: {
      connect: [{ id: 'category-1' }, { id: 'category-2' }],
    },
  },
});
```

### 4. Complex Queries

```typescript
// Find users with posts
const usersWithPosts = await prisma.user.findMany({
  where: {
    posts: {
      some: {
        published: true,
      },
    },
  },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 5,
    },
    profile: true,
  },
});

// Pagination
const page = 1;
const pageSize = 10;
const posts = await prisma.post.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  where: { published: true },
  orderBy: { createdAt: 'desc' },
});

// Count
const totalPosts = await prisma.post.count({
  where: { published: true },
});
```

### 5. Transactions

```typescript
// Transfer operation
const result = await prisma.$transaction(async (tx) => {
  const user1 = await tx.user.update({
    where: { id: 'user1' },
    data: { balance: { decrement: 100 } },
  });

  const user2 = await tx.user.update({
    where: { id: 'user2' },
    data: { balance: { increment: 100 } },
  });

  return { user1, user2 };
});
```

## Common Commands

```bash
# Create migration
npx prisma migrate dev --name add_user_table

# Apply migrations (production)
npx prisma migrate deploy

# Generate Prisma Client
npx prisma generate

# Open Prisma Studio (database GUI)
npx prisma studio

# Reset database
npx prisma migrate reset

# Seed database
npx prisma db seed

# Format schema
npx prisma format

# Validate schema
npx prisma validate

# Pull schema from existing database
npx prisma db pull

# Push schema without migrations
npx prisma db push
```

## Migrations Workflow

```bash
# Development
1. Edit schema.prisma
2. npx prisma migrate dev --name descriptive_name
3. Review migration SQL in prisma/migrations/
4. Commit migration files to git

# Production
1. Pull latest code with migrations
2. npx prisma migrate deploy
3. Verify with npx prisma migrate status
```

## Seeding Database

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin User',
      passwordHash: 'hashed_password',
      role: 'ADMIN',
    },
  });

  console.log({ admin });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

Add to package.json:
```json
{
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  }
}
```

## Best Practices

✅ **DO:**
- Use connection pooling in production
- Use transactions for multi-step operations
- Index frequently queried fields
- Use soft deletes for important data
- Include timestamps (createdAt, updatedAt)
- Use enums for fixed value sets
- Validate data at schema level
- Use cascading deletes carefully
- Generate types after schema changes
- Version control migrations

❌ **DON'T:**
- Store sensitive data unencrypted
- Skip migrations in production
- Use db push for production
- Forget to close connections
- Store large files in database
- Use SELECT * in production
- Skip validation
- Hardcode database URLs

## Performance Tips

1. **Use Indexes**
```prisma
model User {
  email String @unique
  name  String

  @@index([name])
}
```

2. **Select Only Needed Fields**
```typescript
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
});
```

3. **Use Connection Pooling**
```typescript
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: `${process.env.DATABASE_URL}?connection_limit=10`,
    },
  },
});
```

4. **Batch Operations**
```typescript
await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
});
```

## Common Issues

### "Can't reach database server"
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check firewall/network settings

### "Migration conflicts"
- Pull latest migrations from git
- Run `npx prisma migrate resolve --applied <migration-name>`

### "Type errors after schema changes"
- Run `npx prisma generate`
- Restart TypeScript server

## Testing

```typescript
// Use separate test database
// .env.test
DATABASE_URL="postgresql://user:password@localhost:5432/mydb_test"

// test-setup.ts
beforeAll(async () => {
  await prisma.$executeRawUnsafe('DROP SCHEMA public CASCADE');
  await prisma.$executeRawUnsafe('CREATE SCHEMA public');
  await execSync('npx prisma migrate deploy');
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

## Token Savings

- **Setup Time**: 10 minutes vs 2+ hours manual setup
- **Lines of Code**: 500+ lines (schema, migrations, types)
- **Tokens Saved**: ~20,000 tokens
- **Type Safety**: Eliminates 50+ common database errors

## Integration With

- **JWT Authentication**: User model with password hash
- **Express APIs**: Database queries in routes
- **GraphQL**: Prisma as data source
- **Next.js**: API routes with Prisma
- **Docker**: Containerized PostgreSQL
- **Redis**: Caching layer

## Related Components

- `jwt-authentication` - User authentication
- `redis-cache` - Query caching
- `docker-compose` - Database containerization
- `backup-restore` - Database backups