# Frontend UI/UX Redesign Design

Date: 2026-05-13

## Scope

Redesign the existing `frontend` Vue application across both user-facing areas:

- Public lesson browsing: `/`, `/class/:classId`, `/class/:classId/:subjectId`, `/chapter/:chapterId`
- Authenticated portal: `/portal`, chapter edit, upload, class/subject/user/audit management screens

This phase is UI/UX-focused. It will not change backend contracts, routing semantics, auth rules, or lesson data models unless a small frontend-only adapter is needed to present existing data cleanly.

Reference mockup:

- `.superpowers/brainstorm/frontend-uiux-20260513/content/frontend-redesign-proposal.html`
- Local preview during design review: `http://localhost:55978/frontend-redesign-proposal.html`

## Design Direction

Use one shared product design system for the whole lesson platform.

The current frontend has two competing visual modes: colorful public cards and a dense portal table. The redesign should unify them into a calm school workspace: navy and gold brand color, white/soft-gray surfaces, compact controls, clean typography, and predictable layout rhythm.

The public side should feel approachable and academic, not like a marketing landing page. The portal should feel operational and efficient, not decorative.

## Recommended Approach

Use Approach A from the mockup: design-system refresh.

This means:

- Keep Vue, Vue Router, Pinia, and the current API layer.
- Introduce shared CSS tokens and reusable shell/control/table/card styles.
- Redesign public browsing and portal screens together so they feel like one platform.
- Avoid a large component architecture rewrite unless a screen is already too tangled to style safely.

This is the best balance of visible improvement, implementation risk, and maintainability.

## Information Architecture

### Public Lesson Browser

The public path should remain browse-first:

1. Home: brand header, concise platform title, search affordance, class grid.
2. Class page: class title, subject grid/list, clear chapter counts.
3. Subject chapter list: breadcrumb, subject title, searchable/scan-friendly chapter list.
4. Chapter detail: structured reading page with chapter summary, concepts, learning outcomes, exhibits, media, and PDF action.

The public side should not introduce a marketing homepage, fake stats, or unrelated school sections. The first screen remains the usable lesson browser.

### Portal

The portal should become a persistent workspace:

1. Left sidebar for primary admin/teacher navigation.
2. Top bar for page title, current user, role, account actions.
3. Content region with page-specific toolbars, metrics, tables, forms, and dialogs.
4. Consistent action placement across chapter, class, subject, user, upload, and audit screens.

The portal should prioritize scanning and repeated work: filtering, approving, editing, deleting, and reviewing records.

## Layout System

### Public Shell

- Keep a public top strip for address/phone, but simplify visual weight.
- Use a white main nav with logo, platform name, and minimal navigation.
- Replace oversized gradient hero blocks with a cleaner two-column intro on desktop and single-column intro on mobile.
- Replace highly saturated class gradients with compact, consistent class tiles.
- Use list/card hybrids for chapter lists, with strong title hierarchy and restrained metadata.

### Portal Shell

- Replace the single horizontal navy navbar with a two-part app shell:
  - Dark navy sidebar for navigation.
  - White top bar for page context and user actions.
- Keep content width fluid and work-focused.
- Use cards only for metrics, form panels, modals, and repeated content groups.
- Tables remain tables. Do not convert management views into card grids.

### Responsive Behavior

- Public pages should collapse to single-column layouts below tablet width.
- Portal sidebar should collapse into a top navigation or drawer on mobile.
- Tables should use horizontal scroll where data density requires it, and compact row layouts where practical.
- Buttons and filters must not wrap into unreadable clusters.

## Visual System

### Colors

Use a restrained DVM palette:

- Navy: primary brand, sidebar, major actions.
- Blue: focus states, links, secondary actions.
- Gold: primary creation actions and brand accent.
- Soft gray: page backgrounds and table headers.
- White: surfaces.
- Green/amber/red: status colors only.

Avoid dominant purple gradients, multi-color class cards, and heavy decorative backgrounds.

### Typography

- Use the existing Inter/system stack.
- Use tighter, smaller type for portal controls and table rows.
- Use clear public-page headings without oversized hero-scale typography.
- Avoid negative letter spacing and viewport-scaled text.
- Standardize labels, table headers, buttons, helper text, and badges.

### Components

Create or standardize these component families:

- App shells: `PublicShell`, `PortalShell`
- Navigation: public nav, portal sidebar, mobile nav
- Buttons: primary, secondary, danger, ghost, icon button
- Inputs: search, select, text input, textarea
- Badges: approved, pending, role, count, PDF
- Tables: header, row, action cell, empty/loading/error states
- Cards: metric cards, class tiles, subject cards, chapter cards
- Modal and form sections

Use existing components where possible, but normalize their styling through shared classes/tokens.

## Screen Designs

### Home

The home page should show:

- DVM brand and lesson platform identity.
- A concise title: browse lesson plans by class, subject, and chapter.
- A search affordance only if it can be backed by currently loaded data. Phase 1 should not add a new global search API. If true global search would require backend work, replace the home search with a simple "Choose your class" control.
- A compact class grid with consistent tiles.

The home page should not use decorative waves or heavy gradient class cards.

### Subject Dashboard

The class page should show:

- Breadcrumb back to Home.
- Class title.
- Subject grid using consistent white tiles.
- Subject icon, subject name, chapter count, and clear click target.

Subject colors may appear as small top borders or accents, not full-card color themes.

### Chapter List

The chapter list should show:

- Breadcrumb and subject context.
- Optional search/filter row if the data is available locally.
- Chapter rows/cards with title, aim preview, sessions, concept count, PDF availability, and view action.

Rows should be compact enough for teachers to scan many chapters.

### Chapter Detail

The detail page should become a structured reading surface:

- Header with breadcrumb, chapter title, subject/class metadata, sessions/concepts, PDF action.
- Concepts as well-spaced content sections.
- Learning outcomes as prominent callouts.
- Integration, library, activity, life lesson, remarks as structured subsections.
- Exhibits/media presented consistently, with modal behavior retained if useful.

Avoid huge decorative hero panels that push actual lesson content too far down.

### Portal Dashboard

The portal landing should show:

- Page title: Chapter workspace.
- Summary metrics: total chapters, pending approval, concept count, PDF readiness or similar available metrics.
- Filter/search toolbar.
- Chapter table with approval status and action controls.

Existing admin actions should move into sidebar navigation instead of a long row of buttons. The sidebar must only show pages the current role can access.

### Management Screens

Class, subject, user, upload, and audit screens should adopt the same portal shell and controls:

- Page header with title and primary action.
- Toolbar for filters/search where relevant.
- Tables for list management.
- Consistent modals/forms.
- Shared loading, empty, error, and success states.

## Interaction Design

- Keep current click paths and routes.
- Add clear hover/focus states on interactive controls.
- Keep destructive actions visually distinct and confirmation-based.
- Use icon buttons for compact row actions only if labels or tooltips make intent clear.
- Preserve keyboard focus visibility.
- Modals should be centered, scroll safely on small screens, and have clear cancel/save actions.

## Data Flow

Use the existing API calls in each view. No backend changes are planned.

Frontend improvements may include:

- Local computed summaries for portal metrics from loaded chapter data.
- Local search/filter state where API data is already present.
- Shared helpers for subject labels, status labels, and count formatting.

Do not introduce new data dependencies unless the current endpoint already returns the required fields.

## Error, Empty, and Loading States

Standardize these states:

- Loading: compact spinner or skeleton within the relevant panel.
- Error: bordered alert with retry action where applicable.
- Empty: clear message and next action if the user has permission.
- Disabled actions: visible disabled state with no layout shift.

These states must be consistent across public and portal screens.

## Accessibility

- Use semantic headings and landmarks.
- Keep color contrast high on navy, gold, and status badges.
- Do not rely on color alone for approval status.
- Ensure table headers, form labels, modal titles, and buttons are screen-reader friendly.
- Use visible focus states for links, buttons, selects, inputs, and modal controls.

## Implementation Boundaries

In scope:

- CSS design tokens and shared utility/component styles.
- Public shell redesign.
- Portal shell redesign.
- Home, class, chapter list, chapter detail visual refresh.
- Portal, upload, class management, subject management, user management, audit screens visual refresh.
- Reusable Vue components only where they reduce duplication or improve clarity.

Out of scope:

- Backend API changes.
- New auth model.
- Replacing Vue or routing.
- Full ERP app redesign under `erp/`.
- Website redesign under `website/`.
- Telegram bot changes.

## Testing and Verification

Implementation should be verified with:

- `npm run build` in `frontend`.
- Browser review of public flow: Home -> Class -> Subject -> Chapter.
- Browser review of portal flow: Login -> Portal -> Edit/Add modal or representative management screen.
- Desktop and mobile viewport screenshots.
- Visual comparison against the accepted mockup direction.

The implementation should not be called complete until the major screens match the agreed design direction in layout, density, palette, typography, and interaction behavior.

## Decisions

- Phase 1 covers both public lesson browsing and portal.
- Recommended approach is a design-system refresh, not a full framework rewrite.
- Phase 1 does not add a new global search API.
- Portal navigation only shows role-available pages.
