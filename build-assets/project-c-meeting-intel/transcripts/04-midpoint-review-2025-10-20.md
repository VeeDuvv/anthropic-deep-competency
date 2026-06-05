# Meeting Transcript: Midpoint Review

**Client:** Ridgeline Financial Services
**Date:** October 20, 2025
**Time:** 10:00 AM - 11:45 AM ET
**Attendees:**
- Karen Walsh (Ridgeline, VP of Operations)
- Derek Simmons (Ridgeline, Director of IT)
- Nina Patel (Ridgeline, Head of Compliance)
- Tom Westbrook (Meridian, Engagement Lead)
- Priya Sharma (Meridian, Technical Lead)
- Aisha Patel (Meridian, Business Analyst)

---

**Tom:** Welcome back everyone. We're at the midpoint — six weeks in, six weeks to go. Today I want to cover development status, the AI prototype, and a timeline conversation. Priya, take us through development.

**Priya:** Right, so let me go through each system. Application portal integration — done and in production. Working smoothly, no issues. Unified audit log — done, running in production. We've captured over 2,000 events in the first week alone. Nina, your compliance team can query this anytime.

**Nina:** I've already been using it. It's night and day compared to what we had. My analyst pulled a complete decision trail in 3 minutes last week. That used to take 3 days.

**Karen:** That alone might be worth the whole project.

**Priya:** LoanPro upgrade happened on October 14 — one day late, but it's done. Our adapter layer connected to production on October 16 and it's been stable. Data flows from applications to LoanPro automatically now. The underwriters are seeing new applications appear in LoanPro within 30 seconds of submission instead of, what was it, Derek, how long before?

**Derek:** Same day if we were lucky. Sometimes next morning.

**Priya:** And the FIS queuing system is done. We tested it with a batch of 500 transactions and it processed everything in 12 minutes, with proper error handling and retries. Derek's team has been monitoring it and no issues so far.

**Tom:** So Phase 1 — system integration — is essentially complete, about 10 days ahead of the November 1 target. That gives us more room for Phase 2.

**Karen:** That's excellent. What about the AI piece?

**Priya:** I have a working prototype. Let me share my screen. So this is the underwriter's dashboard. When a loan application comes in, the AI reviews the application data, credit report, income verification, and — for auto loans — vehicle valuation. It produces a recommendation with a confidence score and a detailed explanation.

**Priya:** Here's a real example from our test data. This is a $15,000 auto loan application. The AI recommends approval with 94% confidence. The explanation says — and I'll read it — "Applicant has a 720 credit score, stable employment for 5 years, debt-to-income ratio of 28% which is well within the 40% guideline, and the vehicle loan-to-value ratio is 82% against a KBB value of $18,300. No derogatory marks in the last 3 years."

**Karen:** That's exactly what I was hoping for. The underwriter can see the reasoning and either agree or disagree.

**Nina:** I have a question about the confidence score. What does 94% mean exactly? How do we explain that to the regulators?

**Priya:** It's based on how closely the application matches our approval criteria. A 94% means the application clearly meets all guidelines with significant margin. A score between 60-80% means some factors are borderline and need human judgment. Below 60%, the AI flags it for full manual review.

**Nina:** And what happens when the AI is wrong? Say it recommends approval and the underwriter disagrees?

**Priya:** Great question. The underwriter overrides the recommendation and enters a reason. That override gets logged in the audit trail and also feeds back into our quality monitoring. If we see a pattern of overrides — like the AI consistently misjudging a certain loan type — we adjust.

**Nina:** I'd like to see weekly reports on override rates, especially in the first month.

**Tom:** Aisha, add that to the reporting requirements.

**Aisha:** Got it. Speaking of the underwriters — the session we did last week went really well, by the way. The team lead, Marcus, was initially skeptical but by the end he was excited. His exact words were, I wrote them down — "If this does the data crunching, I can spend my time on the judgment calls that actually need experience." That's the adoption story we want.

**Karen:** That's great to hear. I was worried about pushback.

**Tom:** Now, there's a topic I need to raise that's less positive. Priya and I were reviewing the scope for Phase 3 — the customer-facing status portal — and we have a concern about timeline.

**Priya:** The portal itself is straightforward. The complication is that Karen's team wants it to include a document upload feature — so customers can upload pay stubs, bank statements, and ID verification photos directly. That wasn't in the original scope and it adds about two weeks of development for the upload handling, document validation, and integration with the underwriting workflow.

**Karen:** But it's such an obvious feature. If we're building a portal, not having document upload feels incomplete. Our competitors all have this.

**Tom:** I agree it's important. The question is timing. If we add document upload, Phase 3 moves from December 5 to approximately December 15 — which is after the board meeting.

**Karen:** Hmm. What if we launch the portal without upload by December 5, and add upload as a fast follow in January?

**Tom:** That works. We'd have the status tracking and notification features live for the board meeting, and document upload as a clear next step.

**Karen:** Let's do that. I'd rather show the board a working portal with a roadmap than nothing at all.

**Nina:** Before we move on — I want to flag something that came up in our internal risk review. We're storing loan applicant data in this new unified database. Have we done a data classification exercise? I need to make sure we have the right controls — encryption, access controls, retention policies.

**Derek:** Priya and I discussed this. The database is encrypted at rest and in transit. Access is role-based — only the application, the integration layer, and the audit log service can write to it. We need to define retention policies though.

**Nina:** I'll send you our data retention policy. Loan application data is 7 years for approved loans, 25 months for denied applications. Please make sure the system supports automated deletion at those intervals.

**Priya:** We'll add that to the backlog.

**Tom:** Good catch, Nina. Okay, to summarize. Phase 1 is done — ahead of schedule. Phase 2 — AI-assisted underwriting — targeting November 21. Phase 3 — customer portal without upload — targeting December 5. Document upload is a fast follow in January. Everyone aligned?

**Karen:** Aligned.

**Tom:** Next meeting November 3. We should have the AI system in beta testing with the underwriters by then.
