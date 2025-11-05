# UI Flows – Legal Analysis Console

## Global Shell

- **Header** – Attorney/client selector + health indicator
- **Tabs** – Research · Documents · Cases · Privileged Chat · Ethics
- **Theme** – Night-mode glassmorphism to align with other blueprint consoles

## Research Flow

1. Attorney enters natural-language question
2. Optional jurisdiction & limit filters applied
3. API call `/api/research`
4. Display: research memo, authority list, ethics tag
5. Secondary panel: `/api/precedents/search` results with citations

## Document Analysis Flow

1. Select document type (contract, brief, etc.)
2. Paste legal text (or attach once upload support lands)
3. Trigger `/api/analyze-document`
4. Present analysis memo, risk table, related templates

## Case Management Flow

1. Create case (title, type, jurisdiction, client)
2. Case list shows status + jurisdiction tags
3. Selecting case sets global `selectedCaseId`
4. Run `/api/cases/{id}/analysis` to populate strategy + precedents
5. Downstream components (Documents tab) receive `caseId`

## Privileged Chat Flow

1. Start session (auto when sending first message)
2. `/api/privileged-chat/session` returns token + expiry
3. Chat composer posts to `/api/privileged-chat`
4. Transcript renders alternating attorney/client bubbles
5. Footer shows session expiry + ethics status

## Ethics Dashboard Flow

1. On load call `/api/ethics/audit?attorneyId=...`
2. Render compliance metrics (score, privilege events, pending disclosures)
3. Extendable for compliance drill-down (future Phase 3)

## Responsive Behaviour

- Two-column grids collapse to single column <768px
- Tab buttons wrap when viewport narrow
- Chat transcript becomes taller at small widths to preserve readability

