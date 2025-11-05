# Express OIDC Provider

Lightweight OpenID Connect provider powered by [`oidc-provider`](https://github.com/panva/node-oidc-provider`).

## Features
- Boots an Express server wrapped around `oidc-provider`
- In-memory account store for quick prototyping (swap for your DB)
- Security middleware (`helmet`) and HTTPS enforcement hook
- Example client configuration and token endpoint

## Installation
```bash
npm install oidc-provider express helmet
```

## Usage
```ts
import { createOIDCServer } from './express-oidc-server';

const server = await createOIDCServer({
  issuer: 'https://auth.example.com',
  clients: [
    {
      client_id: 'web-app',
      client_secret: 'super-secret',
      redirect_uris: ['https://app.example.com/callback'],
      response_types: ['code'],
      grant_types: ['authorization_code']
    }
  ]
});
```

Update the in-memory `AccountStore` to use your user database before production.

## Smoke Test
Run `node tests/smoke.js` to ensure the module exports are available.
