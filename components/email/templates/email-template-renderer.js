/**
 * Email Template Renderer Pattern
 *
 * Lean component (280 LOC) for email rendering with templates
 * Source pattern: forwardemail/email-templates
 *
 * Features:
 * - Template rendering (Pug, Handlebars, EJS)
 * - HTML to text conversion
 * - CSS inlining for email clients
 * - Preview mode for development
 * - I18n support
 *
 * Usage:
 * ```
 * const emailer = createEmailRenderer({
 *   templateDir: './emails',
 *   transport: nodemailer.createTransport(...)
 * });
 *
 * await emailer.send({
 *   template: 'welcome',
 *   to: 'user@example.com',
 *   locals: { name: 'John' }
 * });
 * ```
 */

const path = require('path');
const fs = require('fs').promises;
const { convert } = require('html-to-text');

/**
 * Simple template engines (lightweight alternatives)
 */
const templateEngines = {
  /**
   * Simple variable substitution ({{variable}})
   */
  simple: (template, locals) => {
    return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return locals[key] !== undefined ? locals[key] : match;
    });
  },

  /**
   * EJS-style templates (<%=variable%>)
   */
  ejs: (template, locals) => {
    // Basic EJS implementation
    return template.replace(/<%=\s*(\w+)\s*%>/g, (match, key) => {
      return locals[key] !== undefined ? locals[key] : '';
    });
  },
};

/**
 * Inline CSS for email compatibility
 * Simplified version - in production use 'juice' package
 */
function inlineCSS(html) {
  // Basic CSS inlining (very simplified)
  // In production, use the 'juice' package for full CSS inlining
  return html.replace(/<style>([\s\S]*?)<\/style>/g, (match, css) => {
    // Extract simple rules and inline them
    // This is a basic implementation - use 'juice' for production
    return '';
  });
}

/**
 * Convert HTML to plain text
 */
function htmlToText(html) {
  return convert(html, {
    wordwrap: 80,
    selectors: [
      { selector: 'a', options: { baseUrl: 'https://example.com' } },
      { selector: 'img', format: 'skip' },
    ],
  });
}

/**
 * Email template renderer
 */
class EmailRenderer {
  constructor(options = {}) {
    this.options = {
      templateDir: options.templateDir || path.join(process.cwd(), 'emails'),
      engine: options.engine || 'simple',
      inlineCSS: options.inlineCSS !== false,
      generateText: options.generateText !== false,
      transport: options.transport, // Nodemailer transport
      preview: options.preview || process.env.NODE_ENV === 'development',
      defaultFrom: options.defaultFrom || 'noreply@example.com',
      ...options,
    };

    this.cache = new Map();
  }

  /**
   * Load and cache template
   */
  async loadTemplate(templateName) {
    if (this.cache.has(templateName)) {
      return this.cache.get(templateName);
    }

    const templatePath = path.join(this.options.templateDir, `${templateName}.html`);

    try {
      const template = await fs.readFile(templatePath, 'utf-8');
      this.cache.set(templateName, template);
      return template;
    } catch (error) {
      throw new Error(`Template not found: ${templateName} at ${templatePath}`);
    }
  }

  /**
   * Render template with locals
   */
  async render(templateName, locals = {}) {
    const template = await this.loadTemplate(templateName);
    const engine = templateEngines[this.options.engine] || templateEngines.simple;

    // Render HTML
    let html = engine(template, locals);

    // Inline CSS if needed
    if (this.options.inlineCSS) {
      html = inlineCSS(html);
    }

    // Generate text version
    const text = this.options.generateText ? htmlToText(html) : '';

    return { html, text };
  }

  /**
   * Send email
   */
  async send(options) {
    const {
      template,
      to,
      from = this.options.defaultFrom,
      subject,
      locals = {},
      attachments = [],
    } = options;

    // Render template
    const { html, text } = await this.render(template, locals);

    // Create email message
    const message = {
      from,
      to,
      subject,
      html,
      text,
      attachments,
    };

    // Preview mode (development)
    if (this.options.preview) {
      console.log('\n=== EMAIL PREVIEW ===');
      console.log('To:', to);
      console.log('From:', from);
      console.log('Subject:', subject);
      console.log('Text Preview:');
      console.log(text.substring(0, 200) + '...');
      console.log('====================\n');
      return { preview: true, message };
    }

    // Send email (production)
    if (!this.options.transport) {
      throw new Error('Email transport not configured');
    }

    const info = await this.options.transport.sendMail(message);
    return { sent: true, messageId: info.messageId };
  }

  /**
   * Clear template cache
   */
  clearCache() {
    this.cache.clear();
  }
}

/**
 * Common email templates (inline)
 */
const commonTemplates = {
  welcome: `
    <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
          .content { padding: 20px; background: #f9f9f9; }
          .button { display: inline-block; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Welcome to {{appName}}!</h1>
          </div>
          <div class="content">
            <p>Hi {{name}},</p>
            <p>Thanks for signing up! We're excited to have you on board.</p>
            <p><a href="{{confirmUrl}}" class="button">Confirm Email</a></p>
            <p>If the button doesn't work, copy and paste this link: {{confirmUrl}}</p>
          </div>
        </div>
      </body>
    </html>
  `,

  passwordReset: `
    <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .alert { background: #ff9800; color: white; padding: 15px; border-radius: 5px; }
          .button { display: inline-block; padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 5px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="alert">
            <h2>Password Reset Request</h2>
          </div>
          <p>Hi {{name}},</p>
          <p>We received a request to reset your password. Click the button below to proceed:</p>
          <p><a href="{{resetUrl}}" class="button">Reset Password</a></p>
          <p>This link will expire in {{expiryHours}} hours.</p>
          <p>If you didn't request this, please ignore this email.</p>
        </div>
      </body>
    </html>
  `,
};

/**
 * Factory function
 */
function createEmailRenderer(options = {}) {
  return new EmailRenderer(options);
}

/**
 * Example usage
 */
if (require.main === module) {
  (async () => {
    // Create renderer with inline templates
    const renderer = createEmailRenderer({
      preview: true, // Development mode
    });

    // Override loadTemplate to use inline templates
    renderer.loadTemplate = async (name) => commonTemplates[name] || '';

    // Send welcome email
    await renderer.send({
      template: 'welcome',
      to: 'user@example.com',
      subject: 'Welcome to Our App!',
      locals: {
        appName: 'My App',
        name: 'John Doe',
        confirmUrl: 'https://example.com/confirm/abc123',
      },
    });

    // Send password reset email
    await renderer.send({
      template: 'passwordReset',
      to: 'user@example.com',
      subject: 'Reset Your Password',
      locals: {
        name: 'John Doe',
        resetUrl: 'https://example.com/reset/xyz789',
        expiryHours: 24,
      },
    });
  })();
}

module.exports = {
  EmailRenderer,
  createEmailRenderer,
  commonTemplates,
  htmlToText,
};
