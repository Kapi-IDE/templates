import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 10);
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin User',
      passwordHash: adminPassword,
      role: 'ADMIN',
      profile: {
        create: {
          bio: 'System administrator',
          location: 'San Francisco, CA',
        },
      },
    },
    include: {
      profile: true,
    },
  });

  console.log('✅ Created admin user:', admin.email);

  // Create regular users
  const user1Password = await bcrypt.hash('user123', 10);
  const user1 = await prisma.user.upsert({
    where: { email: 'john@example.com' },
    update: {},
    create: {
      email: 'john@example.com',
      name: 'John Doe',
      passwordHash: user1Password,
      role: 'USER',
      profile: {
        create: {
          bio: 'Software developer passionate about TypeScript',
          website: 'https://johndoe.com',
          location: 'New York, NY',
        },
      },
    },
    include: {
      profile: true,
    },
  });

  console.log('✅ Created user:', user1.email);

  const user2Password = await bcrypt.hash('user123', 10);
  const user2 = await prisma.user.upsert({
    where: { email: 'jane@example.com' },
    update: {},
    create: {
      email: 'jane@example.com',
      name: 'Jane Smith',
      passwordHash: user2Password,
      role: 'EDITOR',
      profile: {
        create: {
          bio: 'Technical writer and content creator',
          website: 'https://janesmith.com',
          location: 'Austin, TX',
        },
      },
    },
    include: {
      profile: true,
    },
  });

  console.log('✅ Created user:', user2.email);

  // Create categories
  const techCategory = await prisma.category.upsert({
    where: { slug: 'technology' },
    update: {},
    create: {
      name: 'Technology',
      slug: 'technology',
      description: 'Articles about technology and software development',
    },
  });

  const tutorialCategory = await prisma.category.upsert({
    where: { slug: 'tutorials' },
    update: {},
    create: {
      name: 'Tutorials',
      slug: 'tutorials',
      description: 'Step-by-step guides and tutorials',
    },
  });

  const newsCategory = await prisma.category.upsert({
    where: { slug: 'news' },
    update: {},
    create: {
      name: 'News',
      slug: 'news',
      description: 'Latest news and updates',
    },
  });

  console.log('✅ Created categories');

  // Create tags
  const tags = await Promise.all([
    prisma.tag.upsert({
      where: { name: 'TypeScript' },
      update: {},
      create: { name: 'TypeScript' },
    }),
    prisma.tag.upsert({
      where: { name: 'Node.js' },
      update: {},
      create: { name: 'Node.js' },
    }),
    prisma.tag.upsert({
      where: { name: 'PostgreSQL' },
      update: {},
      create: { name: 'PostgreSQL' },
    }),
    prisma.tag.upsert({
      where: { name: 'Prisma' },
      update: {},
      create: { name: 'Prisma' },
    }),
    prisma.tag.upsert({
      where: { name: 'React' },
      update: {},
      create: { name: 'React' },
    }),
  ]);

  console.log('✅ Created tags');

  // Create posts
  const post1 = await prisma.post.create({
    data: {
      title: 'Getting Started with Prisma',
      slug: 'getting-started-with-prisma',
      excerpt: 'Learn how to set up Prisma in your Node.js project',
      content: `# Getting Started with Prisma

Prisma is a next-generation ORM that makes database access easy and type-safe.

## Installation

\`\`\`bash
npm install prisma @prisma/client
npx prisma init
\`\`\`

## Define Your Schema

Create your data model in \`prisma/schema.prisma\`.

## Generate Client

\`\`\`bash
npx prisma generate
\`\`\`

Now you're ready to query your database!`,
      published: true,
      publishedAt: new Date(),
      authorId: user1.id,
      categories: {
        create: [
          { categoryId: techCategory.id },
          { categoryId: tutorialCategory.id },
        ],
      },
      tags: {
        create: [
          { tagId: tags[3].id }, // Prisma
          { tagId: tags[1].id }, // Node.js
        ],
      },
    },
  });

  const post2 = await prisma.post.create({
    data: {
      title: 'TypeScript Best Practices',
      slug: 'typescript-best-practices',
      excerpt: 'Learn the best practices for writing clean TypeScript code',
      content: `# TypeScript Best Practices

Here are some essential best practices for TypeScript development.

## Use Strict Mode

Enable strict mode in your tsconfig.json for better type safety.

## Avoid Any

Try to avoid using \`any\` type. Use \`unknown\` if you need a dynamic type.

## Use Type Guards

Implement type guards for runtime type checking.`,
      published: true,
      publishedAt: new Date(),
      authorId: user2.id,
      categories: {
        create: [{ categoryId: techCategory.id }],
      },
      tags: {
        create: [{ tagId: tags[0].id }], // TypeScript
      },
    },
  });

  const post3 = await prisma.post.create({
    data: {
      title: 'Building REST APIs with Node.js',
      slug: 'building-rest-apis-nodejs',
      excerpt: 'A comprehensive guide to building RESTful APIs',
      content: `# Building REST APIs with Node.js

Learn how to build scalable REST APIs using Node.js and Express.

## Setup Express

\`\`\`javascript
const express = require('express');
const app = express();
\`\`\`

## Define Routes

Create routes for CRUD operations.

## Add Middleware

Implement authentication, validation, and error handling.`,
      published: false, // Draft post
      authorId: user1.id,
      categories: {
        create: [{ categoryId: tutorialCategory.id }],
      },
      tags: {
        create: [{ tagId: tags[1].id }], // Node.js
      },
    },
  });

  console.log('✅ Created posts');

  // Create notifications
  await prisma.notification.createMany({
    data: [
      {
        userId: user1.id,
        type: 'post_published',
        title: 'Your post was published',
        message: 'Your post "Getting Started with Prisma" is now live!',
        read: false,
      },
      {
        userId: user2.id,
        type: 'post_published',
        title: 'Your post was published',
        message: 'Your post "TypeScript Best Practices" is now live!',
        read: true,
        readAt: new Date(),
      },
    ],
  });

  console.log('✅ Created notifications');

  // Create audit logs
  await prisma.auditLog.createMany({
    data: [
      {
        userId: admin.id,
        action: 'user_created',
        resource: 'User',
        resourceId: user1.id,
        details: { email: user1.email },
      },
      {
        userId: admin.id,
        action: 'user_created',
        resource: 'User',
        resourceId: user2.id,
        details: { email: user2.email },
      },
      {
        userId: user1.id,
        action: 'post_created',
        resource: 'Post',
        resourceId: post1.id,
        details: { title: post1.title },
      },
    ],
  });

  console.log('✅ Created audit logs');

  console.log('\n🎉 Seeding completed successfully!');
  console.log('\n📊 Summary:');
  console.log(`   Users: ${await prisma.user.count()}`);
  console.log(`   Posts: ${await prisma.post.count()}`);
  console.log(`   Categories: ${await prisma.category.count()}`);
  console.log(`   Tags: ${await prisma.tag.count()}`);
  console.log(`   Notifications: ${await prisma.notification.count()}`);
  console.log(`   Audit Logs: ${await prisma.auditLog.count()}`);
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });