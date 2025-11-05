# Recipe: Create Reveal.js Slides for Vision Decks

**Backwards Build Phase**: Sync (communicate the vision) → Code (assemble deliverable)

## 1. Purpose
Provide a repeatable workflow for generating a ready-to-open Reveal.js HTML presentation that reflects the latest product vision. Uses the component at `templates/components/documentation/reveal-presentation/`.

## 2. Inputs
- Source narrative (`future/docs_ide/01-overview/vision.md` or equivalent)
- Brand assets (logos, colors) if needed
- Reveal component files (`reveal-template.html`, `README.md`, `metadata.yaml`)

## 3. Workflow

### Step 1 — Extract Narrative Highlights (Spec → Sync)
1. Read the current `vision.md` document.
2. Summarize key sections: Problem, Solution, Market, Roadmap, CTA.
3. Map bullet points to slide variables (see table below).

| Vision Section | Template Variable |
|----------------|-------------------|
| Vision headline | `{{PRODUCT_NAME}}`, `{{PRODUCT_DESCRIPTION}}` |
| Target audience | `{{TARGET_AUDIENCE}}` |
| Problem bullets | `{{PROBLEM_POINTS}}` |
| Solution pillars | `{{FEATURE_LIST}}`, `{{USER_BENEFITS}}` |
| Market context | `{{MARKET_SIZE}}`, `{{USE_CASES}}` |
| Technology stance | `{{TECH_FRONTEND}}`, `{{TECH_BACKEND}}`, `{{TECH_INFRASTRUCTURE}}` |
| Roadmap | `{{ROADMAP_PHASE1}}`, `{{ROADMAP_PHASE2}}`, `{{NEXT_STEPS}}` |
| Call to action | `{{CTA_TITLE}}`, `{{CTA_ACTION}}`, `{{CTA_DESCRIPTION}}` |

### Step 2 — Populate Template (Code)
1. Copy `templates/components/documentation/reveal-presentation/reveal-template.html` into the target docs folder (e.g., `future/docs_ide/01-overview/vision-slides.html`).
2. Replace template variables with content extracted in Step 1. Use a global search/replace or a templating script.
3. Update brand colors in the `<style>` section if necessary.
4. Optionally embed logos/screenshots by adding `<img>` tags within relevant slides.

### Step 3 — Validate Output (Test)
1. Open the HTML locally (`open vision-slides.html`) and cycle through slides.
2. Confirm: text fits, no placeholders remain, navigation works.
3. Share preview link (commit to docs repo or publish to static hosting) for stakeholder review.

### Step 4 — Publish (Sync)
1. Attach the HTML (and supporting assets) to the weekly Sync deliverables.
2. Document the update in release notes / Slack summary.
3. Archive previous versions in `vision-slides/{timestamp}/` if historical tracking is required.

## 4. Automation Notes
- Autogen script can read `vision.md`, fill variables via `jinja`/`mustache`, and write HTML.
- Quality baseline checks: ensure no template tokens (`{{...}}`) remain before publishing.
- Consider adding CI step that renders slides and uploads screenshots for visual diffing.

## 5. References
- Component README: `templates/components/documentation/reveal-presentation/README.md`
- Backwards Build alignment: spec → architecture (vision document), code (deck assembly), sync (stakeholder review).
- Vision source: `future/docs_ide/01-overview/vision.md`
