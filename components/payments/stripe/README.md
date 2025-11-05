# Stripe Payment Intent Server

Express server pattern that creates Payment Intents, verifies webhooks, and demonstrates Stripe Tax integration.

## Install
```bash
npm install express stripe body-parser
```

## Usage
```js
const { createPaymentServer } = require('./payment-intent-server');

createPaymentServer({
  stripeSecretKey: process.env.STRIPE_SECRET_KEY,
  webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
  port: 4242,
});
```

Endpoints:
- `POST /create-payment-intent`
- `POST /webhook`
- `GET /config`
- `GET /health`

## Smoke Test
Run `node tests/smoke.js` to verify exports without hitting Stripe.
