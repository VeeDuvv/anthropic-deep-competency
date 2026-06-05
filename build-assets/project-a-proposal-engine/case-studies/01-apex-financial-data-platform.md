# Case Study: Apex Financial Group — Data Platform Modernization

## Client

Apex Financial Group, a regional bank with $8B in assets, 1,200 employees, and 45 branch locations across the Midwest.

## Challenge

Apex's data infrastructure was a 12-year-old patchwork of SQL Server databases, SSIS ETL jobs, and Excel-based reporting. Regulatory reports (CCAR, DFAST) took 3 weeks to compile manually. Business analysts waited 48 hours for ad-hoc queries. The CTO described it as "flying blind with a 2-day delay on every decision."

## Approach

Meridian deployed a 6-person team over 12 months to modernize Apex's data platform:

- **Architecture:** Migrated 15 data domains from SQL Server to Snowflake on AWS, with dbt for transformations and Airflow for orchestration
- **Data Quality:** Implemented David Okafor's data quality framework — automated validation at every stage, reducing data incidents from 15/month to 2/month
- **Self-Service Analytics:** Replaced 40+ Excel reports with Tableau dashboards, reducing report generation from 48 hours to real-time
- **Regulatory Automation:** Automated CCAR and DFAST reporting, reducing compilation time from 3 weeks to 2 days

## Results

- **85% reduction** in regulatory report compilation time (3 weeks → 2 days)
- **48 hours → real-time** for business analytics queries
- **87% reduction** in data quality incidents (15/month → 2/month)
- **$1.2M annual savings** from decommissioned legacy infrastructure
- **35% increase** in analyst productivity — analysts spend time analyzing, not waiting
- Apex's internal data team (8 people) fully self-sufficient within 3 months of project completion

## Team

Rachel Kim (lead), David Okafor, James Rodriguez, + 3 additional engineers

## Client Quote

"Meridian didn't just migrate our data — they transformed how we make decisions. For the first time, our executives have real-time visibility into the bank's performance." — CFO, Apex Financial Group
