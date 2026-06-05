# Proposal: Nova Retail — AI-Powered Personalization Engine

**Client:** Nova Retail (e-commerce + 120 physical stores, $900M revenue)
**Date:** November 2024
**Value:** $850K over 8 months
**Status:** Won
**Team:** Sarah Nakamura (lead), Rachel Kim, David Okafor, + 2 additional engineers
**Practice:** Data & AI

## Executive Summary

Nova Retail's current recommendation engine (rule-based, built in 2019) delivers generic product suggestions with a 2.1% click-through rate. Competitors using AI-powered personalization report 8-12% click-through rates. We propose replacing the rule-based system with a modern AI personalization engine combining collaborative filtering, content-based recommendations, and generative AI for personalized product descriptions.

## Approach

**Phase 1 (Months 1-3):** Data foundation — unify customer data from POS, e-commerce, loyalty program, and browsing behavior into a real-time customer profile. Build feature store for ML models.

**Phase 2 (Months 4-6):** Model development — collaborative filtering for product recommendations, customer segmentation for marketing, and Claude-powered personalized product descriptions and email content.

**Phase 3 (Months 7-8):** A/B testing framework, production deployment, and performance optimization. Target: 6%+ click-through rate on recommendations.

## Key Differentiators

- Sarah Nakamura built a similar personalization system at her previous company (achieved 9.2% CTR)
- Combined ML + generative AI approach — most competitors use one or the other
- Real-time processing capability (Kafka + feature store) for in-session personalization
- Built-in A/B testing framework for continuous optimization

## Timeline

8 months, 5-person team (3 Meridian + 2 Nova data team)
