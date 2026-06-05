# Day 1: Foundations + Claude Code

**Monday, June 22 | 11:00 AM - 4:00 PM ET | NYC (In-Person)**

---

## Agenda

| Time | Block | Format | Lead |
|------|-------|--------|------|
| 11:00-11:30 | Welcome + Introductions | Facilitated | PPMD |
| 11:30-12:00 | Program Overview: Two Tracks, Two Weeks | Presentation | Sr. Manager |
| 12:00-12:45 | Claude Fundamentals: Architecture, Models, Capabilities | Lecture + Demo | Sr. Manager |
| 12:45-1:30 | Lunch | -- | -- |
| 1:30-2:15 | Claude Code Deep Dive: Setup, CLAUDE.md, Workflows | Live Demo | Manager |
| 2:15-3:00 | Lab 1: Your First Claude Code Project | Hands-on | All facilitators |
| 3:00-3:15 | Break | -- | -- |
| 3:15-3:45 | Lab 2: CLAUDE.md Mastery + Slash Commands | Hands-on | All facilitators |
| 3:45-4:00 | Day 1 Wrap: Key Takeaways + Day 2 Preview | Discussion | Sr. Manager |
| 6:30 | Team Dinner | -- | -- |

---

## Learning Objectives

By the end of Day 1, participants will:

- Understand Claude's model architecture, context window, and key capabilities
- Know the difference between Claude models (Opus, Sonnet, Haiku) and when to use each
- Be productive in Claude Code: navigation, commands, plan mode, slash commands
- Have a working CLAUDE.md configuration for a real project
- Understand the two-track program structure (Competency + Build)

---

## Session Details

### Welcome + Introductions (30 min)

**Format:** Round-table

Each participant shares:
- Name, role, and team
- One thing they've already built or tried with AI
- What they most want to learn in the next two weeks

Facilitator sets expectations:
- This is a hands-on program — laptops open, code running
- Ask questions constantly — no "dumb questions" in this room
- We're building the playbook together — feedback shapes the program

### Program Overview (30 min)

**Key points to cover:**

- **Competency Track (Week 1):** Systematic coverage of 5 Claude domains
  - Domain 1: Claude Fundamentals
  - Domain 2: Prompt Engineering
  - Domain 3: Tool Use and Agents
  - Domain 4: Enterprise Integration
  - Domain 5: Safety and Responsible AI
- **Build Track (Week 2):** AI Product Process — build a real product as a team
  - Strategy → Spec → Harness → Build → Demo → Comms
- **Assessment:** Internal competency check at the end (not a formal exam)
- **Trainer pipeline:** 2-3 of you will become co-facilitators for future cohorts

### Claude Fundamentals (45 min)

**Content:**

- Claude model family: Opus (deepest reasoning), Sonnet (balanced), Haiku (fastest)
- Context window: 200K tokens — what that means in practice
- Key capabilities: analysis, coding, writing, math, vision, multilingual
- What Claude is NOT good at: real-time data, executing code, browsing the web (without tools)
- Constitutional AI and safety: how Claude's training differs
- Pricing: input/output tokens, caching, batching

**Demo:**
- Same prompt across Opus, Sonnet, Haiku — compare quality, speed, cost
- Show a 200K context window in action (load a large codebase)

### Claude Code Deep Dive (45 min)

**Content:**

- What Claude Code is: an agentic coding tool in your terminal
- Core workflow: `claude` → natural language → code changes
- Key features:
  - File reading and editing
  - Shell command execution
  - Multi-file refactoring
  - Git integration
  - Plan mode (`/plan`) — think before you build
  - Custom slash commands (`.claude/commands/`)
  - MCP server integration
- CLAUDE.md: project-level instructions that persist across sessions
  - What to put in it: coding standards, architecture decisions, project context
  - What NOT to put in it: secrets, absolute paths, ephemeral state
- Permission model: what Claude Code can and cannot do without asking

**Live demo:**
- Start a new project from scratch using only Claude Code
- Show plan mode → implementation → test → commit flow
- Demonstrate CLAUDE.md influencing Claude's behavior

### Lab 1: Your First Claude Code Project (45 min)

See [Lab 01](../../labs/lab-01-claude-code-basics.md)

### Lab 2: CLAUDE.md Mastery + Slash Commands (30 min)

See [Lab 02](../../labs/lab-02-claude-md-slash-commands.md)

### Day 1 Wrap (15 min)

**Discussion prompts:**
- What surprised you about Claude Code?
- How does this compare to other AI coding tools you've used?
- What would you want Claude Code to do that it doesn't?

**Preview Day 2:** Messages API deep dive, prompt engineering techniques, and building your first API integration.

---

## Facilitator Notes

- Ensure all 12 participants have working Claude Code before lunch. If anyone is stuck, pair them with someone who's set up.
- The team dinner is important for cohort bonding — keep it informal, no agenda.
- Collect "parking lot" questions throughout the day for later sessions.
- If the pre-work was done well, the labs should flow quickly. Have stretch goals ready for fast finishers.
