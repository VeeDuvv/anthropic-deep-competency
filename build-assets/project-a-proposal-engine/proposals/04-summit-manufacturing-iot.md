# Proposal: Summit Manufacturing — IoT Platform & Predictive Maintenance

**Client:** Summit Manufacturing (industrial equipment, 4 plants, $1.2B revenue)
**Date:** September 2024
**Value:** $1.4M over 10 months
**Status:** Won
**Team:** Marcus Chen (lead), David Okafor, Tom Westbrook, + 4 additional engineers
**Practice:** Cloud & Infrastructure + Data & AI

## Executive Summary

Summit Manufacturing loses an estimated $8M annually to unplanned equipment downtime across 4 plants. Current maintenance is purely reactive — equipment runs until failure. We propose an IoT sensor platform with predictive maintenance ML models that detect failures 48-72 hours in advance, enabling planned maintenance windows and reducing downtime by 60%.

## Approach

**Phase 1 (Months 1-3):** IoT infrastructure — deploy sensors on 50 critical machines across 2 pilot plants. Build AWS IoT Core ingestion pipeline, time-series database (TimescaleDB), and real-time dashboards.

**Phase 2 (Months 4-7):** Predictive models — train anomaly detection and remaining-useful-life models on 12 months of historical sensor data. Build alerting system integrated with Summit's CMMS (computerized maintenance management system).

**Phase 3 (Months 8-10):** Scale to all 4 plants, 200+ machines. Optimize models with production data. Build mobile app for maintenance technicians. Knowledge transfer.

## Key Differentiators

- Tom Westbrook's manufacturing domain expertise — he's evaluated 15 IoT use cases and knows which deliver ROI
- Edge computing approach (AWS Greengrass) for low-latency local processing
- Meridian's data quality framework ensures clean sensor data from day one
- Phased rollout with 2-plant pilot proves value before full commitment

## Timeline

10 months, 7-person team (4 Meridian + 3 Summit engineering)
