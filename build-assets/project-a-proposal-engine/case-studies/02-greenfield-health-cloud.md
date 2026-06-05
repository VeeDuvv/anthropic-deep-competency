# Case Study: Greenfield Health System — Cloud Migration

## Client

Greenfield Health System, a 5-hospital network in the Midwest with 12,000 employees and 2 million patient encounters per year.

## Challenge

Greenfield's on-premise data centers were running 200+ clinical and administrative applications on aging hardware (some servers 8+ years old). Annual infrastructure maintenance cost $3.2M. The CIO's top concerns: a single power outage could take down the patient records system, telehealth expansion was impossible on current infrastructure, and HIPAA audit findings were increasing each year.

## Approach

Meridian's 8-person team executed a 14-month migration to AWS:

- **HIPAA Landing Zone:** Built a compliant AWS foundation with VPC isolation, encryption (at rest and in transit), CloudTrail audit logging, and automated compliance checks (AWS Config + custom rules)
- **Application Migration:** Migrated 200+ applications in 3 waves — administrative first, then clinical, then patient-facing. Zero PHI exposure incidents throughout
- **Database Modernization:** Migrated 12 Oracle databases to Aurora PostgreSQL, reducing licensing costs by $800K/year
- **Disaster Recovery:** Implemented multi-region DR with 15-minute RPO and 1-hour RTO, compared to previous 24-hour RTO

## Results

- **Zero downtime** during migration of critical clinical systems
- **Zero PHI exposure** incidents across 14 months of migration
- **$2.1M annual savings** ($800K Oracle licensing + $1.3M infrastructure consolidation)
- **99.99% uptime** since migration (vs. 99.5% on-premise)
- **Telehealth enabled:** New patient portal and video visit platform deployed on cloud infrastructure
- Clean HIPAA audit with zero findings for the first time in 5 years

## Team

Marcus Chen (lead), James Rodriguez, Priya Sharma, + 5 additional engineers

## Client Quote

"We slept through a major storm last winter — our systems stayed up because they were in the cloud. That alone was worth the investment." — CIO, Greenfield Health System
