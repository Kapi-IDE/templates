const serverModule = require('../payment-intent-server');

if (typeof serverModule.createPaymentServer !== 'function') {
  throw new Error('createPaymentServer export missing');
}

if (typeof serverModule.createPaymentIntent !== 'function') {
  throw new Error('createPaymentIntent export missing');
}

console.log('Stripe payment module exports verified.');
