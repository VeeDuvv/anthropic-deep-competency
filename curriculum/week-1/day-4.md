# Day 4: MCP + Extended Thinking + Enterprise Integration

**Thursday, June 25 | 8:00 AM - 5:00 PM ET | NYC (In-Person)**

---

## Agenda

| Time | Block | Format | Lead |
|------|-------|--------|------|
| 8:00-8:15 | Day 3 Recap + Q&A | Discussion | Sr. Manager |
| 8:15-9:15 | MCP Deep Dive: Protocol, Servers, Transports | Lecture + Demo | Manager |
| 9:15-10:15 | Lab 11: Build a Custom MCP Server | Hands-on | All |
| 10:15-10:30 | Break | -- | -- |
| 10:30-11:30 | Extended Thinking: When and How to Use It | Lecture + Demo | Sr. Manager |
| 11:30-12:15 | Lab 12: Extended Thinking for Complex Reasoning | Hands-on | All |
| 12:15-1:00 | Lunch | -- | -- |
| 1:00-2:00 | Enterprise Integration: RAG, Embeddings, Classification | Lecture + Demo | Sr. Manager |
| 2:00-3:00 | Lab 13: RAG Pipeline with Claude | Hands-on | All |
| 3:00-3:15 | Break | -- | -- |
| 3:15-4:15 | Safety + Responsible AI: Guardrails, Eval, Red-Teaming | Lecture + Demo | Manager |
| 4:15-4:45 | Lab 14: Safety Testing + Evaluation | Hands-on | All |
| 4:45-5:00 | Day 4 Wrap + Day 5 Preview | Discussion | Sr. Manager |
| 6:30 | Team Dinner | -- | -- |

---

## Learning Objectives

By the end of Day 4, participants will:

- Understand MCP architecture: clients, servers, transports, capabilities
- Build a custom MCP server that exposes domain-specific tools
- Use extended thinking for complex reasoning and math tasks
- Build a RAG pipeline: chunking, embedding, retrieval, generation
- Apply safety best practices: content filtering, prompt injection defense, evaluation
- Complete coverage of all 5 competency domains

---

## Session Details

### MCP Deep Dive (60 min)

- Model Context Protocol: what it is and why it matters
- Architecture: Host → Client → Server
- Capabilities: tools, resources, prompts, sampling
- Transports: stdio, SSE, streamable HTTP
- Existing servers: filesystem, GitHub, Slack, databases
- Building custom servers: Python SDK, TypeScript SDK

### Extended Thinking (60 min)

- What extended thinking is: Claude "thinks" before responding
- When to use it: complex reasoning, math, code analysis, multi-step planning
- Budget tokens: controlling thinking depth
- Streaming thinking: showing progress to users
- Limitations: no tool use during thinking, token costs
- Comparison with chain-of-thought prompting

### Enterprise Integration (60 min)

- RAG patterns: naive, hybrid, agentic RAG
- Embedding: Voyage AI, chunking strategies, vector databases
- Classification: multi-label, hierarchical, with confidence scores
- Summarization: extractive vs. abstractive, map-reduce for long docs
- Data extraction: structured output from unstructured input
- Integration patterns: microservices, event-driven, batch processing

### Safety + Responsible AI (60 min)

- Claude's safety training: Constitutional AI, RLHF
- Prompt injection: direct, indirect, defense strategies
- Content filtering: building guardrails for production apps
- Evaluation frameworks: automated eval, human eval, red-teaming
- Responsible deployment: monitoring, feedback loops, incident response
- Anthropic's usage policy: what's allowed and what's not

---

## Labs

- [Lab 11: Custom MCP Server](../../labs/lab-11-custom-mcp-server.md)
- [Lab 12: Extended Thinking](../../labs/lab-12-extended-thinking.md)
- [Lab 13: RAG Pipeline](../../labs/lab-13-rag-pipeline.md)
- [Lab 14: Safety Testing](../../labs/lab-14-safety-evaluation.md)

---

## Facilitator Notes

- Day 4 completes all 5 competency domains. Emphasize this milestone.
- The MCP server lab is the most technically challenging. Have working example code ready as a fallback.
- Second team dinner — use it to discuss build project ideas for Week 2.
