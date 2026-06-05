# Claude Competency Domains Overview

**Anthropic Deep Competency Program | 5 Domains | 14 Labs | 10 Days**

This program covers five skill domains that together represent comprehensive Claude practitioner competency. Week 1 covers all five domains through lectures, demos, and hands-on labs. The knowledge check on Day 5 assesses your understanding across all domains.

---

## Domain 1: Claude Fundamentals

**What it covers:** How Claude works, what it can do, and how to choose the right model.

| Topic | You Should Know |
|-------|----------------|
| Model family | Opus (deepest reasoning), Sonnet (balanced), Haiku (fastest) — and when to use each |
| Context window | 200K tokens — what that means, how to use it, when it's a constraint |
| Capabilities | Analysis, coding, writing, math, vision, multilingual |
| Limitations | No real-time data, no code execution (without tools), no persistent memory |
| Claude Code | Installation, CLAUDE.md, plan mode, slash commands, permission model |
| Pricing | Input/output tokens, caching discounts, batch API |

**Covered in:** Day 1 (lectures + Labs 01-02)

---

## Domain 2: Prompt Engineering

**What it covers:** How to write prompts that produce reliable, high-quality outputs.

| Topic | You Should Know |
|-------|----------------|
| Core principles | Be specific, use examples, give roles, break down tasks |
| XML tags | Structure input/output boundaries, prevent injection |
| Few-shot prompting | Selecting examples, formatting, edge case coverage |
| Chain-of-thought | When to use it, thinking tags, extended thinking |
| System prompts | Persona setting, constraints, output format control |
| Prefilling | Controlling response format by starting the assistant turn |
| Evaluation | Measuring prompt quality, A/B testing, consistency |

**Covered in:** Day 2 (lectures + Labs 03-05)

---

## Domain 3: Tool Use and Agents

**What it covers:** How to give Claude access to external tools and build autonomous agents.

| Topic | You Should Know |
|-------|----------------|
| Tool definition | JSON Schema for input_schema, clear descriptions |
| Tool use loop | tool_use → execute locally → tool_result → final response |
| Tool choice | auto, any, specific tool forcing |
| Multi-tool agents | Parallel calls, iterative tool use, error handling |
| Agentic patterns | ReAct, plan-execute-reflect, human-in-the-loop |
| Agent SDK | Agent, Tool, Runner, guardrails, handoffs |
| Decision framework | When to use agents vs. direct prompts |

**Covered in:** Day 3 (lectures + Labs 07-10)

---

## Domain 4: Enterprise Integration

**What it covers:** How to build production systems with Claude at the center.

| Topic | You Should Know |
|-------|----------------|
| Messages API | Request/response format, streaming, multi-turn, vision |
| Prompt caching | Cache breakpoints, 90% read discount, when to use |
| MCP | Protocol architecture, transports, building custom servers |
| RAG | Chunking, retrieval, grounding responses, citation |
| Extended thinking | Budget tokens, streaming, when it helps vs. overkill |
| Cost optimization | Model routing, caching, batching, token estimation |
| Deployment | Rate limiting, retries, monitoring, scaling |

**Covered in:** Days 2 + 4 (lectures + Labs 06, 11-13)

---

## Domain 5: Safety and Responsible AI

**What it covers:** How to build Claude applications that are safe, secure, and trustworthy.

| Topic | You Should Know |
|-------|----------------|
| Constitutional AI | How Claude's safety training works and why it matters |
| Prompt injection | Direct and indirect attacks, defense strategies |
| Guardrails | Input screening, system prompt hardening, output filtering |
| Evaluation | Automated eval suites, LLM-as-judge, red-teaming |
| Usage policy | What's allowed, what's not, responsible deployment |
| Production safety | Monitoring, feedback loops, incident response |

**Covered in:** Day 4 (lecture + Lab 14)

---

## How the Domains Map to the Program

```
Week 1 (In-Person NYC)
  Day 1  ████████████████  Domain 1: Fundamentals
  Day 2  ████████████████  Domain 2: Prompting  +  Domain 4: API/Streaming
  Day 3  ████████████████  Domain 3: Tool Use & Agents
  Day 4  ████████████████  Domain 4: MCP/RAG  +  Domain 5: Safety
  Day 5  ██████            Knowledge Check (all 5 domains)

Week 2 (Virtual)
  Days 6-10               AI-Native Build Track — apply all domains in a team project
```

---

## Self-Assessment

Before Day 1, rate yourself 1-5 on each domain. We'll compare again on Day 5.

| Domain | Pre-Program (1-5) | Post-Week 1 (1-5) |
|--------|-------------------|-------------------|
| 1. Claude Fundamentals | ___ | ___ |
| 2. Prompt Engineering | ___ | ___ |
| 3. Tool Use and Agents | ___ | ___ |
| 4. Enterprise Integration | ___ | ___ |
| 5. Safety and Responsible AI | ___ | ___ |

**Scale:** 1 = Never used it | 2 = Tried it once | 3 = Can do basics | 4 = Comfortable | 5 = Could teach it
