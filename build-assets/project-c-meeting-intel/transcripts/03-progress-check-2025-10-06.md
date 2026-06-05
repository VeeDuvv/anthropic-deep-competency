# Meeting Transcript: Sprint 1 Progress Check

**Client:** Ridgeline Financial Services
**Date:** October 6, 2025
**Time:** 10:00 AM - 11:00 AM ET
**Attendees:**
- Karen Walsh (Ridgeline, VP of Operations)
- Derek Simmons (Ridgeline, Director of IT)
- Tom Westbrook (Meridian, Engagement Lead)
- Priya Sharma (Meridian, Technical Lead)
- Aisha Patel (Meridian, Business Analyst)

*Note: Nina Patel unable to attend — sent written feedback on requirements doc.*

---

**Tom:** Morning everyone. Quick note — Nina couldn't make it today, but she reviewed the requirements doc and sent detailed feedback. Aisha, you incorporated that, correct?

**Aisha:** Yes, all of Nina's comments are addressed. She had two substantive changes — she wants the audit log to include IP addresses for all user actions, which is straightforward, and she wants a quarterly compliance report that summarizes all AI-assisted decisions with their approval rates. I've added both to the spec.

**Tom:** Great. Priya, let's start with development status.

**Priya:** So, good news and a complication. Good news first — the application portal integration is done. We have a clean API that pushes application data to a central message queue. The unified audit log is operational — every event from the portal gets timestamped and stored in a single database.

**Derek:** I can confirm that. My team tested it last Thursday and the data looks clean.

**Priya:** The complication is LoanPro. Their upgrade to v3 was supposed to happen today, but they pushed it to October 13. Something about another customer's migration taking longer than expected. So we're a week behind on that integration.

**Karen:** A week behind already? That worries me.

**Tom:** It's a week on the LoanPro piece specifically, not on the whole project. Priya was smart to build against the v3 sandbox — the adapter layer is ready. Once LoanPro does the upgrade, we just point it at production. So the actual integration work isn't delayed, just the production testing.

**Priya:** Right. And I've been using the extra time on the FIS integration, which is actually going well. Derek, what's the status on the rate limit?

**Derek:** Uh, not great. I've been going back and forth with FIS for two weeks. They want to charge us $15K per year for an increased rate limit. I'm pushing back, but honestly, I think we should just build the queue.

**Tom:** That changes our cost picture. The queuing system is the $30K contingency we discussed. Karen, should we proceed?

**Karen:** Yes. Just build it. I'd rather spend $30K once than $15K every year forever. Plus I don't trust FIS to actually deliver the increase on time anyway.

**Tom:** Agreed. Priya, add the queuing system to Sprint 2.

**Priya:** Already have a design ready. We'll use Redis-based queue with retry logic. Should take about a week to implement.

**Aisha:** I have an update on the customer experience side. I've been working with Karen's operations team on the status tracking design. We mapped out six stages that a loan application goes through — received, documents verified, underwriting review, decision pending, approved slash denied, and funding. Customers will see these stages with estimated time remaining.

**Karen:** My team loved the prototype. It's simple but it's exactly what customers have been asking for. One thing though — we had a debate about whether to show the "denied" status in real-time or have a human call the customer first. The concern is that a customer sees "denied" on their phone and we lose the chance to explain why and potentially offer alternatives.

**Tom:** That's a good UX question. What did you land on?

**Karen:** We want a 4-hour delay on denial notifications. The status shows "decision pending" for 4 hours after a denial, during which an associate calls the customer. After 4 hours, the status updates automatically whether we've reached them or not.

**Aisha:** I'll build that into the workflow. Priya, is the 4-hour delay technically complex?

**Priya:** Not at all. Simple scheduled task.

**Tom:** Okay, let me recap where we are against the timeline. Phase 1 target is November 1. We're on track for the portal integration and audit log. LoanPro integration is one week behind but recoverable. FIS integration is in progress, queuing system added. I'd say we're at moderate risk for Phase 1 — the LoanPro delay could cascade, but we have contingency time.

**Karen:** I want to raise something else. Our CEO mentioned this project in the all-hands last week. He's expecting big things. I don't want to dampen expectations, but I also don't want to overpromise. Tom, can you put together a one-page status update I can share with the executive team? Just the high-level — on track, key milestones, any risks.

**Tom:** Absolutely. I'll have it to you by Wednesday.

**Karen:** Thank you. And one more thing — I've started hearing from the underwriting team. They're nervous about the AI component. Some of them think we're trying to replace them. Can we schedule an introductory session with the underwriters to explain what we're actually building?

**Tom:** Great idea. Aisha, can you design a 30-minute session for the underwriting team? Focus on "AI as assistant, not replacement." Show them the mock-up of how the AI recommendation would appear in their workflow.

**Aisha:** I'll set that up for next week. Do we know how many underwriters there are?

**Derek:** Eight underwriters, but you probably only need the team lead and maybe two or three others for the initial session.

**Tom:** Okay, action items. Priya follows up with LoanPro on the October 13 upgrade — make sure it actually happens. Priya also builds the Redis queuing system in Sprint 2. Aisha schedules the underwriter session. Tom delivers the exec status update to Karen by Wednesday. Next meeting October 20.
