# Meeting Transcript: Technical Assessment Review

**Client:** Ridgeline Financial Services
**Date:** September 22, 2025
**Time:** 10:00 AM - 11:30 AM ET
**Attendees:**
- Karen Walsh (Ridgeline, VP of Operations)
- Derek Simmons (Ridgeline, Director of IT)
- Nina Patel (Ridgeline, Head of Compliance)
- Tom Westbrook (Meridian, Engagement Lead)
- Priya Sharma (Meridian, Technical Lead)
- Aisha Patel (Meridian, Business Analyst)

---

**Tom:** Good morning. We've had two productive weeks since the kickoff. Priya finished the technical assessment and Aisha completed the compliance deep-dive with Nina. Let's walk through what we found.

**Priya:** Thanks Tom. I'll start with the systems audit. So the good news is that the overall architecture is more salvageable than I expected. The application portal — the .NET app — is actually well-structured. The codebase is clean, it has decent test coverage, and it has a REST API that we can extend.

**Derek:** That's nice to hear. Our team built that one, so I'll pass along the compliment.

**Priya:** The LoanPro situation — I have mixed news. Derek was right that the v2 API is painful. But I spoke with their engineering team directly — went around support — and they confirmed that Ridgeline is eligible for a free upgrade to v3. The v3 API has proper webhooks, a sandbox environment, and decent documentation. The upgrade takes about two weeks on their end.

**Karen:** Is there a catch? That sounds too easy.

**Priya:** The catch is timing. They have an upgrade queue and the earliest slot is October 6. That puts us two weeks behind on the integration workstream. I'd recommend we start building the adapter layer against the v3 sandbox now, and switch to production when the upgrade completes.

**Derek:** I'll reach out to our LoanPro account rep to confirm that October 6 date.

**Priya:** For the FIS core banking integration, I want to flag a risk. Their API has a rate limit of 100 requests per minute. For batch processing — like running all pending applications through underwriting — that's going to be a bottleneck. We either need to negotiate a higher limit or build a queuing system.

**Tom:** What's the impact if we don't solve the rate limit?

**Priya:** On a busy day with 200 applications, batch processing would take over two hours instead of minutes. It won't affect individual applications, but it means daily reconciliation and reporting will be slow.

**Derek:** I can escalate the rate limit issue with FIS. We're a decent-sized customer, they should accommodate us. But I wouldn't count on it happening quickly.

**Tom:** Okay, let's plan for both scenarios. Priya, build the queuing system as a fallback. Derek, pursue the rate limit increase. Whoever wins first, we go with that approach.

**Aisha:** Let me jump in with the compliance findings. Nina and I had an excellent session. I want to summarize the key requirements. First, every loan decision needs a complete audit trail — who reviewed it, when, what data they saw, and what decision they made. The current system actually has most of this, it's just scattered across three systems instead of unified.

**Nina:** Right. The OCC's concern wasn't that we don't have audit data, it's that we can't produce it quickly. When they asked for the decision trail on a specific loan, it took us three days to reconstruct it from three systems.

**Aisha:** So our integration layer needs to create a unified audit log. Second requirement — and this is the big one for the AI component — any AI-assisted decision needs to show its reasoning. If the system recommends approval, we need to show which factors drove that recommendation.

**Karen:** Is that a regulatory requirement or a Ridgeline requirement?

**Nina:** Both, actually. The regulators are increasingly focused on explainability in automated lending decisions. And internally, our underwriters won't trust a black box. They need to understand why the AI is recommending what it's recommending.

**Priya:** That's very doable with Claude. We can use structured prompts that explicitly list the factors considered and their contribution to the recommendation. It's actually one of Claude's strengths — it can show its work.

**Tom:** Let me share the updated timeline. We're proposing three phases. Phase 1, by November 1 — system integration. All three systems connected, unified audit log, real-time status tracking for customers. Phase 2, by November 21 — AI-assisted underwriting for simple loans. Auto-loans and personal loans under $25K with human review. Phase 3, by December 5 — expanded AI coverage, performance dashboards, and a customer-facing status portal.

**Karen:** That gives us a week before the board meeting with Phase 3. I'm comfortable with that. But I want to be realistic — what's the risk that Phase 1 slips?

**Tom:** The biggest risk is the LoanPro upgrade timing. If that slips past October 6, Phase 1 would push by the same amount. Priya's parallel development approach mitigates most of it.

**Karen:** Okay. Derek, make the LoanPro upgrade your priority this week.

**Derek:** On it.

**Tom:** One thing I want to raise — budget. We scoped this at $480K in the original proposal. Based on the technical assessment, I think we're on track, but the FIS queuing system is out of scope. That's about $30K additional. I wanted to flag it now rather than surprise you later.

**Karen:** Is the queuing system optional?

**Tom:** It is if Derek gets the rate limit increased. But I'd recommend budgeting for it as a contingency.

**Karen:** Fine. $30K contingency is approved on my end. I'll need to inform finance, but it's within my authority.

**Tom:** Great. Action items: Derek confirms LoanPro upgrade date and pursues FIS rate limit. Priya begins adapter development against v3 sandbox. Aisha finalizes the requirements doc with the audit trail and explainability specifications. Nina reviews the requirements doc before we start development.

**Nina:** When can I expect the requirements doc?

**Aisha:** End of this week. I'll send it Friday.

**Nina:** I'll review over the weekend and have feedback by Monday.

**Tom:** Perfect. Next meeting October 6 — we'll be two weeks into development. Same time.
