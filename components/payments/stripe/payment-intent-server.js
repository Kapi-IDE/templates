/**
 * Stripe Payment Intent Pattern
 *
 * Lean component (200 LOC) for Stripe payment processing
 * Source pattern: stripe-samples
 *
 * Features:
 * - Payment Intent creation
 * - Webhook handling with signature verification
 * - Tax calculation (optional)
 * - Automatic payment methods
 *
 * Usage:
 * ```
 * const paymentServer = createPaymentServer({
 *   stripeSecretKey: process.env.STRIPE_SECRET_KEY,
 *   webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
 * });
 * ```
 */

const express = require('express');
const stripe = require('stripe');

/**
 * Calculate tax using Stripe Tax API
 */
async function calculateTax(stripeClient, orderAmount, currency, address) {
  const taxCalculation = await stripeClient.tax.calculations.create({
    currency,
    customer_details: {
      address: address || {
        line1: '123 Main St',
        city: 'San Francisco',
        state: 'CA',
        postal_code: '94111',
        country: 'US',
      },
      address_source: 'shipping',
    },
    line_items: [
      {
        amount: orderAmount,
        reference: 'ProductRef',
        tax_behavior: 'exclusive',
        tax_code: 'txcd_30011000', // General merchandise
      },
    ],
  });

  return taxCalculation;
}

/**
 * Create payment intent
 */
async function createPaymentIntent(stripeClient, options = {}) {
  const {
    amount,
    currency = 'usd',
    calculateTax: shouldCalculateTax = false,
    metadata = {},
    customer,
  } = options;

  let finalAmount = amount;
  let paymentIntentData = {
    currency,
    amount: finalAmount,
    automatic_payment_methods: { enabled: true },
    metadata,
  };

  // Optional: Calculate tax
  if (shouldCalculateTax && options.address) {
    const taxCalculation = await calculateTax(
      stripeClient,
      amount,
      currency,
      options.address
    );
    finalAmount = taxCalculation.amount_total;
    paymentIntentData.amount = finalAmount;
    paymentIntentData.metadata.tax_calculation = taxCalculation.id;
  }

  // Optional: Attach customer
  if (customer) {
    paymentIntentData.customer = customer;
  }

  const paymentIntent = await stripeClient.paymentIntents.create(paymentIntentData);

  return paymentIntent;
}

/**
 * Handle Stripe webhook events
 */
function handleWebhookEvent(event) {
  const handlers = {
    'payment_intent.succeeded': (paymentIntent) => {
      console.log(`✅ Payment succeeded: ${paymentIntent.id}`);
      // TODO: Fulfill order, update database, send confirmation email
      return { status: 'fulfilled', paymentIntent };
    },

    'payment_intent.payment_failed': (paymentIntent) => {
      console.log(`❌ Payment failed: ${paymentIntent.id}`);
      // TODO: Notify customer, log failure
      return { status: 'failed', paymentIntent };
    },

    'charge.succeeded': (charge) => {
      console.log(`💰 Charge succeeded: ${charge.id}`);
      return { status: 'charged', charge };
    },

    'customer.created': (customer) => {
      console.log(`👤 Customer created: ${customer.id}`);
      return { status: 'customer_created', customer };
    },
  };

  const handler = handlers[event.type];
  if (handler) {
    return handler(event.data.object);
  }

  console.log(`⚠️  Unhandled event type: ${event.type}`);
  return { status: 'unhandled', type: event.type };
}

/**
 * Create Stripe payment server
 *
 * @param {Object} options - Configuration
 * @param {string} options.stripeSecretKey - Stripe secret key
 * @param {string} options.webhookSecret - Webhook signing secret
 * @param {number} options.port - Server port
 * @returns {Object} { app, stripeClient, server }
 */
function createPaymentServer(options = {}) {
  const {
    stripeSecretKey = process.env.STRIPE_SECRET_KEY,
    webhookSecret = process.env.STRIPE_WEBHOOK_SECRET,
    publishableKey = process.env.STRIPE_PUBLISHABLE_KEY,
    port = process.env.PORT || 4242,
  } = options;

  if (!stripeSecretKey) {
    throw new Error('STRIPE_SECRET_KEY is required');
  }

  const stripeClient = stripe(stripeSecretKey, {
    apiVersion: '2023-10-16',
  });

  const app = express();

  // Raw body for webhook signature verification
  app.use(
    express.json({
      verify: (req, res, buf) => {
        if (req.originalUrl.startsWith('/webhook')) {
          req.rawBody = buf.toString();
        }
      },
    })
  );

  // Serve static files (optional)
  if (options.staticDir) {
    app.use(express.static(options.staticDir));
  }

  // Health check
  app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'stripe-payment-server' });
  });

  // Get publishable key
  app.get('/config', (req, res) => {
    res.json({ publishableKey });
  });

  // Create payment intent
  app.post('/create-payment-intent', async (req, res) => {
    try {
      const paymentIntent = await createPaymentIntent(stripeClient, req.body);

      res.json({
        clientSecret: paymentIntent.client_secret,
        id: paymentIntent.id,
      });
    } catch (error) {
      console.error('Payment Intent creation error:', error);
      res.status(400).json({
        error: error.message,
      });
    }
  });

  // Webhook endpoint
  app.post('/webhook', async (req, res) => {
    const sig = req.headers['stripe-signature'];

    try {
      // Verify webhook signature
      const event = stripeClient.webhooks.constructEvent(
        req.rawBody,
        sig,
        webhookSecret
      );

      // Handle the event
      const result = handleWebhookEvent(event);

      res.json({ received: true, ...result });
    } catch (err) {
      console.error(`⚠️  Webhook signature verification failed:`, err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }
  });

  // Start server
  const server = app.listen(port, () => {
    console.log(`💳 Stripe payment server running on port ${port}`);
  });

  return { app, stripeClient, server };
}

/**
 * Example usage
 */
if (require.main === module) {
  createPaymentServer({
    port: 4242,
  });
}

module.exports = {
  createPaymentServer,
  createPaymentIntent,
  handleWebhookEvent,
  calculateTax,
};
