/**
 * Fake Data Generator Pattern
 *
 * Lean component (250 LOC) for deterministic fake data generation
 * Source pattern: snaplet/copycat
 *
 * Features:
 * - Deterministic: same input → same output
 * - Type-safe data generation
 * - Realistic faker data
 * - Seeded randomization
 *
 * Usage:
 * ```
 * const user = generate.user('user-123');
 * // Always generates same user for 'user-123'
 * ```
 */

/**
 * Simple hash function for deterministic seed generation
 */
function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

/**
 * Seeded random number generator
 */
class SeededRandom {
  constructor(seed) {
    this.seed = seed % 2147483647;
    if (this.seed <= 0) this.seed += 2147483646;
  }

  next() {
    this.seed = (this.seed * 16807) % 2147483647;
    return (this.seed - 1) / 2147483646;
  }

  int(min, max) {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }

  choice(array) {
    return array[this.int(0, array.length - 1)];
  }
}

/**
 * Data generation helpers
 */
const DATA = {
  firstNames: [
    'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Emma',
    'Robert', 'Olivia', 'William', 'Sophia', 'Alexander', 'Isabella', 'Daniel',
  ],
  lastNames: [
    'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
    'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White',
  ],
  cities: [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
    'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
  ],
  domains: [
    'gmail.com', 'yahoo.com', 'outlook.com', 'example.com', 'test.com',
    'company.com', 'mail.com', 'email.com',
  ],
  streets: [
    'Main St', 'Oak Ave', 'Maple Dr', 'Park Blvd', 'Washington St',
    'Lake Rd', 'Hill Ave', 'Elm St', 'Cedar Ln', 'Pine St',
  ],
  companies: [
    'Tech Corp', 'Global Industries', 'Digital Solutions', 'Innovation Labs',
    'Future Systems', 'Smart Technologies', 'Data Analytics Inc', 'Cloud Services',
  ],
};

/**
 * Fake data generator with deterministic output
 */
class FakeDataGenerator {
  constructor(seed) {
    this.seed = seed;
    this.rng = new SeededRandom(hashCode(String(seed)));
  }

  /**
   * Generate first name
   */
  firstName() {
    return this.rng.choice(DATA.firstNames);
  }

  /**
   * Generate last name
   */
  lastName() {
    return this.rng.choice(DATA.lastNames);
  }

  /**
   * Generate full name
   */
  fullName() {
    return `${this.firstName()} ${this.lastName()}`;
  }

  /**
   * Generate email address
   */
  email(domain) {
    const first = this.firstName().toLowerCase();
    const last = this.lastName().toLowerCase();
    const num = this.rng.int(1, 9999);
    const domainName = domain || this.rng.choice(DATA.domains);

    const formats = [
      `${first}.${last}${num}@${domainName}`,
      `${first}_${last}@${domainName}`,
      `${first}${num}@${domainName}`,
    ];

    return this.rng.choice(formats);
  }

  /**
   * Generate phone number
   */
  phoneNumber() {
    const areaCode = this.rng.int(200, 999);
    const prefix = this.rng.int(200, 999);
    const lineNumber = this.rng.int(1000, 9999);
    return `(${areaCode}) ${prefix}-${lineNumber}`;
  }

  /**
   * Generate address
   */
  address() {
    const number = this.rng.int(1, 9999);
    const street = this.rng.choice(DATA.streets);
    const city = this.rng.choice(DATA.cities);
    const zip = this.rng.int(10000, 99999);

    return {
      street: `${number} ${street}`,
      city,
      state: 'CA',
      zip: String(zip),
      country: 'USA',
    };
  }

  /**
   * Generate company info
   */
  company() {
    return {
      name: this.rng.choice(DATA.companies),
      catchPhrase: 'Innovative solutions for modern problems',
      industry: this.rng.choice(['Technology', 'Finance', 'Healthcare', 'Retail']),
    };
  }

  /**
   * Generate user object
   */
  user() {
    return {
      id: this.seed,
      firstName: this.firstName(),
      lastName: this.lastName(),
      email: this.email(),
      phone: this.phoneNumber(),
      address: this.address(),
      company: this.company().name,
    };
  }

  /**
   * Generate number in range
   */
  int(min, max) {
    return this.rng.int(min, max);
  }

  /**
   * Generate boolean
   */
  boolean() {
    return this.rng.next() > 0.5;
  }

  /**
   * Generate UUID-like string
   */
  uuid() {
    const hex = () => this.rng.int(0, 15).toString(16);
    return `${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}-${hex()}${hex()}${hex()}${hex()}-4${hex()}${hex()}${hex()}-${hex()}${hex()}${hex()}${hex()}-${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}${hex()}`;
  }
}

/**
 * Factory function for generating data
 */
function createGenerator(seed) {
  return new FakeDataGenerator(seed);
}

/**
 * Quick access generators
 */
const generate = {
  user: (seed) => createGenerator(seed).user(),
  email: (seed, domain) => createGenerator(seed).email(domain),
  fullName: (seed) => createGenerator(seed).fullName(),
  phoneNumber: (seed) => createGenerator(seed).phoneNumber(),
  address: (seed) => createGenerator(seed).address(),
  company: (seed) => createGenerator(seed).company(),
  int: (seed, min, max) => createGenerator(seed).int(min, max),
  boolean: (seed) => createGenerator(seed).boolean(),
  uuid: (seed) => createGenerator(seed).uuid(),
};

/**
 * Example usage
 */
if (require.main === module) {
  console.log('=== Fake Data Generator Examples ===\n');

  console.log('User (seed: user-123):');
  console.log(generate.user('user-123'));

  console.log('\nUser (same seed: user-123):');
  console.log(generate.user('user-123')); // Same output

  console.log('\nUser (different seed: user-456):');
  console.log(generate.user('user-456')); // Different output

  console.log('\nEmail:', generate.email('test-email'));
  console.log('Phone:', generate.phoneNumber('test-phone'));
  console.log('UUID:', generate.uuid('test-uuid'));
}

module.exports = {
  FakeDataGenerator,
  createGenerator,
  generate,
};
