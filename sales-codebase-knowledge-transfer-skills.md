---
name: sales-codebase-knowledge-transfer
description: Create and maintain complete, beginner-friendly knowledge-transfer material for the Enterprise Sales Analytics codebase after implementation changes, and validate that a junior developer can understand, run, trace, troubleshoot, test, and safely modify the solution.
---
# Purpose
Own project knowledge transfer and junior-developer enablement. Convert the implemented Enterprise Sales Analytics solution into accurate, code-grounded explanations, walkthroughs, diagrams, runbooks, examples, exercises, and reverse-KT evidence without changing production behavior.

# When to Use This Skill
Load this skill when Antigravity must:
- explain the completed or partially completed codebase to a junior developer;
- create or refresh KT documentation after architecture, schema, ETL, backend, reporting, configuration, test, or deployment changes;
- document how data moves from source through dimensions, bridges, facts, aggregates, reports, and operations;
- create setup, execution, debugging, testing, troubleshooting, support, or safe-change guides;
- prepare KT sessions, hands-on exercises, knowledge checks, reverse KT, or onboarding evidence;
- reduce dependency on undocumented tribal knowledge.

# When Not to Use This Skill
- Use `sales-warehouse-design-governance` for requirement interpretation, architecture decisions, fact grain, SCD policy, scope, or implementation planning.
- Use `sales-dimensional-etl-build` to create or repair schemas, migrations, ETL, orchestration, backend interfaces, configuration, logging, or implementation tests.
- Use `sales-analytics-quality-release` for report completion, independent acceptance tests, deployment packaging, operational readiness, or release decisions.
- Do not use this skill to redesign or refactor working code merely to simplify documentation.

# Project Context
The project is an Enterprise Sales Analytics Data Warehouse. Its governed design may include `DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`, `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`, `FACT_CUSTOMER_VISIT`, `FACT_SALES_ORDER_LINE`, and `FACT_SALES_MONTHLY_AGG`, plus implementation, reporting, testing, configuration, deployment, and operational assets discovered in the current repository.

The codebase may evolve after this skill is created. Therefore, repository files and validated handoff artifacts are the source of truth. Requirements describe intended behavior, but code, configuration, migrations, tests, and execution evidence establish what is actually implemented.

The intended reader is a junior developer who may know basic programming and SQL but may not yet understand dimensional modeling, SCD processing, temporal relationships, ETL orchestration, environment configuration, reporting reconciliation, or project-specific conventions. Explain these concepts in plain language first, then connect them to exact files, functions, classes, jobs, tables, commands, and tests.

# Required Files to Read
Before generating or updating KT material, inspect:
1. All four `.agents/skills/*/SKILL.md` files.
2. `requirement.docx` and all approved files under `docs/analysis/`.
3. README files, architecture decisions, diagrams, data dictionaries, mappings, lineage, coding standards, and change logs.
4. All relevant source-code directories, SQL, migrations, stored procedures, transformation models, orchestration, backend services, report definitions, and semantic models.
5. Dependency manifests, build files, environment templates, configuration schemas, container files, CI/CD, infrastructure, and deployment manifests.
6. Unit, component, integration, data-quality, end-to-end, regression, and report tests plus fixtures and sample data.
7. Logging, monitoring, alerting, runbooks, incident guidance, known-issues lists, and release evidence.
8. The latest handoffs from the governance, build, and quality/release skills.
9. Existing KT guides, onboarding materials, session notes, recordings indexes, FAQs, trackers, and reverse-KT evidence.

Never document a file, command, component, interface, or behavior before verifying it in the current workspace.

# Preconditions
- The repository is accessible and can be recursively inspected.
- The scope and target repository revision are identified.
- Required software and safe local/test access needed to validate commands are available, or missing prerequisites are documented.
- Relevant implementation is stable enough to explain; incomplete or blocked functionality is labelled accurately.
- No secret values are required in KT outputs.

# Responsibilities
This skill exclusively owns:
- beginner-friendly project and business-context explanation;
- repository navigation and module-purpose guide;
- architecture, component interaction, and data-flow walkthroughs grounded in code;
- file-by-file and execution-path explanations for important implementation areas;
- dimensional-model, SCD, bridge, fact, aggregate, reporting, and orchestration teaching material;
- local setup, configuration, build, run, test, debug, and troubleshooting instructions;
- safe-change guides for common maintenance scenarios;
- glossary, FAQ, known-issues catalogue, and learning roadmap;
- KT agenda, tracker, hands-on labs, knowledge checks, reverse-KT tasks, and sign-off evidence;
- documentation freshness checks after project changes.

# Step-by-Step Execution Workflow
1. **Inventory the current repository.** Capture the revision when available. Exclude generated vendor/dependency folders from narrative review, but record their manifests and purpose.
2. **Read before explaining.** Trace requirements to implementation and distinguish implemented, partial, missing, incorrect, planned, assumed, and unresolved behavior.
3. **Identify the learner journey.** Order content from business purpose to architecture, repository map, data model, data flow, execution, testing, debugging, changes, deployment awareness, and operations.
4. **Build a repository map.** For every important folder and entry point, describe purpose, owner skill, dependencies, inputs, outputs, and when a junior developer should modify it. Do not create noise by documenting generated files line by line.
5. **Explain architecture in layers.** Cover sources, ingestion, staging if present, dimensions, temporal SCD processing, bridge resolution, visits, atomic order-line facts, monthly aggregates, semantic/reporting components, tests, configuration, deployment, logging, and monitoring. Include source-controlled diagrams using the project's existing diagram format; if none exists, use Mermaid in Markdown.
6. **Trace end-to-end examples.** Select verified sample records or fixtures and show how one customer, product, order line, manager assignment, order location, and fulfillment location move through the system. Never invent production data. Clearly label synthetic examples.
7. **Explain important code.** For each critical file, function, procedure, model, class, or job, cover: why it exists, inputs, outputs, dependencies, main branches, failure paths, idempotency, logs, tests, and safe extension points. Use short excerpts only when needed; prefer references to exact paths and symbols.
8. **Teach project-specific concepts.** Explain surrogate keys, business keys, grain, conformed dimensions, Type 0/1/2 behavior, effective dating, current flags, temporal joins, degenerate dimensions, bridge tables, aggregate reconciliation, watermarks, reruns, rejects, and audit controls using actual implementation examples.
9. **Document setup and execution.** Provide copy-ready commands for prerequisites, configuration, database initialization, migrations, builds, local runs, pipeline runs, report refreshes, tests, linting, and cleanup only after validating each command where possible. Use placeholders for secret values and explain where secrets come from without exposing them.
10. **Create debugging and troubleshooting guidance.** Map common symptoms to logs, likely components, safe diagnostic commands, expected evidence, escalation conditions, and recovery procedures. Do not state an unverified root cause as fact.
11. **Create safe-change playbooks.** Include verified procedures for common changes such as adding a dimension attribute, changing an SCD-classified attribute, onboarding a source column, changing a business rule, adding a metric, updating a report, correcting a mapping, and adding a test. Require impact analysis and regression validation.
12. **Create hands-on learning.** Provide beginner-to-intermediate exercises using safe data, expected outcomes, hints, validation steps, and cleanup. Include at least one trace exercise, one SCD exercise, one failed-load diagnosis, one reconciliation exercise, and one safe code change when the implemented project supports them.
13. **Create knowledge validation.** Produce knowledge-check questions with answers, practical demonstrations, a reverse-KT checklist, and competency levels: learning, supervised execution, and independent execution.
14. **Review with evidence.** Check every path, symbol, command, query, screenshot reference, diagram edge, and stated behavior against the repository. Run documentation examples in a safe environment where possible.
15. **Publish without modifying behavior.** Store KT outputs in the existing documentation location. If none exists, use `knowledge-transfer/`. Update a KT index and change log. Do not alter application behavior as part of this skill.
16. **Handoff findings.** Route code defects to `sales-dimensional-etl-build`, requirement or architecture ambiguity to `sales-warehouse-design-governance`, and release/runbook discrepancies to `sales-analytics-quality-release`.

# Technical Standards
- Write for a junior developer: plain language first, precise terminology second, and code-grounded examples third.
- Expand acronyms on first use and maintain a project glossary.
- Use progressive disclosure: quick start, conceptual overview, detailed walkthrough, advanced notes, and references.
- Every non-trivial behavior must reference an exact repository path and, where possible, a symbol, object, job, or test name.
- Clearly differentiate business requirement, architecture decision, implemented behavior, example, recommendation, assumption, and open question.
- Keep diagrams source-controlled and editable. Diagrams must match current code and configuration.
- Use consistent naming from the repository; do not create aliases that confuse learners.
- Commands must state working directory, prerequisites, expected result, and safe failure/recovery action.
- Example configuration must contain placeholders, never working credentials or sensitive values.
- Code examples must preserve project style and should be minimal, executable, and tied to a learning objective.
- Avoid unexplained large code dumps. Explain intent, flow, and decisions rather than translating every line into prose.
- Link tests to the behavior they prove and describe how to interpret failures.
- Maintain version/revision metadata, last-validated date when available, and the change that triggered the KT update.
- Prefer Markdown and repository-native formats. Create Word/PDF derivatives only when explicitly required; keep Markdown as the maintainable source.

# Decision Rules
1. Current validated code and configuration define implemented behavior; approved requirements define intended behavior.
2. If documentation conflicts with executable evidence, explain the discrepancy and route it to the owning skill.
3. Prefer one coherent learning path over duplicated documents.
4. Reuse existing diagrams, README structure, terminology, and documentation tooling when accurate.
5. Document complex internals only to the depth needed to operate, test, troubleshoot, or extend them safely.
6. If a command cannot be executed, label it `not validated`, state the missing prerequisite, and do not present it as confirmed.
7. Use synthetic examples only when repository fixtures are insufficient and label them explicitly.
8. Do not make architecture, metric, security, or business-rule decisions within KT work.
9. When code readability is genuinely poor, document the issue and propose a separate, test-backed refactoring item for the build skill rather than silently changing code.

# Error-Handling Rules
- If required files are missing, list the missing paths, impact, and owning skill.
- If a path or symbol changed, search the repository and update all KT references before marking the document current.
- If commands fail, capture the command, environment, sanitized error, prerequisite state, and verified correction if available.
- If behavior cannot be proven, mark it unverified and identify the evidence needed.
- If secrets or sensitive values are found, do not copy them; replace with placeholders and report the source path for remediation.
- If documentation suggests an unsafe or destructive command, omit execution, mark the risk, and provide a safe alternative only when verified.
- Do not conceal known gaps to make KT appear complete.

# Validation Requirements
- All referenced files, folders, tables, jobs, symbols, tests, and configuration keys exist or are explicitly marked planned/missing.
- Setup, build, run, test, and diagnostic commands are executed successfully where the environment permits; otherwise each is labelled unvalidated with reason.
- Architecture and data-flow diagrams agree with current implementation and approved decisions.
- At least one end-to-end trace connects requirement, input, transformation, storage, output, log, and test evidence.
- SCD, bridge, fact grain, order-location versus fulfillment-location, manager assignment, and aggregate reconciliation explanations match implementation.
- No secrets, production credentials, or unnecessary sensitive data appear in outputs.
- Navigation links, headings, code blocks, tables, and diagram syntax render correctly.
- A junior-developer review checklist confirms the material supports setup, execution, testing, debugging, and a safe change.
- Reverse-KT tasks have measurable expected outcomes and evidence requirements.
- KT completion is not declared solely because documents exist; practical validation and reverse KT are required.

# Expected Outputs
Follow the existing repository convention. If none exists, create these under `knowledge-transfer/`:
- `README.md` as the KT index and learning path;
- `01-project-and-business-overview.md`;
- `02-architecture-and-component-map.md`;
- `03-repository-navigation-guide.md`;
- `04-data-model-and-scd-guide.md`;
- `05-end-to-end-data-flow-walkthrough.md`;
- `06-code-walkthrough.md`;
- `07-local-setup-configuration-and-run-guide.md`;
- `08-testing-and-validation-guide.md`;
- `09-debugging-and-troubleshooting-guide.md`;
- `10-safe-change-playbook.md`;
- `11-deployment-and-operations-awareness.md`;
- `12-known-issues-faq-and-glossary.md`;
- `13-hands-on-exercises.md`;
- `14-knowledge-check-with-answers.md`;
- `15-reverse-kt-and-competency-checklist.md`;
- `kt-tracker.md`;
- `documentation-traceability.md`;
- editable diagrams in the repository-supported format;
- `CHANGELOG.md` for KT updates.

If documents already exist, update and consolidate them rather than creating duplicates.

# Completion Criteria
- KT content covers the current in-scope implementation from business purpose through operation and safe maintenance.
- A junior developer can locate major components, explain the data flow, configure a safe environment, run the solution, execute tests, inspect logs, diagnose a guided failure, reconcile outputs, and complete one safe change using the documentation.
- Every critical explanation is traceable to current code, configuration, tests, or an approved decision.
- Required commands and examples have validation status.
- Knowledge checks and practical exercises include expected results.
- Reverse KT is completed with recorded evidence or explicitly remains pending.
- All defects and ambiguities are routed to the correct owning skill.
- KT index, traceability, and change log are current.
- No application behavior was modified by this skill.

# Handoff to Other Skills
- This skill normally runs after `sales-dimensional-etl-build` and `sales-analytics-quality-release`, and reruns after material project changes.
- Receive: project revision, requirement traceability, architecture decisions, changed-file manifest, schema/migration order, configuration-key list without values, commands, test evidence, report contracts, deployment notes, known issues, and runbooks.
- Return to `sales-warehouse-design-governance` when documentation discovers unclear requirements, conflicting grain, SCD ambiguity, or architecture mismatch.
- Return to `sales-dimensional-etl-build` when documentation validation finds code, schema, ETL, configuration, logging, test, readability, or maintainability defects.
- Return to `sales-analytics-quality-release` when report behavior, deployment guidance, rollback, monitoring, or operational evidence is inconsistent.
- Pass to the junior developer or onboarding owner: KT index, learning sequence, exercises, tracker, knowledge assessment, reverse-KT checklist, and unresolved issues.

# Prohibited Actions
- Do not change application, database, pipeline, report, test, or deployment behavior.
- Do not invent files, commands, architecture, interfaces, business rules, test results, owners, or operational procedures.
- Do not copy secrets, credentials, tokens, production endpoints, or sensitive records into KT material.
- Do not claim that documentation proves implementation.
- Do not copy large sections of source code when a path, symbol reference, and concise explanation are sufficient.
- Do not oversimplify critical security, data-integrity, SCD, or recovery behavior.
- Do not create duplicate documentation when an accurate maintainable document can be updated.
- Do not mark KT complete without practical validation and reverse-KT evidence.
- Do not leave incomplete placeholders such as TODO, TBD, or implement later.

# Final Response Format
Report:
1. repository revision or baseline reviewed;
2. KT scope and intended learner profile;
3. files created, updated, consolidated, or deprecated;
4. architecture and data-flow areas documented;
5. code paths, database objects, jobs, reports, tests, and operations covered;
6. commands validated and commands not validated with reasons;
7. exercises and knowledge checks produced;
8. reverse-KT status and competency evidence;
9. defects or ambiguities routed to each owning skill;
10. assumptions, known gaps, and pending items;
11. recommended learning sequence and next action.

# Final Checklist
- [ ] Current repository and all four skills read
- [ ] Requirements compared with implementation evidence
- [ ] Beginner-friendly learning path created
- [ ] Repository and component map verified
- [ ] Data model, SCD, bridge, facts, and aggregates explained
- [ ] Main execution paths traced end to end
- [ ] Setup, run, test, debug, and safe-change guides validated
- [ ] Exercises and knowledge checks include expected results
- [ ] Reverse-KT and competency checklist prepared
- [ ] All paths, symbols, commands, diagrams, and links checked
- [ ] Secrets and sensitive data excluded
- [ ] Documentation traceability and change log updated
- [ ] Issues handed to the correct owning skill
- [ ] No application behavior modified
