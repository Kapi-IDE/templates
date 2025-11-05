# Deterministic Fake Data Generator (Node.js)

Seeded faker utilities for generating repeatable test data.

## Install
```bash
npm install dayjs
```

## Usage
```js
const { generate } = require('./fake-data-generator');

const user = generate.user('user-123'); // always the same output
const org = generate.organization('org-456');
```

Use deterministic seeds (`generate.user(<seed>)`) to create stable fixtures across test runs.
