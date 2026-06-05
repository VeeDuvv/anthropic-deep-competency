# Case Study: Nova Retail — AI-Powered Personalization

## Client

Nova Retail, an omnichannel retailer with 120 physical stores and a growing e-commerce platform, $900M annual revenue.

## Challenge

Nova's recommendation engine was a rule-based system built in 2019 that suggested products based on simple category matching. Click-through rate on recommendations: 2.1%. Email marketing used generic segments (age, location) with a 1.8% conversion rate. The CMO said: "We know our customers buy from us, but we don't know why they buy or what they'll want next."

## Approach

Meridian built a modern AI personalization engine over 8 months:

- **Unified Customer Profile:** Integrated data from POS, e-commerce, loyalty program, and browsing behavior into a real-time customer profile (Kafka + feature store)
- **Recommendation Models:** Collaborative filtering for product recommendations, content-based filtering for new products with limited interaction data, and hybrid ranking
- **Generative Personalization:** Claude-powered personalized product descriptions, email subject lines, and promotional content tailored to individual customer preferences
- **A/B Testing Framework:** Built-in experimentation platform to continuously test and improve recommendations

## Results

- **2.1% → 8.7% click-through rate** on product recommendations (4x improvement)
- **1.8% → 4.2% conversion rate** on email marketing
- **$14M incremental revenue** attributed to personalized recommendations in first 6 months
- **23% increase** in average order value for customers receiving personalized recommendations
- **32% reduction** in email unsubscribes (relevant content = fewer opt-outs)
- Personalization engine processes 50M+ events per day in real-time

## Team

Sarah Nakamura (lead), Rachel Kim, David Okafor, + 2 additional engineers

## Client Quote

"The AI doesn't just recommend products — it writes product descriptions that speak to each customer's interests. One customer sees the hiking gear angle, another sees the urban commute angle, for the same jacket. That's a level of personalization we couldn't achieve with 100 marketers." — CMO, Nova Retail
