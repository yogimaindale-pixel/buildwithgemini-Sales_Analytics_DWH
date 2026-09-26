---
name: sales-analytics-quality-release
description: Validate the completed Enterprise Sales Analytics solution end to end, implement or verify required dashboard and detailed-report assets, package deployment artifacts, and produce technical, operational, testing, security, and release documentation.
---
# Purpose
Own consumption-layer completion, independent quality validation, release readiness, deployment packaging, and technical/operational documentation for the Enterprise Sales Analytics project. This skill proves that implemented warehouse behavior satisfies the governed requirements and can be safely deployed and operated.

# When to Use This Skill
Load this skill when Antigravity must:
- create or update the Month Sales Trend dashboard or Detailed Monthly Sales Report using the project's established BI/reporting approach;
- run end-to-end, system, regression, performance, security, data-quality, report, and deployment-readiness validation;
- reconcile report outputs with warehouse facts;
- prepare CI/CD, deployment manifests, release notes, runbooks, rollback instructions, monitoring, alerting, and operational documentation;
- issue a release-readiness decision supported by evidence.

# When Not to Use This Skill
- Use `sales-warehouse-design-governance` for scope, architecture, grain, SCD, KPI-definition, or requirement ambiguity.
- Use `sales-dimensional-etl-build` for schema, migrations, dimensional loads, fact/aggregate logic, ETL orchestration, backend data interfaces, and implementation-level defect correction.

# Project Context
The required consumption outputs are:
1. **Month Sales Trend dashboard:** monthly revenue and quantity trend; sales by order location; sales by warehouse; sales by manufacturing facility using fulfilled quantity from a manufacturing site; regional revenue/quantity rollup; and month-over-month revenue with slicing by region and product. Weekly drill is stated as optional.
2. **Detailed Monthly Sales Report:** customer name, order date, total quantity, total revenue, sales location, location type, and business manager name, suitable for operational, reconciliation, and manager review use.

The authoritative model and requirement status come from `sales-warehouse-design-governance`; executable data behavior comes from `sales-dimensional-etl-build`. At initial analysis there was no chosen BI platform, deployment platform, code, test suite, or operational framework. Reinspect and use only discovered or approved technology.

# Required Files to Read
1. All three `.agents/skills/*/SKILL.md` files.
2. `requirement.docx` and all `docs/analysis/` artifacts.
3. Build handoff, changed-file manifest, schema/data dictionary, lineage, migration order, configuration reference, test results, and rollback notes.
4. All existing report/dashboard models, queries, semantic models, API contracts, test suites, CI/CD, infrastructure/deployment files, monitoring rules, security scans, and runbooks.
5. Existing organization/project coding, release, security, and documentation standards available in the repository.

# Preconditions
- Required architecture and KPI decisions are approved.
- Warehouse build artifacts exist and implementation-level tests pass, or failures are explicitly handed over for diagnosis.
- A permitted test environment and safe test dataset are available for executable validation.
- Target BI and deployment platforms are evidenced or approved before platform-specific artifacts are created.
- Production deployment requires explicit authorization; readiness validation alone does not authorize deployment.

# Responsibilities
This skill exclusively owns:
- semantic/report/dashboard implementation where required;
- cross-component and end-to-end acceptance tests;
- independent data reconciliation and requirement validation;
- regression, performance, security, resilience, and deployment-readiness checks;
- CI/CD and deployable packaging if part of the discovered project;
- environment promotion, rollback, monitoring, alerting, and support documentation;
- technical documentation consolidation and operational runbooks;
- release evidence, defect report, and go/no-go recommendation.

# Step-by-Step Execution Workflow
1. **Verify handoff integrity.** Confirm required artifacts, schema version, migrations, configuration keys, test commands, and traceability are present. Reject incomplete handoffs with a precise gap list.
2. **Baseline quality.** Run existing checks before modifying consumption or release assets. Preserve results for regression comparison.
3. **Select existing consumption pattern.** Use the repository's BI tool, semantic layer, query framework, naming, and deployment method. If absent, return the platform decision to governance; do not invent a BI stack.
4. **Implement/verify dashboard dataset.** Use `FACT_SALES_MONTHLY_AGG` for supported monthly views, while ensuring definitions reconcile to `FACT_SALES_ORDER_LINE`. Apply documented filters and labels.
5. **Implement/verify detailed report.** Source traceable fields from the atomic fact and valid dimension versions. Avoid joins that multiply order-line rows through the manager bridge.
6. **Validate metric semantics.** Confirm revenue uses the approved net/gross definition for each visual or field; document it visibly. Confirm manufacturing views use fulfillment location, while sales-location views use order location.
7. **Execute data-quality tests.** Check uniqueness, mandatory keys, referential integrity, SCD temporal validity, one-current-row rules, eligible fulfillment, manager assignment validity, measure arithmetic, duplicate facts, and aggregate reconciliation.
8. **Execute report acceptance.** Validate required fields, filters, drill behavior if implemented, totals, empty states, invalid filters, date boundaries, region/product slicing, and export behavior where supported.
9. **Execute non-functional validation.** Run available performance, security, dependency, secret, configuration, resilience, and regression checks. Record environment and reproducible commands.
10. **Package release.** Prepare or update CI/CD, deployment artifacts, environment templates, migration sequence, release notes, version/change log, and rollback procedure using the established platform.
11. **Prepare operations.** Document scheduling, dependencies, freshness checks, run monitoring, alerts, failure triage, rerun/recovery, reconciliation, data-quality ownership, backup/restore references, and escalation paths only where supported by evidence.
12. **Close traceability.** Attach validation evidence to each requirement ID. Mark failures or untested items accurately.
13. **Decide readiness.** Issue `GO`, `CONDITIONAL GO`, or `NO-GO` with objective entry/exit criteria and blockers.
14. **Handoff defects.** Route model/requirement defects to governance and implementation defects to build.

# Technical Standards
- Use only discovered/approved BI, test, CI/CD, and deployment technologies.
- Keep semantic definitions centralized according to the existing project pattern; do not duplicate metric logic across visuals.
- Dashboard aggregate totals must reconcile to the atomic source for equivalent filters.
- Report joins must preserve atomic order-line grain and historical dimension correctness.
- Distinguish order location from fulfillment location in naming and calculations.
- Month-over-month calculations must define prior-period behavior, missing months, and filter context using approved semantics.
- Tests must be deterministic, repeatable, environment-aware, and non-destructive by default.
- Deployment configuration must use external secret management; publish only sanitized templates.
- Logs, screenshots, exports, and evidence must not expose credentials or unnecessary sensitive data.
- Operational instructions must cite actual commands, paths, owners, and monitoring artifacts discovered in the repository; unsupported processes remain open issues.

# Decision Rules
1. Requirements and approved architecture decisions define acceptance.
2. Atomic fact is the reconciliation source of truth; aggregate fact is a performance layer.
3. Use fulfillment location for warehouse/manufacturing fulfillment analysis and order location for sales-origin analysis.
4. Do not guess whether report revenue means gross or net; use the approved metric decision or block the affected item.
5. Do not introduce a deployment target, BI platform, security tool, or monitoring product without evidence or approval.
6. A release cannot be `GO` when a critical requirement is failed, security exposure is unresolved, rollback is absent, or migration validation is incomplete.
7. A skipped test is not a pass.

# Error-Handling Rules
- Capture failing requirement ID, environment, input, prerequisite state, expected result, actual result, logs, and reproduction command.
- Redact secrets and minimize personal or customer data in evidence.
- Stop release packaging when schema/migration compatibility is invalid or artifact versions disagree.
- Route implementation defects to `sales-dimensional-etl-build`; route requirement/KPI/architecture ambiguity to `sales-warehouse-design-governance`.
- Use bounded retries only for transient environment failures; do not hide deterministic test failures.
- Never modify production or bypass approval to obtain validation evidence.

# Validation Requirements
- YAML/configuration/deployment artifacts parse successfully using available validators.
- All referenced files and commands exist and are executable in the documented context.
- Required dashboard views and detailed report fields are present and traceable.
- Aggregate and report totals reconcile to controlled atomic-fact queries.
- Required business-rule, SCD, referential, negative-path, rerun, and regression tests pass.
- Available security and secret scans pass or have documented approved exceptions.
- Deployment dry run or equivalent validation succeeds in a permitted non-production environment where supported.
- Rollback instructions are executable or verified structurally when execution is not permitted.
- Runbook includes detection, diagnosis, restart/rerun, reconciliation, and escalation information supported by project evidence.

# Expected Outputs
Follow existing project locations. If none exist, use suitable subfolders under `reports/`, `tests/`, `deploy/`, and `docs/`. Outputs may include:
- dashboard/semantic/report definitions and queries;
- end-to-end, data-quality, reconciliation, performance, security, and regression tests;
- validation evidence and defect reports;
- CI/CD and deployment manifests/scripts;
- sanitized environment templates;
- release notes, change log, deployment guide, rollback guide;
- operations runbook, monitoring/alert specification, troubleshooting guide;
- final traceability and release-readiness report.

# Completion Criteria
- Every in-scope requirement has pass/fail/blocked/not-tested evidence.
- Required analytics outputs are implemented and reconcile to source facts.
- No unresolved critical security, integrity, migration, or rollback issue remains for `GO`.
- Deployment package is version-consistent and validated.
- Technical and operational documentation matches actual files and commands.
- Known issues, assumptions, exceptions, and ownership are explicit.
- Final readiness decision is evidence-based.

# Handoff to Other Skills
- **Next:** project owner or authorized deployment operator after a `GO` decision.
- Pass release package, version, environment prerequisites, deployment sequence, configuration-key list without values, validation evidence, rollback steps, runbook, monitoring checks, known issues, and readiness decision.
- Return implementation defects to `sales-dimensional-etl-build` with reproducible evidence.
- Return requirement, KPI, grain, SCD, or architecture ambiguity to `sales-warehouse-design-governance`.
- Re-run affected validation after either skill provides corrected artifacts.

# Prohibited Actions
- Do not change schema, ETL, or backend implementation directly to hide a failed test.
- Do not invent BI, deployment, monitoring, SLA, RTO/RPO, retention, or ownership requirements.
- Do not mark skipped, blocked, or manually inspected items as passed.
- Do not deploy to production without explicit authorization.
- Do not hardcode or publish secrets.
- Do not weaken acceptance thresholds without an approved decision.
- Do not leave TODO, TBD, placeholder tests, fake screenshots, or fabricated evidence.

# Final Response Format
Report:
1. release scope and version;
2. analytics artifacts created or changed;
3. tests executed with pass/fail/blocked results;
4. reconciliation results;
5. security and configuration validation;
6. deployment package and dry-run result;
7. documentation produced;
8. defects by owning skill;
9. assumptions, exceptions, and unresolved issues;
10. readiness decision and evidence;
11. handoff instructions.

# Final Checklist
- [ ] Build handoff verified
- [ ] Required dashboard and report validated
- [ ] Atomic-to-aggregate reconciliation passed
- [ ] Business and SCD rules tested end to end
- [ ] Regression and non-functional checks recorded
- [ ] Secrets absent from artifacts and evidence
- [ ] Deployment and rollback validated
- [ ] Operations documentation matches implementation
- [ ] Traceability closed with evidence
- [ ] Readiness decision issued
