# Week 1 Foundation Freeze

Last updated: 2026-04-28

## 1) Scope Lock (MVP)
Included in MVP:
- Student records and guardian mapping
- Attendance marking and class-date retrieval
- Fees heads, structures, student assignment, invoice and receipt basics
- Minimal audit logging of critical write actions

Explicitly not included in MVP:
- Advanced analytics and dashboards
- Automation workflows and notifications
- Multi-campus complexity

## 2) Roles and Governance (Initial)
- Teacher: module operations in assigned scope
- HM/Principal: oversight and approvals where policy needs checks
- Super Admin: unrestricted configuration and emergency overrides

## 3) Core Data Model (Frozen Contract)
Master and foundational entities added:
- AcademicYear
- Section (under Class)
- Guardian
- Student
- StudentGuardian
- AttendanceSession
- AttendanceEntry
- FeeHead
- FeeStructure
- FeeStructureItem
- StudentFeeAssignment
- FeeInvoice
- FeeReceipt
- AuditLog

## 4) Key Constraints
- Section uniqueness: per class
- Student uniqueness: admission_no
- Attendance uniqueness: one session per class+section+year+date
- Attendance entry uniqueness: one record per student per session
- Fee structure uniqueness: name+class+year
- Fee assignment uniqueness: student+structure+year
- Invoice and receipt numbers are unique

## 5) Week 1 Build Sequence
1. Freeze scope and model contract (this document)
2. Add ORM models and migration
3. Apply migration in local and verify
4. Scaffold API routers in next slice
5. Add RBAC guards + audit helper in route layer

## 6) Open Decisions (Keep Minimal)
- Invoice numbering strategy (simple serial vs formatted serial)
- Receipt numbering strategy (simple serial vs formatted serial)
- Whether section is mandatory for all classes

Until decided, keep implementations configurable and simple.
