# Build Track: Project Briefs

**Week 2 | 3 Teams of 4 | Sprint 0 (Day 5) through Demo (Day 10)**

Each team selects one project. All three are designed to be completable in 4 sprint days, demo-able to leadership, and relevant to real consulting engagements.

---

## Team Formation Guidelines

Each team of 4 should include a mix of personas:

- At least 1 strong coder (AI Engineer, Software Engineer, or Data Engineer)
- At least 1 strong communicator (BA/Consultant, Product Manager, or Architect)
- Balance of technical depth across the team

Facilitators assign teams on Day 5 based on Week 1 performance and persona mix.

---

## Project A: Proposal Intelligence Engine

### Problem

Consultants spend 15-20 hours assembling each client proposal. They search across past proposals, case studies, team bios, and capability decks — most of it stored in scattered SharePoint folders and shared drives. A senior manager described it: "I know we've done exactly this kind of work before, but I can't find it when I need it."

### Target User

Consulting managers and partners who write 3-5 proposals per month.

### What to Build

A CLI/web tool where a user describes an opportunity in plain language and the system:

1. Retrieves relevant past proposals, case studies, and team profiles from a document corpus
2. Drafts a proposal outline tailored to the opportunity
3. Suggests relevant team members based on skills and past projects
4. Generates an executive summary and key differentiators section

### Required Claude Features (minimum 3)

- **RAG** — retrieve and ground responses in a document corpus
- **Tool use** — tools for searching documents, looking up team profiles, generating sections
- **System prompt** — enforce firm voice/tone, proposal structure, and formatting standards
- **Streaming** — show draft generation in real-time

### Provided Assets

A synthetic corpus will be provided (facilitators create before Day 5):
- 10 past proposal summaries (markdown)
- 8 team member profiles (name, title, skills, past projects)
- 5 case studies (client, challenge, approach, results)
- 1 firm capability overview

### Acceptance Criteria

- [ ] User can describe an opportunity in 2-3 sentences
- [ ] System retrieves at least 3 relevant documents from the corpus
- [ ] Generated proposal outline has: exec summary, approach, team, timeline, differentiators
- [ ] Team suggestions include rationale based on skills/experience match
- [ ] Output cites source documents (which proposal, which case study)
- [ ] Total generation time under 30 seconds

### Demo Pitch

"We turned a 15-hour proposal assembly process into a 15-minute draft. Here's a live demo: I describe an opportunity, and the engine finds relevant past work, suggests a team, and drafts a proposal — all grounded in our actual history."

---

## Project B: Codebase Onboarding Agent

### Problem

New team members joining a project spend their first 1-2 weeks reading code, asking questions in Slack, and building mental models of the architecture. Senior engineers spend hours answering the same onboarding questions. One tech lead said: "Every new person asks the same 20 questions. I wish I could clone myself for the first two weeks."

### Target User

Software engineers joining an existing project (new hires, rotations, or consultants staffed to a client).

### What to Build

An agentic CLI tool that ingests a codebase and becomes an interactive onboarding guide. It should:

1. Analyze the repository structure, key files, and architecture patterns
2. Answer natural language questions about the codebase with file references
3. Generate an onboarding document with architecture overview, key entry points, and common workflows
4. Provide guided walkthroughs of specific features ("show me how authentication works")

### Required Claude Features (minimum 3)

- **Claude Code / tool use** — file reading, search, shell commands for exploring the codebase
- **Extended thinking** — complex architectural analysis across multiple files
- **MCP** — filesystem server for structured codebase access
- **Prompt caching** — cache the codebase context for multi-turn Q&A

### Provided Assets

A sample codebase will be provided (facilitators create before Day 5):
- A Python web application (~2,000 lines across 15-20 files)
- FastAPI backend with auth, CRUD operations, and background jobs
- Basic test suite
- No documentation (intentionally — the agent creates it)

### Acceptance Criteria

- [ ] Agent can ingest a repo and describe its high-level architecture
- [ ] Answers questions like "How does authentication work?" with specific file/line references
- [ ] Generates a structured onboarding document (markdown) covering: architecture, key files, setup, common workflows
- [ ] Guided walkthrough mode: user asks about a feature, agent traces through the relevant files
- [ ] Handles "I don't know" gracefully when asked about code that doesn't exist
- [ ] Works on any Python project (not hardcoded to the sample)

### Demo Pitch

"New engineer, Day 1. Instead of 2 weeks of Slack questions and code spelunking, they run our agent and have a full architecture guide in 5 minutes. Watch me ask it how auth works — it traces through 4 files and explains every step."

---

## Project C: Client Meeting Intelligence

### Problem

After every client meeting, consultants write up notes, extract action items, and update the project tracker. This takes 20-30 minutes per meeting, and important details often get lost. A project manager said: "By the time I write up notes from meeting 3, I've already forgotten half of what was said in meeting 1."

### Target User

Project managers and engagement leads who run 3-5 client meetings per week.

### What to Build

A tool that processes meeting transcripts and produces structured intelligence:

1. Summarizes the meeting with key decisions, risks, and sentiment
2. Extracts action items with owners, deadlines, and priority
3. Tracks themes and decisions across multiple meetings (continuity)
4. Generates a client-ready meeting summary email
5. Flags risks or sentiment changes that need attention

### Required Claude Features (minimum 3)

- **Prompt engineering** — structured extraction with XML tags, few-shot examples
- **Tool use** — tools for reading transcripts, writing summaries, updating a tracking database
- **Agentic workflow** — multi-step: summarize → extract → compare → alert
- **Safety guardrails** — redact client-sensitive information before storing

### Provided Assets

Synthetic meeting transcripts will be provided (facilitators create before Day 5):
- 5 meeting transcripts from a fictional client engagement (progressive storyline)
- Each transcript is 1,500-2,500 words
- Transcripts include realistic elements: tangents, interruptions, implicit decisions, action items buried in discussion

### Acceptance Criteria

- [ ] Processes a transcript and produces: summary, decisions, action items, risks, sentiment score
- [ ] Action items have owner, deadline (if mentioned), and priority
- [ ] Cross-meeting tracking: tool can compare latest meeting with previous ones and flag changes
- [ ] Generates a professional client-ready email summary (different format from internal notes)
- [ ] Risk alerting: flags when sentiment drops or new risks appear
- [ ] Handles messy transcripts (tangents, incomplete sentences, speaker identification)

### Demo Pitch

"Five client meetings, zero manual note-taking. Watch the tool process all five transcripts, build a running tracker of decisions and action items, and catch a risk the project manager missed. Then it drafts the client follow-up email in 10 seconds."

---

## Sprint Schedule

| Day | Sprint | Deliverable |
|-----|--------|-------------|
| Day 5 (Fri) | Sprint 0 | Repo + CLAUDE.md + architecture decision record + Sprint 1 backlog |
| Day 6 (Mon) | Sprint 1 | Spec finalized + project harness + core scaffolding |
| Day 7 (Tue) | Sprint 2 | Core functionality working end-to-end |
| Day 8 (Wed) | Sprint 3 | Feature complete + polish + internal case study draft |
| Day 9 (Thu) | Sprint 4 | Bug fixes + demo prep + dry run + peer code review |
| Day 10 (Fri) | Demo | 15-min presentation to leadership |

---

## Evaluation Criteria

Not scored competitively, but discussed by facilitators and leadership:

| Criterion | What We're Looking For |
|-----------|----------------------|
| **Real-world applicability** | Could this tool be used on a real engagement tomorrow? |
| **Technical depth** | Thoughtful use of Claude features, not just surface-level integration |
| **Claude feature breadth** | Used 3+ features meaningfully (not checkbox usage) |
| **Code quality** | Clean architecture, CLAUDE.md, tests, error handling |
| **Team collaboration** | Everyone contributed. Clear division of work. |
| **Demo quality** | Clear problem statement, live demo works, lessons articulated |

---

## Choosing Your Project

On Day 5, teams rank their preferences 1-2-3. Facilitators assign to avoid duplicates where possible. If two teams want the same project, facilitators decide based on team composition and strengths.

All three projects are designed to be equally challenging. Pick the one that excites your team most.
