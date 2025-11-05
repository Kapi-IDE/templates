/**
 * OIDC Provider Pattern - Express Implementation
 *
 * Lean component (150 LOC) demonstrating OAuth/OIDC server setup
 * Source pattern: node-oidc-provider
 *
 * Features:
 * - OpenID Connect provider setup
 * - Account management
 * - Security headers (helmet)
 * - Production-ready HTTPS enforcement
 *
 * Usage:
 * ```
 * const app = createOIDCServer({
 *   issuer: 'https://auth.example.com',
 *   clients: [{
 *     client_id: 'web-app',
 *     client_secret: 'secret',
 *     redirect_uris: ['https://app.example.com/callback']
 *   }]
 * });
 * ```
 */

import express from 'express';
import helmet from 'helmet';
import { Provider } from 'oidc-provider';

/**
 * Simple in-memory account store
 * Replace with database in production
 */
class AccountStore {
  constructor() {
    this.accounts = new Map();
  }

  async findAccount(ctx, id) {
    const account = this.accounts.get(id) || {
      accountId: id,
      async claims() {
        return {
          sub: id,
          email: `user${id}@example.com`,
          email_verified: true,
        };
      },
    };
    return account;
  }

  addAccount(id, data) {
    this.accounts.set(id, {
      accountId: id,
      ...data,
    });
  }
}

/**
 * Create OIDC Provider configuration
 */
function createOIDCConfig(options = {}) {
  const accountStore = new AccountStore();

  return {
    // Account lookup
    findAccount: accountStore.findAccount.bind(accountStore),

    // Supported features
    features: {
      devInteractions: { enabled: false },
      deviceFlow: { enabled: true },
      revocation: { enabled: true },
    },

    // Client configuration
    clients: options.clients || [
      {
        client_id: 'default-client',
        client_secret: 'client-secret',
        redirect_uris: ['http://localhost:3000/callback'],
        grant_types: ['authorization_code', 'refresh_token'],
        response_types: ['code'],
      },
    ],

    // Token configuration
    ttl: {
      AccessToken: 60 * 60, // 1 hour
      AuthorizationCode: 10 * 60, // 10 minutes
      IdToken: 60 * 60, // 1 hour
      RefreshToken: 14 * 24 * 60 * 60, // 14 days
    },

    ...options.config,
  };
}

/**
 * Setup security headers
 */
function setupSecurity(app) {
  const directives = helmet.contentSecurityPolicy.getDefaultDirectives();
  delete directives['form-action'];

  app.use(
    helmet({
      contentSecurityPolicy: {
        useDefaults: false,
        directives,
      },
    })
  );
}

/**
 * HTTPS redirect middleware (production only)
 */
function httpsRedirect(req, res, next) {
  if (req.secure) {
    next();
  } else if (req.method === 'GET' || req.method === 'HEAD') {
    res.redirect(
      `https://${req.get('host')}${req.originalUrl}`
    );
  } else {
    res.status(400).json({
      error: 'invalid_request',
      error_description: 'HTTPS required',
    });
  }
}

/**
 * Create OIDC server with Express
 *
 * @param {Object} options - Configuration options
 * @param {string} options.issuer - OIDC issuer URL
 * @param {Array} options.clients - Client configurations
 * @param {number} options.port - Server port
 * @param {boolean} options.production - Production mode
 * @returns {Object} { app, provider, server }
 */
export function createOIDCServer(options = {}) {
  const {
    issuer = process.env.ISSUER || 'http://localhost:3000',
    port = process.env.PORT || 3000,
    production = process.env.NODE_ENV === 'production',
  } = options;

  const app = express();
  const config = createOIDCConfig(options);

  // Security setup
  setupSecurity(app);

  // Production config
  if (production) {
    app.enable('trust proxy');
    app.use(httpsRedirect);
  }

  // Create OIDC provider
  const provider = new Provider(issuer, config);
  if (production) {
    provider.proxy = true;
  }

  // Mount OIDC routes
  app.use(provider.callback());

  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({ status: 'ok', issuer });
  });

  // Start server
  const server = app.listen(port, () => {
    console.log(`OIDC Provider running on port ${port}`);
    console.log(`Well-known config: ${issuer}/.well-known/openid-configuration`);
  });

  return { app, provider, server };
}

/**
 * Example usage
 */
if (import.meta.url === `file://${process.argv[1]}`) {
  createOIDCServer({
    issuer: 'http://localhost:3000',
    clients: [
      {
        client_id: 'demo-app',
        client_secret: 'demo-secret',
        redirect_uris: ['http://localhost:8080/callback'],
        grant_types: ['authorization_code', 'refresh_token'],
        response_types: ['code'],
      },
    ],
  });
}
