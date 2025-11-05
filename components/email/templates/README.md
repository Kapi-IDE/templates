# Email Template Renderer (Node.js)

Simple renderer for HTML email templates with support for text fallbacks and CSS inlining.

## Install
```bash
npm install html-to-text juice nodemailer
```

## Usage
```js
const { createEmailRenderer } = require('./email-template-renderer');
const renderer = createEmailRenderer({ templateDir: './emails' });

await renderer.send({
  template: 'welcome',
  transport: nodemailer.createTransport({...}),
  to: 'user@example.com',
  locals: { name: 'Jane' }
});
```

Template engines supported: simple `{{variable}}`, Handlebars-style sections, or direct HTML.
