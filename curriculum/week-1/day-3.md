# Day 3: Tool Use + Agents

**Wednesday, June 17 | 8:00 AM - 5:00 PM ET | NYC (In-Person)**

---

## Agenda

| Time | Block | Format | Lead |
|------|-------|--------|------|
| 8:00-8:15 | Day 2 Recap + Q&A | Discussion | Sr. Manager |
| 8:15-9:15 | Tool Use Fundamentals: Defining, Calling, Handling | Lecture + Demo | Sr. Manager |
| 9:15-10:15 | Lab 7: Build Your First Tool-Using App | Hands-on | All |
| 10:15-10:30 | Break | -- | -- |
| 10:30-11:30 | Advanced Tool Patterns: Multi-Tool, Parallel, Error Handling | Lecture + Demo | Manager |
| 11:30-12:15 | Lab 8: Multi-Tool Agent | Hands-on | All |
| 12:15-1:00 | Lunch | -- | -- |
| 1:00-2:00 | Agentic Architecture: Loops, Memory, Orchestration | Lecture + Demo | Sr. Manager |
| 2:00-3:00 | Lab 9: Build an Agentic Workflow | Hands-on | All |
| 3:00-3:15 | Break | -- | -- |
| 3:15-4:15 | Claude Agent SDK: Building Production Agents | Lecture + Demo | Manager |
| 4:15-4:45 | Lab 10: Agent SDK Quickstart | Hands-on | All |
| 4:45-5:00 | Day 3 Wrap + Day 4 Preview | Discussion | Sr. Manager |

---

## Learning Objectives

By the end of Day 3, participants will:

- Define tools with JSON Schema input schemas
- Handle the tool use loop: tool_use → tool_result → final response
- Implement multi-tool agents with parallel tool calling
- Understand agentic patterns: ReAct, planning, memory, delegation
- Use the Claude Agent SDK for production-grade agent development
- Know when to use tools vs. prompt engineering vs. RAG

---

## Session Details

### Tool Use Fundamentals (60 min)

- Tool definition: name, description, input_schema (JSON Schema)
- The tool use loop: Claude decides to call → you execute → return result
- Best practices: clear descriptions, constrained schemas, error messages
- Computer use vs. API tools vs. MCP tools
- Tool choice: auto, any, specific tool forcing

### Advanced Tool Patterns (60 min)

- Parallel tool calls: when Claude calls multiple tools at once
- Multi-step tool chains: sequential tool calls for complex tasks
- Error handling: graceful degradation, retry logic
- Tool result formatting: structured vs. unstructured responses
- Security: input validation, sandboxing, preventing injection

### Agentic Architecture (60 min)

- What makes something "agentic": autonomy, tool use, loop, memory
- Agentic patterns:
  - ReAct (Reason + Act)
  - Plan → Execute → Reflect
  - Multi-agent delegation
  - Human-in-the-loop checkpoints
- State management: conversation history, external memory
- When NOT to use agents: simple tasks, deterministic workflows

### Claude Agent SDK (60 min)

- SDK overview: Python SDK for building production agents
- Core concepts: Agent, Tool, Runner
- Guardrails and safety: input/output validation
- Handoffs: multi-agent coordination
- Tracing and observability

---

## Labs

- [Lab 07: First Tool-Using App](../../labs/lab-07-tool-use-basics.md)
- [Lab 08: Multi-Tool Agent](../../labs/lab-08-multi-tool-agent.md)
- [Lab 09: Agentic Workflow](../../labs/lab-09-agentic-workflow.md)
- [Lab 10: Agent SDK Quickstart](../../labs/lab-10-agent-sdk.md)

---

## Facilitator Notes

- Day 3 is where it clicks for most people. The transition from "API caller" to "agent builder" is the aha moment.
- Lab 9 is the hardest lab so far. Pair weaker participants with stronger ones.
- The Agent SDK section assumes participants have completed Labs 7-8. Don't skip ahead.
