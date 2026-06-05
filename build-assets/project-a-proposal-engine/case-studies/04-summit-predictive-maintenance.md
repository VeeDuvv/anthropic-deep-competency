# Case Study: Summit Manufacturing — Predictive Maintenance

## Client

Summit Manufacturing, an industrial equipment manufacturer with 4 plants, 2,500 employees, and $1.2B in annual revenue.

## Challenge

Summit was losing $8M annually to unplanned equipment downtime. When a CNC machine or press brake failed, the entire production line stopped while maintenance scrambled for parts and technicians. Average unplanned downtime: 6 hours per incident, 15 incidents per month across 4 plants. The VP of Operations called it "our most expensive problem that we've accepted as normal."

## Approach

Meridian deployed an IoT-powered predictive maintenance system over 10 months:

- **Sensor Network:** Installed vibration, temperature, pressure, and acoustic sensors on 200 critical machines across all 4 plants, connected via AWS IoT Core
- **Real-Time Pipeline:** Kafka + Flink stream processing handling 2M sensor events per day, stored in TimescaleDB for time-series analysis
- **Predictive Models:** ML models trained on 12 months of historical data to detect anomalies and predict remaining useful life. Alerts fire 48-72 hours before expected failure
- **Mobile App:** Maintenance technicians receive push notifications with failure predictions, recommended actions, and parts availability

## Results

- **62% reduction** in unplanned downtime (15 incidents/month → 5.7)
- **$4.9M annual savings** from reduced downtime and optimized maintenance scheduling
- **48-72 hour advance warning** on 85% of equipment failures
- **22% reduction** in maintenance parts inventory (better planning = less emergency stock)
- **3.2x ROI** in first year (on $1.4M investment)
- Maintenance team shifted from reactive to predictive — job satisfaction scores increased 40%

## Team

Marcus Chen (lead), David Okafor, Tom Westbrook, + 4 additional engineers

## Client Quote

"We went from 'the machine just died' to 'the machine will need attention Thursday, and the parts are already on the shelf.' That's a fundamentally different way to run a factory." — VP of Operations, Summit Manufacturing
