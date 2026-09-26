---
name: sales-dimensional-etl-build
description: Build or complete the Enterprise Sales Analytics warehouse schema, SCD-aware dimensional loads, atomic and aggregate facts, orchestration, configuration, backend data interfaces, logging, and implementation tests after the governed build contract is available.
---
# Purpose
Own implementation and integration of the database and data-processing layer for the Enterprise Sales Analytics warehouse while preserving verified working behavior. This includes schema objects, SCD logic, relationship resolution, ETL/ELT, orchestration, configuration, backend data contracts, audit controls, error handling, and developer-level tests.

# When to Use This Skill
Load this skill when Antigravity must create, repair, extend, or validate:
- dimensional DDL and migrations;
- source-to-target transformations;
- Type 0, Type 1, or Type 2 dimension loading;
- bridge, visit fact, atomic sales fact, or monthly aggregate processing;
- incremental loads, reruns, orchestration, control tables, configuration, logging, or data-layer APIs;
- unit/component/integration tests owned by the implementation layer.

# When Not to Use This Skill
- Use `sales-warehouse-design-governance` for requirements analysis, architecture decisions, model changes, ambiguous grain/SCD rules, and implementation planning.
- Use `sales-analytics-quality-release` for dashboard/report assets, end-to-end acceptance, release packaging, deployment execution guidance, and operational documentation.

# Project Context
The target logical model is defined by `requirement.docx` and the approved analysis artifacts. Core objects are `DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`, `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`, `FACT_CUSTOMER_VISIT`, `FACT_SALES_ORDER_LINE`, and `FACT_SALES_MONTHLY_AGG`.

Important rules:
- an order may contain multiple products and multiple order locations;
- multiple business managers may serve the same customer within a division over time, but each order line has one manager;
- fulfillment is allowed only from a manufacturing facility or a warehouse-eligible location;
- fulfillment can occur from a location different from the order location;
- historical dimension versions must be resolved according to the applicable event date;
- the monthly aggregate supports dashboard performance but does not replace the atomic fact.

At initial analysis, no executable implementation or platform selection was available. Reinspect before execution because the repository may have changed.

# Required Files to Read
1. All three `.agents/skills/*/SKILL.md` files.
2. `requirement.docx`.
3. `docs/analysis/project-understanding.md`, `requirements-traceability.md`, `architecture-decisions.md`, `implementation-status.md`, `implementation-backlog.md`, and `handoff-to-build.md`, when present.
4. All discovered schema, migration, stored procedure, transformation, job, service, repository, configuration, environment-template, test, sample-data, and deployment files relevant to the assigned requirement IDs.
5. Existing coding standards, linter/formatter settings, dependency manifests, CI configuration, and README instructions.

# Preconditions
- The planning handoff identifies requirement IDs, acceptance criteria, dependencies, and unresolved blockers.
- Platform and runtime choices required for executable code are evidenced or approved.
- Required source schema/contracts and safe test data are available.
- A rollback or reversible migration approach exists for changes to existing objects.
- Secrets are externally supplied through the project's approved mechanism.

# Responsibilities
This skill exclusively owns:
- physical schema and migration implementation;
- surrogate/business key constraints and indexes;
- dimension, bridge, fact, and aggregate load logic;
- SCD merge/versioning behavior;
- source-to-target transformation and referential resolution;
- incremental processing, idempotency, rerun safety, orchestration, and audit controls;
- implementation-layer configuration, logging, and error handling;
- backend data access or service interfaces if present in the approved design;
- unit, component, and integration tests for the data-processing layer;
- developer documentation for build and local execution.

# Step-by-Step Execution Workflow
1. **Reinspect and baseline.** Inventory the current repository, run existing non-destructive checks, and capture the pre-change state.
2. **Read the handoff.** Map assigned requirement IDs to target files and tests. If grain, platform, source contract, or SCD behavior is unresolved, return that item to `sales-warehouse-design-governance`.
3. **Reuse project patterns.** Determine migration framework, SQL dialect, language, package manager, job framework, configuration pattern, naming, testing, and logging from the repository. Do not introduce a parallel framework.
4. **Implement dimensions in dependency order.** Build `DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, and `DIM_PRODUCT` using defined surrogate keys, business keys, Type 1 attributes, Type 2 effective dating, current flags, and version numbers.
5. **Implement temporal resolution.** Resolve dimension versions using the relevant business event date. Detect missing, duplicate, overlapping, or invalid effective-date ranges.
6. **Implement bridge logic.** Build `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` with customer, division/location, manager, start/end dates, and current flag. Enforce one valid assignment per applicable relationship and time slice unless requirements explicitly allow otherwise.
7. **Implement supporting fact.** Load `FACT_CUSTOMER_VISIT` at customer + visited division + visit date + assisting manager grain, with visit count behavior defined by the requirement.
8. **Implement atomic fact.** Load `FACT_SALES_ORDER_LINE`, retaining order number and line number as degenerate identifiers; resolve order, fulfillment, customer, product, and manager keys; calculate `Gross_Revenue = Quantity * Unit_Price` and `Net_Revenue = Gross_Revenue - Discount_Amount` using approved numeric precision.
9. **Enforce business rules.** Reject or quarantine invalid fulfillment locations, broken manager assignments, unresolved mandatory dimensions, duplicate order lines, negative/invalid measures, and impossible date ranges according to approved rules.
10. **Implement monthly aggregate.** Derive `FACT_SALES_MONTHLY_AGG` from validated atomic facts by month, region, product, and location type. Include total quantity, total net revenue, order-line count, and refresh timestamp. Make refresh repeatable.
11. **Add orchestration and controls.** Implement dependency ordering, watermarks or approved incremental mechanism, run IDs, row counts, reject counts, timestamps, status, retry boundaries, and safe reruns.
12. **Configure securely.** Use environment-specific external configuration and secret references. Provide sanitized templates only.
13. **Test continuously.** Add unit, component, migration, SCD, idempotency, referential, business-rule, and aggregate-reconciliation tests. Run existing tests after each coherent change.
14. **Document changes.** Update technical build instructions, schema/data dictionary, lineage, configuration reference, and test evidence without claiming deployment.
15. **Handoff.** Provide built artifacts and evidence to `sales-analytics-quality-release`.

# Technical Standards
- Follow the discovered SQL dialect, framework, naming, formatting, and repository conventions.
- Use migration-controlled, reviewable, reversible database changes.
- Never rely on physical row order or mutable natural keys as fact foreign keys.
- Enforce one current Type 2 row per business key and non-overlapping effective periods.
- Type 1 changes overwrite only the attributes designated Type 1; Type 2 changes create versions only for designated Type 2 attributes.
- Preserve `9999-12-31` as the current-end convention only if supported by the selected platform and confirmed by the project contract.
- Resolve facts to historical dimension versions valid on the event date, not simply current rows.
- Keep atomic and aggregate loads idempotent. A rerun with unchanged inputs must not duplicate records.
- Use transactions or equivalent atomic mechanisms around matched data changes where supported.
- Use structured logs with run ID, component, stage, severity, record counts, and sanitized error context.
- Do not log credentials, tokens, personal contact values, or complete sensitive source records.
- Validate configuration at startup and fail clearly on absent mandatory settings.

# Decision Rules
1. Follow approved architecture decisions and existing tested project patterns.
2. Prefer set-based transformations and database-native features compatible with the selected platform.
3. Optimize only after correctness and baseline measurement; preserve readable, testable transformations.
4. Do not normalize region into a new dimension unless governance approves it.
5. Do not add a backend/API layer unless existing architecture or approved requirements call for one.
6. For unknown dimension handling, late-arriving facts, deletion semantics, fiscal calendar, currency, or nullability, use only approved decisions; otherwise escalate.
7. Any change to grain, source contract, SCD matrix, or report semantics returns to the governance skill.

# Error-Handling Rules
- Fail fast for invalid configuration, unavailable mandatory dependencies, and incompatible schema versions.
- Separate retryable infrastructure failures from non-retryable data/contract failures.
- Quarantine invalid records with reason code, source identifier, run ID, and timestamp when the approved design permits; never silently discard.
- Roll back incomplete transactional changes; checkpoint only validated stages.
- Make retries bounded and idempotent.
- Preserve the original exception and contextual metadata while redacting secrets and sensitive values.
- Do not continue aggregate refresh after atomic fact validation fails.

# Validation Requirements
- DDL/migrations apply cleanly to a permitted non-production environment and are reversible where required.
- Primary, foreign, unique, check, and temporal constraints conform to the approved model.
- Type 1 updates do not create unnecessary versions.
- Type 2 changes close the prior row and create one current row without overlapping periods.
- Order-line facts contain one row per approved grain and resolve date-valid dimension versions.
- Fulfillment-location eligibility and manager-assignment rules are tested.
- Gross and net revenue formulas reconcile with controlled test cases.
- Monthly aggregates reconcile to atomic facts for identical filters.
- Rerunning unchanged input produces no duplicates or unintended history.
- Automated tests and static checks pass; any skipped test has an explicit reason and owner.

# Expected Outputs
Paths must follow the discovered project structure. Typical outputs include:
- schema/migration scripts for dimensions, bridge, facts, control, audit, and reject objects;
- transformation or backend source code;
- orchestration/job definitions;
- safe configuration templates;
- unit, component, migration, and integration tests;
- sample or fixture data without secrets;
- schema/data dictionary and lineage updates;
- build/run instructions;
- implementation and test evidence for handoff.

# Completion Criteria
- All assigned requirement IDs are implemented or explicitly blocked.
- No existing passing behavior is regressed.
- Database objects, loads, incremental behavior, reruns, error paths, and audit controls are tested.
- Atomic and aggregate data reconcile.
- Security scanning or available secret checks show no introduced secret.
- Changed files and commands are documented.
- Release skill receives deployable artifacts and evidence.

# Handoff to Other Skills
- **Next:** `sales-analytics-quality-release` after implementation tests pass.
- Pass changed-file manifest, schema version, migration order, configuration keys without values, run commands, test commands/results, sample dataset description, known limitations, rollback instructions, and requirement traceability updates.
- Return to `sales-warehouse-design-governance` for unresolved architecture, grain, source-contract, SCD, or scope decisions.
- Accept defect returns from `sales-analytics-quality-release` with reproducible inputs, expected versus actual results, logs, and failing requirement IDs.

# Prohibited Actions
- Do not alter approved grain or metric semantics without governance.
- Do not hardcode credentials or production endpoints.
- Do not modify production data or execute destructive operations without explicit authorization.
- Do not create duplicate frameworks, pipelines, services, or schema objects.
- Do not bypass migrations with undocumented manual changes.
- Do not weaken constraints or tests merely to make a run pass.
- Do not create dashboard/report or release-owner artifacts except implementation-facing documentation.
- Do not leave TODO, TBD, stub, or placeholder implementations.

# Final Response Format
Report:
1. assigned requirement IDs completed;
2. files created, modified, or deleted;
3. schema/migration order;
4. transformation and SCD behavior implemented;
5. configuration changes without secret values;
6. commands executed;
7. tests and results;
8. data reconciliation evidence;
9. issues, assumptions, and blockers;
10. rollback notes;
11. handoff package and next skill.

# Final Checklist
- [ ] Current repository and handoff read
- [ ] Existing patterns reused
- [ ] Migrations safe and ordered
- [ ] Dimensions and SCD logic validated
- [ ] Bridge and facts validated at declared grain
- [ ] Business rules enforced
- [ ] Incremental reruns are idempotent
- [ ] Logs and errors are sanitized
- [ ] Tests pass with evidence
- [ ] Release handoff complete
