# Reveal.js Presentation Template

A modern, customizable presentation template using Reveal.js with dark theme and variable substitution.

## Overview

This component provides a production-ready presentation template for product pitches, technical demos, or project documentation. Features a clean dark theme with customizable branding and automatic slide navigation.

## Features

- **Modern Design**: Dark theme with customizable accent colors
- **Responsive Layout**: Works on desktop and mobile
- **Variable Substitution**: Template variables for easy customization
- **Full Screen Mode**: Press 'F' to toggle full screen
- **Keyboard Navigation**: Arrow keys, space bar for slides
- **Progress Bar**: Visual progress indicator
- **Slide Numbers**: Automatic slide numbering

## Quick Start

1. Copy `reveal-template.html` to your project
2. Replace template variables with your content:
   - `{{PRODUCT_NAME}}` - Your product/project name
   - `{{PRODUCT_DESCRIPTION}}` - Short description
   - `{{TARGET_AUDIENCE}}` - Who is this for
   - And 20+ more variables

3. Open in browser - no build step required!

## Template Variables

### Basic Info
- `{{PRODUCT_NAME}}` - Product name
- `{{PRODUCT_DESCRIPTION}}` - One-line description
- `{{TARGET_AUDIENCE}}` - Target users

### Problem Section
- `{{PROBLEM_TITLE}}` - Problem statement title
- `{{PROBLEM_DESCRIPTION}}` - Problem description
- `{{PROBLEM_POINTS}}` - List items for challenges
- `{{PROBLEM_QUOTE}}` - Customer quote

### Solution Section
- `{{SOLUTION_TITLE}}` - Solution title
- `{{SOLUTION_DESCRIPTION}}` - How you solve it
- `{{FEATURE_LIST}}` - Key features list

### Market Section
- `{{MARKET_SIZE}}` - TAM/SAM/SOM
- `{{USE_CASES}}` - Use case list

### Features Section
- `{{FEATURE_CARDS_LEFT}}` - Left column features
- `{{FEATURE_CARDS_RIGHT}}` - Right column features

### Benefits Section
- `{{BENEFIT_METRICS}}` - Metrics (e.g., "10x faster")
- `{{USER_BENEFITS}}` - User benefits list
- `{{BUSINESS_BENEFITS}}` - Business benefits list

### Technology Section
- `{{TECH_FRONTEND}}` - Frontend stack
- `{{TECH_BACKEND}}` - Backend stack
- `{{TECH_DATABASE}}` - Database choice
- `{{TECH_INFRASTRUCTURE}}` - Infrastructure

### Roadmap Section
- `{{ROADMAP_PHASE1}}` - MVP phase
- `{{ROADMAP_PHASE2}}` - Growth phase
- `{{NEXT_STEPS}}` - Immediate next steps

### CTA Section
- `{{CTA_DESCRIPTION}}` - Call to action description
- `{{CTA_TITLE}}` - CTA title
- `{{CTA_ACTION}}` - Action text

## Customization

### Colors
Edit CSS variables in the `<style>` section:
```css
:root {
  --background-color: #121212;
  --main-color: #f5f5f5;
  --accent-color: #00c4b4;      /* Primary brand color */
  --secondary-color: #9370DB;    /* Secondary accent */
}
```

### Slides
Add new slides by duplicating a `<section>` block:
```html
<section>
  <h2>Your Title</h2>
  <div class="card">
    <p>Your content</p>
  </div>
</section>
```

## Keyboard Shortcuts

- **Arrow Keys**: Navigate slides
- **Space**: Next slide
- **F**: Toggle fullscreen
- **Esc**: Exit fullscreen/overview
- **O**: Toggle overview mode
- **S**: Speaker notes (if enabled)

## Use Cases

- Product pitches and demos
- Technical presentations
- Project documentation
- Stakeholder updates
- Conference talks
- Internal training

## Token Savings

Using this template vs building from scratch:
- **Tokens Saved**: ~8,000 tokens (Reveal.js setup + styling)
- **Time Saved**: 30-60 minutes
- **Lines of Code**: 295 lines ready to use

## Dependencies

All dependencies loaded via CDN (no npm install):
- Reveal.js 4.5.0
- Reveal.js Highlight plugin
- Inter font (Google Fonts)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Example Usage

See `examples/` folder for complete examples:
- Product pitch deck
- Technical architecture presentation
- MVP demo slides

## Metadata

- **Category**: Documentation
- **Type**: Presentation Template
- **Framework**: Reveal.js
- **Language**: HTML/CSS/JavaScript
- **Complexity**: Low
- **Setup Time**: 5 minutes