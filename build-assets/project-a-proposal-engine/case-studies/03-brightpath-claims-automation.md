# Case Study: BrightPath Insurance — Claims Processing Automation

## Client

BrightPath Insurance, a property & casualty insurer with 500K policyholders and 120K claims processed annually.

## Challenge

BrightPath's claims process was paper-heavy and slow. Average claim resolution: 14 business days. Adjusters spent 60% of their time on data entry — typing information from scanned forms, police reports, and medical records into the claims system. Customer satisfaction for claims handling was 3.1 out of 5. The VP of Claims said: "Our adjusters are the most expensive data entry clerks in the industry."

## Approach

Meridian built an AI-assisted claims processing platform over 9 months:

- **Document Intelligence:** OCR + Claude-powered extraction pipeline that reads claim forms, police reports, repair estimates, and medical records, extracting structured data with 92% accuracy
- **Smart Routing:** ML classifier that categorizes claims by complexity (simple/moderate/complex). Simple claims under $2K auto-approved with human spot-check
- **Adjuster Dashboard:** New interface with AI-generated claim summaries, historical comparisons, and recommended actions. Adjusters make decisions, AI does the grunt work
- **Fraud Detection:** Anomaly scoring model that flags suspicious claims for investigation (caught $3.2M in fraudulent claims in first 6 months)

## Results

- **14 days → 4 days** average claim resolution time (71% reduction)
- **40% of claims** auto-processed (simple claims under $2K)
- **60% → 15%** of adjuster time spent on data entry
- **3.1 → 4.4** customer satisfaction score for claims (out of 5)
- **$3.2M** in fraud detected in first 6 months of deployment
- **$2.8M annual savings** from operational efficiency gains

## Team

Priya Sharma (lead), Sarah Nakamura, Aisha Patel, + 3 additional engineers

## Client Quote

"Our adjusters finally get to do what they were hired to do — assess claims and help customers. The AI handles the paperwork." — VP of Claims, BrightPath Insurance
