# DVM ERP Strategy and Execution Plan

Last updated: 2026-04-28

## 1) Purpose
This document is the operating guide for day-to-day execution and long-term delivery.
It keeps scope tight, prevents drift, and ensures we ship MVP by the deadline.

## 2) MVP North Star (Target: 2026-06-20)
Deliver a stable, usable school ERP MVP with only:
- Student module (core student records)
- Attendance module (daily marking and basic views)
- Fees module (heads, structures, assignments, receipts)
- Essential reports only

Out of scope until post-MVP:
- Nice-to-have UX enhancements
- Deep analytics dashboards
- Advanced automation workflows

## 3) Execution Principles
- Ship in vertical slices: schema -> API -> minimal UI -> test.
- One source of truth: this file + active todo list.
- No uncontrolled feature additions before MVP.
- Every change must be testable and rollback-friendly.
- Keep migrations clean and reproducible.

## 4) Day-to-Day Goals (Operating Rhythm)
Use this section daily.

### Daily Start (15-20 min)
- Confirm today’s top 1-3 deliverables.
- Check blockers from previous day.
- Validate branch, migration head, and environment health.
- Lock the day’s scope before coding.

### Daily Build Block
- Complete one vertical slice end-to-end.
- Prefer small commits with clear intent.
- Keep backend tests and frontend build green.

### Daily Close (15 min)
- Record completed items and carry-forward items.
- Note defects, risks, and decisions.
- Update next day’s exact target.

## 5) Weekly Goals (Until MVP)

### Week 1: Foundation and Scope Freeze
- Freeze module scope and role rules.
- Define core ERP data model.
- Implement master data migrations.
- Add RBAC permission matrix scaffolding.
- Add audit logging base.

### Week 2: Student Module
- Student CRUD APIs.
- Guardian mapping basics.
- Minimal student management UI.
- Validation and list filters.

### Week 3: Attendance Module
- Attendance session and entry APIs.
- Marking and class-date views.
- Minimal attendance UI flow.
- Basic attendance reporting endpoints.

### Week 4: Fees Module + Stabilization
- Fee head and structure APIs.
- Student fee assignment, invoice, receipt basics.
- Minimal fees UI.
- UAT fixes, hardening, and deployment prep.

## 6) Long-Term Goals (Post-MVP)
- Expand reports (collections, dues, attendance trends).
- Add stronger audit and approval analytics.
- Improve parent-facing communication workflows.
- Introduce role-specific dashboards by usage patterns.
- Performance optimization and operational observability.

## 7) Definition of Done (Per Feature)
A feature is done only when all are true:
- Migration applied successfully in local and server.
- API contracts finalized and validated.
- Minimum UI flow works for target role.
- Tests added/updated and passing.
- Edge cases and permission checks verified.
- Documentation updated (this file and relevant README sections).

## 8) Risks and Controls
- Risk: scope creep.
  - Control: no new MVP features without explicit trade-off.
- Risk: migration drift.
  - Control: check alembic head before merge and deploy.
- Risk: approval bottlenecks.
  - Control: concise pending change summaries and reviewer visibility.
- Risk: deadline compression.
  - Control: prioritize function over polish until MVP freeze.

## 9) Daily Log Template
Copy this block each day:

## YYYY-MM-DD
### Top Goals
- 
- 
- 

### Completed
- 

### Blockers
- 

### Decisions
- 

### Next Day Focus
- 

## 10) Current Immediate Priorities
- Finalize Week 1 data model decisions.
- Implement master data migrations.
- Add RBAC hooks on new ERP routes.
- Add audit base table and write hooks.
