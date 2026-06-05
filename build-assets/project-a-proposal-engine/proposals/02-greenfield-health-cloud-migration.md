# Proposal: Greenfield Health System — Cloud Migration & HIPAA Compliance

**Client:** Greenfield Health System (5-hospital network, Midwest)
**Date:** January 2025
**Value:** $1.8M over 14 months
**Status:** Won
**Team:** Marcus Chen (lead), James Rodriguez, Priya Sharma, + 4 additional engineers
**Practice:** Cloud & Infrastructure

## Executive Summary

Greenfield Health System operates 200+ clinical and administrative applications across aging on-premise data centers. Rising maintenance costs ($3.2M/year), compliance risks, and inability to support telehealth expansion are driving the need for cloud migration. We propose a multi-phase migration to AWS with a HIPAA-compliant landing zone, prioritizing patient-facing applications first.

## Approach

**Phase 1 (Months 1-4):** HIPAA-compliant AWS landing zone — VPC architecture, encryption, IAM, audit logging, and compliance automation. Migration of 15 low-risk administrative applications using lift-and-shift.

**Phase 2 (Months 5-10):** Migration of 50 clinical applications with dependency mapping, database migrations (Oracle to Aurora PostgreSQL), and performance testing. Implement disaster recovery across two AWS regions.

**Phase 3 (Months 11-14):** Modernization of patient portal (containerization, API layer), telehealth platform integration, and decommission of primary data center. Knowledge transfer and managed services transition.

## Key Differentiators

- Marcus Chen has led 15+ healthcare cloud migrations with zero PHI exposure incidents
- Pre-built HIPAA compliance automation (Terraform modules + AWS Config rules) reduces Phase 1 by 6 weeks
- Meridian's healthcare practice understands clinical workflow impact — we involve clinical stakeholders early
- 24/7 migration support during cutover weekends with rollback playbooks

## Timeline

14 months, 8-person team (5 Meridian + 3 Greenfield IT)
