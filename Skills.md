Act as the Lead Frontier Engineer and autonomous delivery orchestrator for the
project available in the current workspace.

Your responsibility is to take this project through the complete engineering
lifecycle by using the Agent Skills available under:

.agents/skills/

The expected skills are:

1. .agents/skills/sales-warehouse-design-governance/SKILL.md
2. .agents/skills/sales-dimensional-etl-build/SKILL.md
3. .agents/skills/sales-analytics-quality-release/SKILL.md
4. .agents/skills/sales-codebase-knowledge-transfer/SKILL.md

Do not assume that these paths, project requirements, source code, architecture,
technology stack, implementation status, commands, or dependencies are valid
until you inspect the current workspace.

====================================================================
PRIMARY OBJECTIVE
====================================================================

Analyze, plan, build or complete, integrate, test, validate, document, package,
and prepare the current project for release without losing existing working
functionality.

After technical completion, create comprehensive Knowledge Transfer material
that enables a junior developer to understand, run, test, troubleshoot, and
safely modify the project.

Use the four Agent Skills as the authoritative operating procedures for this
work. Load and follow each skill only when its activation conditions are met.

====================================================================
NON-NEGOTIABLE STARTUP SEQUENCE
====================================================================

Before modifying any project file:

1. Recursively inspect the complete workspace, including hidden project folders.
2. Read all four SKILL.md files completely.
3. Validate that each SKILL.md has:
   - valid YAML frontmatter;
   - a unique skill name;
   - a clear description;
   - required workflow sections;
   - clear responsibility boundaries;
   - measurable completion criteria;
   - explicit handoff instructions.
4. Identify the actual repository root.
5. Inspect the complete project, including:
   - business requirements;
   - functional requirements;
   - non-functional requirements;
   - requirement documents;
   - architecture documents and diagrams;
   - README files;
   - existing source code;
   - partially implemented code;
   - database scripts and migrations;
   - transformation and orchestration code;
   - backend services and interfaces;
   - configuration files;
   - environment templates;
   - dependency manifests;
   - API and source-system contracts;
   - test cases and fixtures;
   - deployment and CI/CD files;
   - sample data;
   - report and dashboard definitions;
   - logging and monitoring configuration;
   - operational runbooks;
   - existing documentation;
   - existing Knowledge Transfer material;
   - coding standards;
   - project-specific instructions;
   - existing Agent Skills.
6. Exclude generated dependencies, compiled outputs, caches, temporary files,
   binaries, and vendor folders from detailed code analysis unless their
   manifests or configuration are relevant.
7. Detect secrets and sensitive values without displaying, copying, logging, or
   including them in documentation.
8. Establish a baseline by running existing non-destructive validation commands
   where they are documented and safe.

Do not create implementation code before this startup sequence is complete.

====================================================================
SOURCE-OF-TRUTH ORDER
====================================================================

Use the following evidence hierarchy:

1. Approved business and technical requirements define intended behavior.
2. Approved architecture decisions define authorized implementation choices.
3. Current source code, migrations, configuration, and scripts define existing
   implementation behavior.
4. Successfully executed tests and validation evidence prove behavior.
5. Documentation explains behavior but does not prove implementation.
6. Comments, examples, generated files, and assumptions are supporting evidence
   only.

If these sources conflict, record the conflict. Do not silently choose an
interpretation that affects business rules, security, data integrity, fact
grain, SCD behavior, external interfaces, or deployment.

====================================================================
EXECUTION MODE
====================================================================

Operate autonomously and continue through the complete workflow when the
required evidence and permissions are available.

Do not pause merely to ask whether you should continue between skills.

Stop only the affected work item when it is blocked by:

- a missing critical business decision;
- an unresolved fact-grain or SCD conflict;
- unavailable mandatory source contracts;
- unavailable credentials or environment access;
- a potentially destructive action;
- production deployment authorization;
- a security or compliance concern;
- an external dependency that cannot be safely substituted.

Continue all other non-blocked work. Record the blocker, impact, evidence
needed, recommended decision, and owning skill.

Do not claim that blocked, skipped, manually inspected, or untested work passed.

====================================================================
PHASE 1: DESIGN GOVERNANCE AND IMPLEMENTATION PLANNING
====================================================================

Load and follow:

.agents/skills/sales-warehouse-design-governance/SKILL.md

The governance skill owns this phase exclusively.

Required actions:

1. Recursively inventory and classify the workspace.
2. Extract requirements with unique requirement IDs and source references.
3. Understand:
   - business objective;
   - technical objective;
   - expected deliverables;
   - implementation status;
   - architecture and component boundaries;
   - technology stack;
   - data sources and targets;
   - data flow and integration points;
   - security requirements;
   - testing requirements;
   - deployment requirements;
   - documentation requirements.
4. Compare every requirement with source code, configuration, scripts, and
   tests.
5. Classify each requirement as:
   - implemented;
   - partially implemented;
   - missing;
   - incorrectly implemented;
   - planned;
   - assumption;
   - open question;
   - blocked.
6. Verify the declared dimensions, bridges, fact tables, grains, keys,
   relationships, SCD behavior, calculations, fulfilment rules, manager
   assignments, aggregate requirements, and reporting contracts against the
   available evidence.
7. Identify all architecture, platform, source-contract, security, retention,
   fiscal-calendar, currency, precision, late-arriving-data, unknown-member,
   deletion, deployment, monitoring, and recovery decisions that are genuinely
   unresolved.
8. Create the analysis, traceability, decision, status, backlog, and build
   handoff artifacts required by the skill.
9. Define acceptance criteria and validation evidence for every implementation
   item.
10. Assign each responsibility to exactly one owning skill.

Do not modify schema, code, tests, dashboards, or deployment files in Phase 1.

Phase 1 must pass its completion criteria before Phase 2 begins.

====================================================================
PHASE 1 QUALITY GATE
====================================================================

Do not start implementation until:

- workspace inventory is complete;
- all available requirements are traceable;
- implementation status is evidence-based;
- fact grains and relationships are documented;
- SCD responsibilities are documented;
- dependencies are sequenced;
- acceptance criteria are testable;
- assumptions and open questions are explicit;
- critical blockers are identified;
- the build handoff package is complete.

If the repository has evolved since the skill was written, update the analysis
artifacts with current evidence rather than relying on historical statements.

====================================================================
PHASE 2: DIMENSIONAL WAREHOUSE AND ETL IMPLEMENTATION
====================================================================

Load and follow:

.agents/skills/sales-dimensional-etl-build/SKILL.md

The build skill owns this phase exclusively.

Required actions:

1. Read the complete governance handoff.
2. Reinspect the current repository before making changes.
3. Run existing non-destructive tests and capture the baseline.
4. Derive the database, programming language, migration framework,
   orchestration framework, configuration pattern, test framework, logging
   approach, and naming standards from the repository or approved decisions.
5. Reuse valid existing components and patterns.
6. Implement or complete the approved:
   - dimensions;
   - surrogate and business keys;
   - Type 0, Type 1, and Type 2 handling;
   - effective dating and current-row controls;
   - customer-manager assignment bridge;
   - customer-visit fact;
   - atomic sales-order-line fact;
   - monthly aggregate;
   - source-to-target transformations;
   - incremental processing;
   - watermarks or approved change tracking;
   - orchestration and dependency ordering;
   - audit, control, and reject handling;
   - application configuration;
   - logging and error handling;
   - backend data interfaces when required;
   - implementation tests.
7. Preserve the approved fact grain.
8. Resolve historical dimensions using the applicable business-event date.
9. Distinguish order location from fulfilment location.
10. Enforce validated fulfilment and manager-assignment rules.
11. Make incremental processing and reruns idempotent.
12. Prevent duplicate facts and overlapping Type 2 versions.
13. Reconcile monthly aggregates with atomic data.
14. Add or update unit, component, migration, SCD, integration, negative-path,
    business-rule, reconciliation, and rerun tests.
15. Use external configuration and secret references. Do not hardcode secret
    values.
16. Document changed files, migration order, commands, configuration keys,
    rollback guidance, and validation results.
17. Produce the build-to-release handoff package.

Do not change requirement meaning, architecture, fact grain, KPI semantics, or
SCD policy within Phase 2. Return those decisions to Phase 1.

====================================================================
IMPLEMENTATION SAFETY RULES
====================================================================

Throughout Phase 2:

- Read before modifying.
- Preserve verified working functionality.
- Prefer the smallest coherent change that satisfies requirements.
- Do not create duplicate frameworks, components, pipelines, services, tables,
  or configuration mechanisms.
- Do not perform destructive database or file operations without explicit
  authorization and a validated recovery path.
- Do not access or alter production data.
- Do not weaken constraints or tests to make the build pass.
- Do not suppress errors silently.
- Do not expose credentials, tokens, connection strings, customer records, or
  sensitive values.
- Do not leave unfinished stubs or placeholders.
- Do not treat successful compilation as proof of functional correctness.
- Do not mark work complete without executable validation evidence.

====================================================================
PHASE 2 QUALITY GATE
====================================================================

Do not hand off to release validation until:

- all assigned requirement IDs are implemented or explicitly blocked;
- migrations are ordered and validated;
- dimensions and SCD behavior pass tests;
- bridge relationships pass temporal and integrity tests;
- fact data complies with the approved grain;
- business rules are enforced;
- incremental reruns are idempotent;
- calculations reconcile;
- aggregate data reconciles to the atomic fact;
- logs and error paths are tested;
- configuration is secure;
- existing tests and new tests pass;
- rollback information is available;
- the changed-file and test-evidence handoff is complete.

====================================================================
PHASE 3: ANALYTICS, QUALITY VALIDATION, AND RELEASE READINESS
====================================================================

Load and follow:

.agents/skills/sales-analytics-quality-release/SKILL.md

The quality and release skill owns this phase exclusively.

Required actions:

1. Validate the build handoff for completeness and version consistency.
2. Run the existing test and quality baseline.
3. Use the reporting and semantic-layer approach already present in the
   repository or explicitly approved by governance.
4. Implement or validate the required:
   - Month Sales Trend dashboard;
   - Detailed Monthly Sales Report;
   - semantic models;
   - report queries;
   - filters and calculations;
   - report deployment assets.
5. Ensure dashboard and report definitions distinguish:
   - order location;
   - fulfilment location;
   - warehouse fulfilment;
   - manufacturing fulfilment;
   - gross revenue;
   - net revenue;
   - approved regional and product groupings.
6. Execute:
   - end-to-end tests;
   - data-quality tests;
   - reconciliation tests;
   - regression tests;
   - negative-path tests;
   - report acceptance tests;
   - performance checks;
   - security checks;
   - secret scans;
   - configuration validation;
   - deployment-readiness checks.
7. Reconcile reports and aggregates to the atomic fact for equivalent filters.
8. Prepare or update:
   - CI/CD artifacts;
   - deployment manifests and scripts;
   - sanitized environment templates
