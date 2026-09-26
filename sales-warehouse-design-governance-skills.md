
---
name: sales-warehouse-design-governance
description: Analyze and govern the Enterprise Sales Analytics dimensional-warehouse requirements, produce an evidence-based implementation plan and traceability baseline, and resolve model or scope decisions before schema, ETL, reporting, testing, or deployment work begins.
---
# Purpose
Own requirements interpretation, architecture governance, dimensional-model consistency, implementation planning, and requirement-to-artifact traceability for the Enterprise Sales Analytics Data Warehouse. This skill establishes the approved build contract. It does not implement database objects, pipelines, dashboards, or deployment artifacts.

# When to Use This Skill
Load this skill when Antigravity must:
- begin or resume the project;
- inspect the workspace and determine scope, stack, status, gaps, or conflicts;
- translate `requirement.docx` into an implementation-ready backlog;
- validate dimensional grain, keys, relationships, SCD ownership, business rules, and cross-component contracts;
- assess a proposed change that could affect multiple tables, ETL jobs, reports, tests, or deployment;
- reconcile requirements with existing code before modification.

# When Not to Use This Skill
- Use `sales-dimensional-etl-build` to create or modify schemas, SQL, seed data, ETL/ELT jobs, orchestration, configuration, or backend data services.
- Use `sales-analytics-quality-release` to create reports/dashboard assets, automated validation, release packaging, deployment runbooks, and operational documentation.

# Project Context
The available workspace contains `requirement.docx` and no source code, configuration, database scripts, tests, deployment files, README, or existing Agent Skills at analysis time. Treat implementation status as **planned, not implemented**, until a fresh recursive inspection finds executable evidence.

The requirement defines an enterprise sales analytical warehouse using Kimball-style dimensional design and SCD handling. It describes:
- atomic sales order-line analysis, customer visits, and a monthly aggregate;
- conformed dimensions for date, location, customer, business manager, and product;
- a customer-manager assignment bridge;
- reporting by customer, product, location, location type, region, manufacturing/warehouse fulfillment, and business manager;
- Type 0, Type 1, and Type 2 attribute behavior;
- multi-product orders, multiple order locations, multiple managers within a division, one manager per order line, and fulfillment only from manufacturing or warehouse-eligible locations.

Authoritative logical entities are `DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`, `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`, `FACT_CUSTOMER_VISIT`, `FACT_SALES_ORDER_LINE`, and `FACT_SALES_MONTHLY_AGG`. `DIM_REGION` is mentioned only as an optional future normalization and must not be created without an approved decision.

Known analytical outputs are a Month Sales Trend dashboard and a Detailed Monthly Sales Report. The dashboard requires revenue and quantity trends, location, warehouse, manufacturing, regional rollups, and month-over-month revenue. The detailed report requires customer name, order date, total quantity, total revenue, sales location, location type, and business manager name.

# Required Files to Read
Before any work:
1. Recursively list the workspace, including hidden folders, while excluding generated dependency/vendor folders from content review.
2. Read `requirement.docx` in full, including screenshots, tables, diagrams, headers, and footers.
3. Read any subsequently available README, architecture decision records, data dictionaries, API contracts, source files, SQL, migrations, configuration, environment templates, tests, sample data, CI/CD, deployment manifests, and existing `SKILL.md` files.
4. Read all three files under `.agents/skills/` to preserve boundaries and handoffs.
5. If a referenced file is missing, record it in the gap register. Do not infer its contents.

# Preconditions
- The repository root is accessible.
- `requirement.docx` is readable.
- No implementation action starts until the workspace inventory and requirements/code comparison are complete.
- Any technology/platform selection not evidenced in the workspace is recorded as an open decision.

# Responsibilities
This skill exclusively owns:
- workspace inventory and evidence classification;
- project understanding and requirement extraction;
- current-state versus target-state assessment;
- requirement IDs and traceability matrix;
- logical architecture and component boundaries;
- dimensional grain, relationship, and SCD decision validation;
- implementation backlog, dependency sequence, assumptions, risks, and open questions;
- change-impact analysis and preservation rules.

# Step-by-Step Execution Workflow
1. **Inventory first.** Recursively enumerate all files. Classify each as requirement, architecture, source, schema, ETL, configuration, test, sample data, deployment, documentation, skill, generated dependency, or unknown.
2. **Extract evidence.** Read textual and visual content. Record each requirement with source path and section/image/table reference. Never treat a document statement as proof of implementation.
3. **Establish status.** For each requirement, classify `implemented`, `partially implemented`, `missing`, `incorrect`, `planned`, `assumption`, or `open question`. Require code/configuration/test evidence for any implemented status.
4. **Confirm grains.** Preserve these declared grains unless an approved correction is documented:
   - `FACT_SALES_ORDER_LINE`: order number + order line number + product + order location + fulfillment location + business manager + order date, using surrogate relationships to dimensions.
   - `FACT_CUSTOMER_VISIT`: customer + division visited + visit date + business manager who assisted.
   - `FACT_SALES_MONTHLY_AGG`: month + region + product + location type.
5. **Validate relationship rules.** Model product and location multiplicity at the line grain. Use `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` for customer-to-manager assignments by division/location and effective period. Do not put multi-valued manager lists in dimensions.
6. **Validate SCD policy.** Date is Type 0. Location, customer, business manager, and product contain the Type 1/Type 2 attributes specified by the requirement. Region follows the documented mixed strategy and remains a decision topic if normalization is proposed.
7. **Identify contradictions.** Record naming, datatype, nullable-key, SCD, fiscal-calendar, platform, orchestration, security, SLA, retention, and deployment ambiguities. Do not silently resolve business ambiguity.
8. **Produce the build contract.** Create or update project analysis, requirement traceability, architecture decisions, implementation backlog, and handoff package in the repository's established documentation location. If none exists, use `docs/analysis/`.
9. **Gate implementation.** Mark items `ready` only when required inputs, acceptance criteria, dependencies, and validation method are explicit.
10. **Handoff.** Pass the approved build contract to `sales-dimensional-etl-build`; pass reporting requirements and acceptance measures to `sales-analytics-quality-release`.

# Technical Standards
- Use Kimball dimensional modeling and conformed dimensions as stated in the requirement.
- Preserve atomic fact grain. Do not combine order header and order line logic.
- Use surrogate keys for dimensions and fact relationships; retain applicable business keys and degenerate dimensions.
- Resolve SCD versions using the business event date, especially order date for customer, product, location, and manager history.
- Preserve auditability through load timestamps, effective dates, end dates, current flags, and version numbers where specified.
- Treat region as an attribute of location unless a documented decision approves `DIM_REGION`.
- Do not select a database, language, scheduler, cloud platform, BI tool, or deployment target without repository evidence or an explicit decision.
- Never include credentials, tokens, connection strings with secrets, personal data, or production values in skills or analysis artifacts.

# Decision Rules
1. Requirement evidence outranks comments, generated files, or inferred conventions.
2. Working, tested repository patterns outrank new patterns unless they conflict with requirements or security.
3. Prefer the smallest change that satisfies the requirement and preserves compatibility.
4. If multiple approaches are equivalent, choose the one consistent with the discovered stack and document the decision.
5. If a choice affects grain, history, security, external contracts, or destructive migration, stop that item and record an open decision rather than inventing an answer.
6. Missing platform details remain unresolved; downstream skills must parameterize or wait for an approved selection.

# Error-Handling Rules
- If a file cannot be read, record path, error, impact, and fallback inspection attempted.
- If requirements conflict, cite both statements and create a decision entry; do not choose silently.
- If implementation evidence is absent, classify the feature as missing or planned.
- If secrets are discovered, do not reproduce them; record only file path and remediation need.
- If path references are invalid, search by exact filename and then by distinctive terms before marking missing.

# Validation Requirements
- Every requirement has a unique ID, source reference, owner skill, status, acceptance evidence, and dependency.
- Every implemented claim links to code/configuration plus a validation result.
- Fact grains, dimensions, bridge relationships, SCD rules, reporting fields, security, testing, and deployment needs are covered.
- All referenced paths exist at validation time or are explicitly marked planned.
- The three skill responsibilities are mutually exclusive and collectively complete.

# Expected Outputs
Unless the project defines alternatives:
- `docs/analysis/project-understanding.md`
- `docs/analysis/workspace-inventory.md`
- `docs/analysis/requirements-traceability.md`
- `docs/analysis/implementation-status.md`
- `docs/analysis/architecture-decisions.md`
- `docs/analysis/implementation-backlog.md`
- `docs/analysis/handoff-to-build.md`

# Completion Criteria
- Full workspace inventory completed.
- Requirements extracted and traceable.
- Current implementation status supported by evidence.
- Grains, keys, relationships, SCD ownership, integrations, and report contracts documented.
- No unresolved critical ambiguity is hidden.
- Build backlog is ordered, testable, and assigned to an owning skill.
- Handoff package enables implementation without rereading this original user prompt.

# Handoff to Other Skills
- **Next:** `sales-dimensional-etl-build` after the build contract is ready.
- Pass requirement IDs, target entities, grains, source-to-target rules, SCD matrix, decision log, dependency order, and unresolved blockers.
- Provide `sales-analytics-quality-release` with dashboard/report contracts, metric definitions, expected data-quality checks, and non-functional acceptance criteria.
- Return work to this skill when a discovered implementation constraint changes grain, scope, SCD behavior, cross-component contracts, or architecture decisions.

# Prohibited Actions
- Do not implement or modify application code, SQL, schemas, pipelines, tests, dashboards, or deployment artifacts.
- Do not invent source schemas, sample values, platform choices, SLAs, fiscal rules, security roles, or operational procedures.
- Do not mark documentation-only items as implemented.
- Do not expose or copy secrets.
- Do not delete, rename, or destructively migrate existing artifacts.
- Do not create a fourth skill.

# Final Response Format
Report:
1. analysis summary;
2. stack evidenced versus undecided;
3. implementation-status counts by classification, only when exact counts are available;
4. artifacts created or changed;
5. decisions made with evidence;
6. assumptions and open questions;
7. blockers and risks;
8. validation performed and results;
9. handoff target and required next action.

# Final Checklist
- [ ] Workspace recursively inspected
- [ ] Requirements read, including visuals
- [ ] Code and configuration compared with requirements
- [ ] Grains and SCD rules verified
- [ ] Status and traceability recorded
- [ ] Assumptions and open questions explicit
- [ ] No project implementation changed
- [ ] Build and release handoffs prepared
