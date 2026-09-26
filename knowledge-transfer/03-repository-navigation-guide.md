# Module 03: Repository Navigation Guide

## Folder Structure Map

```
Session3/
├── .agents/skills/              # Active Agent Skills (Governance, Build, Quality, KT)
├── config/
│   ├── dev_config.json          # Development configuration settings
│   └── config.template.json     # Environment configuration template
├── docs/
│   ├── analysis/                # Phase 1 Governance & planning documentation
│   └── release/                 # Operations runbooks & release readiness reports
├── deploy/
│   └── ci_cd_pipeline.yml       # GitHub Actions CI/CD pipeline script
├── knowledge-transfer/          # 15-module onboarding suite for junior developers
├── reports/
│   └── dashboard/               # Month Sales Trend Web Dashboard (index.html, styles.css, app.js)
├── sql/
│   └── migrations/              # SQL DDL migrations (001 to 004)
├── src/
│   ├── analytics/               # Analytical reporting & reconciliation tools
│   ├── database/                # Database connection & migration runner
│   ├── etl/                     # Seed data generator & ETL pipeline loaders
│   └── utils/                   # Structured logging utility
├── tests/                       # Pytest unit & integration test suite
├── main.py                      # Master pipeline CLI orchestrator
└── requirements.txt             # Project dependencies
```
