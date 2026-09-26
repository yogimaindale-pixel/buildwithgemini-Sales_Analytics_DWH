# Module 11: Deployment and Operations Awareness

## CI/CD Pipeline Lifecycle
The project incorporates continuous integration via GitHub Actions (`deploy/ci_cd_pipeline.yml`). Every commit triggers:
1. Environment setup (Python 3.10)
2. Schema migration verification
3. Full ETL run execution
4. Unit and integration test suite execution
5. Atomic-to-aggregate reconciliation verification gate

## Monitoring & Operational Logs
- `ETL_PIPELINE_RUNS`: Records `run_id`, `start_time`, `end_time`, `status`, `records_processed`, `records_rejected`.
- `ETL_REJECT_LOG`: Records quarantined records with raw JSON payload and rejection reason.
