# Workspace Inventory & File Classification

## Classification Manifest

| Path | Category | Purpose | Status |
| :--- | :--- | :--- | :--- |
| `Skills.md` | Master Orchestrator | Execution rules and non-negotiable startup sequence | Active |
| `sales-warehouse-design-governance-skills.md` | Agent Skill | Governance & requirements skill source | Root Copy |
| `sales-dimensional-etl-build-skills.md` | Agent Skill | ETL build skill source | Root Copy |
| `sales-analytics-quality-release-skills.md` | Agent Skill | Quality & Release skill source | Root Copy |
| `sales-codebase-knowledge-transfer-skills.md` | Agent Skill | Knowledge Transfer skill source | Root Copy |
| `.agents/skills/sales-warehouse-design-governance/SKILL.md` | Agent Skill | Governance & requirements skill | Active |
| `.agents/skills/sales-dimensional-etl-build/SKILL.md` | Agent Skill | ETL build skill | Active |
| `.agents/skills/sales-analytics-quality-release/SKILL.md` | Agent Skill | Quality & Release skill | Active |
| `.agents/skills/sales-codebase-knowledge-transfer/SKILL.md` | Agent Skill | Knowledge Transfer skill | Active |
| `docs/analysis/*` | Analysis Documentation | Governance phase outputs | Creating |
| `sql/migrations/*` | Database DDL | DDL scripts for tables, constraints, indices | Creating |
| `src/*` | Source Code | Python ETL engine, models, analytics, utils | Creating |
| `reports/dashboard/*` | Consumption Layer | Month Sales Trend web dashboard | Creating |
| `tests/*` | Quality Assurance | Pytest test suite for dimensions, bridge, facts, reconciliation | Creating |
| `knowledge-transfer/*` | Documentation | 15-module junior developer onboarding suite | Creating |

---

## Secret Scan & Security Baseline
- Secrets scan conducted: Zero hardcoded credentials or API keys present in repository.
- Environment variables and sanitized configuration templates (`config/config.template.json`) used exclusively.
