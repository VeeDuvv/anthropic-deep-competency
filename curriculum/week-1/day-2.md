# Day 2: API Deep Dive + Prompt Engineering

**Tuesday, June 23 | 8:00 AM - 5:00 PM ET | NYC (In-Person)**

---

## Agenda

| Time | Block | Format | Lead |
|------|-------|--------|------|
| 8:00-8:15 | Day 1 Recap + Q&A | Discussion | Sr. Manager |
| 8:15-9:15 | Messages API Deep Dive | Lecture + Demo | Sr. Manager |
| 9:15-10:00 | Lab 3: Messages API — From Curl to Production | Hands-on | All |
| 10:00-10:15 | Break | -- | -- |
| 10:15-11:15 | Prompt Engineering: Principles + Patterns | Lecture + Demo | Sr. Manager |
| 11:15-12:00 | Lab 4: Prompt Engineering Workshop | Hands-on | All |
| 12:00-12:45 | Lunch | -- | -- |
| 12:45-1:45 | Advanced Prompting: System Prompts, Few-Shot, Chain-of-Thought | Lecture + Demo | Manager |
| 1:45-2:45 | Lab 5: Prompt Engineering Challenge | Hands-on | All |
| 2:45-3:00 | Break | -- | -- |
| 3:00-4:00 | Streaming, Caching, and Cost Optimization | Lecture + Demo | Manager |
| 4:00-4:45 | Lab 6: Build a Streaming Chat App | Hands-on | All |
| 4:45-5:00 | Day 2 Wrap + Day 3 Preview | Discussion | Sr. Manager |

---

## Learning Objectives

By the end of Day 2, participants will:

- Make Messages API calls confidently (Python SDK and raw HTTP)
- Understand all API parameters: model, max_tokens, temperature, top_p, stop_sequences
- Apply prompt engineering patterns: system prompts, few-shot, chain-of-thought, XML tags
- Use streaming for real-time responses
- Apply prompt caching to reduce costs and latency
- Understand token counting and cost estimation

---

## Session Details

### Messages API Deep Dive (60 min)

**Content:**

- Request anatomy: model, messages, max_tokens, system
- Message roles: user, assistant (pre-fill technique)
- Response structure: content blocks, stop_reason, usage
- Error handling: rate limits (429), overloaded (529), auth errors
- SDK vs raw HTTP: when to use each
- Multi-turn conversations: managing message history
- Vision: sending images in messages

**Demo:**
- Build up a Messages API call step by step
- Show multi-turn conversation management
- Demonstrate image analysis via the API

### Prompt Engineering: Principles + Patterns (60 min)

**Content:**

- The prompt engineering mental model: Claude is a helpful assistant, not a search engine
- Core principles:
  - Be specific and detailed
  - Use examples (few-shot)
  - Give Claude a role (system prompts)
  - Break complex tasks into steps
  - Use XML tags for structure
- Anti-patterns: vague instructions, assuming context, prompt injection vulnerabilities
- Evaluation: how to measure prompt quality

### Advanced Prompting (60 min)

**Content:**

- System prompts: persona, constraints, output format
- Few-shot prompting: selecting examples, formatting, edge cases
- Chain-of-thought: when to use it, `<thinking>` tags, extended thinking
- Prefilling assistant responses for format control
- Prompt chaining: breaking complex tasks into pipeline steps
- Long-context prompting: strategies for 200K token windows

### Streaming, Caching, and Cost Optimization (60 min)

**Content:**

- Streaming: server-sent events, SDK streaming, handling partial responses
- Prompt caching: how it works, cache breakpoints, cost savings (90% read discount)
- Batches API: async processing at 50% cost
- Token counting: estimating costs before calling
- Model selection strategy: Haiku for classification, Sonnet for general, Opus for complex reasoning

---

## Labs

- [Lab 03: Messages API](../../labs/lab-03-messages-api.md)
- [Lab 04: Prompt Engineering Workshop](../../labs/lab-04-prompt-engineering.md)
- [Lab 05: Prompt Engineering Challenge](../../labs/lab-05-prompt-challenge.md)
- [Lab 06: Streaming Chat App](../../labs/lab-06-streaming-chat.md)

---

## Facilitator Notes

- Day 2 is the heaviest lecture day. Keep energy up with frequent demos and live coding.
- The prompt engineering challenge (Lab 5) should be competitive — leaderboard on screen.
- Ensure participants understand caching before Day 3 — it's critical for tool use cost management.
