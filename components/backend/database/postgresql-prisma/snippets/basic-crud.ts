// Basic CRUD Operations with Prisma

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// CREATE - Single record
async function createUser() {
  const user = await prisma.user.create({
    data: {
      email: 'user@example.com',
      name: 'John Doe',
      passwordHash: 'hashed_password',
      role: 'USER',
    },
  });
  console.log('Created user:', user);
  return user;
}

// CREATE - Multiple records
async function createManyUsers() {
  const result = await prisma.user.createMany({
    data: [
      { email: 'user1@example.com', name: 'User 1', passwordHash: 'hash1' },
      { email: 'user2@example.com', name: 'User 2', passwordHash: 'hash2' },
      { email: 'user3@example.com', name: 'User 3', passwordHash: 'hash3' },
    ],
    skipDuplicates: true, // Skip if email already exists
  });
  console.log(`Created ${result.count} users`);
  return result;
}

// READ - Find unique
async function findUserByEmail(email: string) {
  const user = await prisma.user.findUnique({
    where: { email },
  });
  console.log('Found user:', user);
  return user;
}

// READ - Find first match
async function findFirstAdmin() {
  const admin = await prisma.user.findFirst({
    where: { role: 'ADMIN' },
    orderBy: { createdAt: 'asc' },
  });
  console.log('First admin:', admin);
  return admin;
}

// READ - Find many with filters
async function findActiveUsers() {
  const users = await prisma.user.findMany({
    where: {
      deletedAt: null, // Not soft-deleted
      role: {
        in: ['USER', 'EDITOR'], // Role is USER or EDITOR
      },
    },
    orderBy: {
      createdAt: 'desc',
    },
    take: 10, // Limit 10
  });
  console.log(`Found ${users.length} active users`);
  return users;
}

// READ - Count records
async function countUsers() {
  const total = await prisma.user.count();
  const admins = await prisma.user.count({
    where: { role: 'ADMIN' },
  });
  console.log(`Total users: ${total}, Admins: ${admins}`);
  return { total, admins };
}

// UPDATE - Single record
async function updateUserName(userId: string, newName: string) {
  const user = await prisma.user.update({
    where: { id: userId },
    data: { name: newName },
  });
  console.log('Updated user:', user);
  return user;
}

// UPDATE - Many records
async function promoteEditors() {
  const result = await prisma.user.updateMany({
    where: { role: 'EDITOR' },
    data: { role: 'MODERATOR' },
  });
  console.log(`Promoted ${result.count} editors to moderators`);
  return result;
}

// UPSERT - Update or create
async function upsertUser(email: string, name: string) {
  const user = await prisma.user.upsert({
    where: { email },
    update: { name }, // Update if exists
    create: {
      // Create if doesn't exist
      email,
      name,
      passwordHash: 'default_hash',
    },
  });
  console.log('Upserted user:', user);
  return user;
}

// DELETE - Single record
async function deleteUser(userId: string) {
  const user = await prisma.user.delete({
    where: { id: userId },
  });
  console.log('Deleted user:', user);
  return user;
}

// DELETE - Many records
async function deleteInactiveUsers() {
  const result = await prisma.user.deleteMany({
    where: {
      deletedAt: {
        not: null, // Soft-deleted users
      },
    },
  });
  console.log(`Deleted ${result.count} inactive users`);
  return result;
}

// SOFT DELETE - Mark as deleted
async function softDeleteUser(userId: string) {
  const user = await prisma.user.update({
    where: { id: userId },
    data: { deletedAt: new Date() },
  });
  console.log('Soft deleted user:', user);
  return user;
}

// SELECT specific fields
async function getUserEmails() {
  const users = await prisma.user.findMany({
    select: {
      id: true,
      email: true,
      name: true,
      // Don't include passwordHash
    },
  });
  console.log('User emails:', users);
  return users;
}

// PAGINATION
async function getPaginatedUsers(page: number = 1, pageSize: number = 10) {
  const skip = (page - 1) * pageSize;

  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip,
      take: pageSize,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.user.count(),
  ]);

  const totalPages = Math.ceil(total / pageSize);

  console.log(`Page ${page}/${totalPages} (${users.length} users)`);

  return {
    users,
    pagination: {
      page,
      pageSize,
      total,
      totalPages,
      hasNext: page < totalPages,
      hasPrev: page > 1,
    },
  };
}

// Example usage
async function main() {
  console.log('--- CRUD Examples ---\n');

  // Create
  const user = await createUser();

  // Read
  await findUserByEmail(user.email);
  await findActiveUsers();

  // Update
  await updateUserName(user.id, 'Jane Doe');

  // Pagination
  await getPaginatedUsers(1, 5);

  // Count
  await countUsers();

  // Soft delete
  await softDeleteUser(user.id);
}

// Run examples
main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());

export {
  createUser,
  createManyUsers,
  findUserByEmail,
  findActiveUsers,
  updateUserName,
  deleteUser,
  softDeleteUser,
  getPaginatedUsers,
};