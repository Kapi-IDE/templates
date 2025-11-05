# Next.js Landing Page Starter

LaunchCanvas is a production-ready marketing site built with the Next.js App Router and Tailwind CSS. It ships with a polished hero, feature highlights, testimonial grid, stats panel, and call-to-action block so you can drop in your copy and deploy immediately.

## Features
- App Router structure with metadata and structured-data examples
- Responsive dark UI built entirely with Tailwind utilities
- Reusable React components for hero, feature grid, testimonials, CTA, and modal waitlist form
- Sticky navigation and SEO-friendly metadata configuration
- MIT licensed so agencies and founders can adapt freely

## Getting Started
```bash
npm install
npm run dev
```

Then open `http://localhost:3000` to view the starter. Update the component copy in `components/` and metadata in `app/page.tsx` to align with your product.

## Deployment
This blueprint runs anywhere Next.js is supported (Vercel, Netlify, Render, custom Node hosting). For a zero-config deployment:
```bash
npm run build
npm start
```

## Structure
```
app/
  layout.tsx        Root layout + global styles
  page.tsx          Landing page with sections
  styles/globals.css
components/
  *.tsx             Reusable UI blocks
public/             (optional assets)
```

Customize the `CallToAction` component with your waitlist or signup endpoint and connect the modal form to your marketing automation stack.
