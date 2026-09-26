# Documentation Traceability Matrix

| Knowledge Transfer Module | Primary Source File / Subsystem | Verification Test |
| :--- | :--- | :--- |
| `01-project-and-business-overview.md` | `docs/analysis/project-understanding.md` | Manual Review |
| `02-architecture-and-component-map.md` | `src/`, `sql/migrations/`, `reports/` | System Architecture Review |
| `03-repository-navigation-guide.md` | Session3 Repository Layout | File Tree Inspection |
| `04-data-model-and-scd-guide.md` | `sql/migrations/001_create_dimensions.sql` | `test_dimensions_scd.py` |
| `05-end-to-end-data-flow-walkthrough.md` | `src/etl/facts_loader.py` | `test_end_to_end_quality.py` |
| `06-code-walkthrough.md` | `src/` modules | Code Inspection |
| `07-local-setup-configuration-and-run-guide.md` | `main.py`, `requirements.txt` | Pipeline Run (`python3 main.py`) |
| `08-testing-and-validation-guide.md` | `tests/*.py` | `python3 -m unittest discover` |
| `09-debugging-and-troubleshooting-guide.md` | `src/etl/facts_loader.py`, `ETL_REJECT_LOG` | `test_fulfillment_rules.py` |
| `10-safe-change-playbook.md` | Pipeline workflow | Change Execution Test |
| `11-deployment-and-operations-awareness.md` | `deploy/ci_cd_pipeline.yml` | Pipeline Syntax Check |
| `12-known-issues-faq-and-glossary.md` | Project Business Rules | Domain Verification |
| `13-hands-on-exercises.md` | Lab tasks | Practical Exercise Verification |
| `14-knowledge-check-with-answers.md` | Knowledge Check Questions | Self-Assessment Scoring |
| `15-reverse-kt-and-competency-checklist.md` | Competency Rubric | Evaluator Sign-off |
