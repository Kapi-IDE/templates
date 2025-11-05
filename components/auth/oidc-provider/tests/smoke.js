const provider = require('../express-oidc-server');

if (typeof provider.createOIDCServer !== 'function') {
  throw new Error('createOIDCServer export missing');
}

console.log('OIDC provider module looks good.');
