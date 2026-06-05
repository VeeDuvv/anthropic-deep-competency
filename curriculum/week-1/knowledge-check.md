# Competency Knowledge Check

**Day 5 | 60 min | Individual | Open-Book**

This is a diagnostic assessment, not a pass/fail exam. Results help you and the facilitators identify gaps to focus on during Week 2 and beyond.

**Format:** 40 questions (8 per domain). Mix of multiple choice, short answer, and code snippets.

**Rules:**
- Open-book: you may reference docs.anthropic.com and your lab code
- No AI assistance (don't ask Claude to answer for you)
- 60 minutes total
- Write answers directly in this document or a copy

---

## Domain 1: Claude Fundamentals (8 questions)

### Q1. (Multiple Choice)

Which Claude model would you choose for a high-volume classification task where each input is a short sentence and cost efficiency matters most?

- A) Claude Opus
- B) Claude Sonnet
- C) Claude Haiku
- D) It doesn't matter — all models cost the same

### Q2. (Short Answer)

Claude's context window is 200K tokens. Approximately how many pages of standard English text is that? What practical limitation should you keep in mind even when your input fits within the window?

### Q3. (Multiple Choice)

What is the primary purpose of a CLAUDE.md file?

- A) To store API keys for Claude Code
- B) To provide project-level instructions and context that persist across Claude Code sessions
- C) To configure which Claude model to use
- D) To log Claude Code's activity history

### Q4. (Short Answer)

Name three things you should put in a CLAUDE.md and two things you should NOT put in one.

### Q5. (Multiple Choice)

In Claude Code, what does `/plan` mode do?

- A) Generates a project timeline with deadlines
- B) Claude analyzes the codebase and proposes changes without making them
- C) Creates a billing estimate for API usage
- D) Switches to a cheaper model for planning tasks

### Q6. (Short Answer)

You have a Python project where you want Claude Code to always use pytest (not unittest), type hints, and Google-style docstrings. Where do you configure this, and write a 3-line example.

### Q7. (Multiple Choice)

Which of these is NOT something Claude can do natively (without tools)?

- A) Analyze an image
- B) Write and debug code
- C) Execute a Python script
- D) Translate between languages

### Q8. (Short Answer)

Explain the difference between Claude Opus and Claude Sonnet. When would you pick Opus over Sonnet for an application, and when would Sonnet be the better choice?

---

## Domain 2: Prompt Engineering (8 questions)

### Q9. (Multiple Choice)

Which prompting technique is most effective for getting Claude to output a consistent, parseable format?

- A) Asking politely
- B) Using XML tags to define input/output structure
- C) Setting temperature to 0
- D) Using all caps in the prompt

### Q10. (Code Snippet)

The following prompt produces inconsistent output — sometimes a single word, sometimes a full paragraph. Fix it so it reliably returns only the category name.

```
Classify this support ticket: "My payment failed when I tried to upgrade."
```

Write the improved prompt.

### Q11. (Multiple Choice)

What is "assistant prefill" and when would you use it?

- A) Pre-loading Claude's memory with facts before a conversation
- B) Starting the assistant's response with specific text to control output format
- C) Caching the system prompt for faster responses
- D) Sending multiple messages in advance to warm up the model

### Q12. (Short Answer)

Explain the difference between few-shot prompting and chain-of-thought prompting. Give a one-sentence example of when you'd use each.

### Q13. (Code Snippet)

Write a system prompt for a Claude-powered customer support bot that:
- Only answers questions about a fictional product called "CloudSync"
- Refuses to discuss competitors by name
- Always responds in 3 sentences or fewer
- Escalates to a human agent if the user is angry

### Q14. (Multiple Choice)

You're building a classification system and need Claude to return valid JSON every time. Which combination of techniques gives you the highest reliability?

- A) System prompt + XML tags + assistant prefill with `{`
- B) High temperature + long max_tokens
- C) Few-shot examples only
- D) Chain-of-thought reasoning

### Q15. (Short Answer)

What is prompt injection? Describe one direct and one indirect injection attack, and name two defense strategies.

### Q16. (Code Snippet)

You have this prompt for extracting meeting action items, but it sometimes includes hallucinated items not in the transcript. Rewrite it to ground the output strictly in the provided text.

```python
messages = [
    {"role": "user", "content": f"Extract action items from this meeting: {transcript}"}
]
```

---

## Domain 3: Tool Use and Agents (8 questions)

### Q17. (Multiple Choice)

In the tool use flow, what happens immediately after Claude returns a response with `stop_reason: "tool_use"`?

- A) Claude executes the tool automatically
- B) The API returns the tool's result directly
- C) Your code executes the tool locally and sends the result back as a `tool_result`
- D) The conversation ends

### Q18. (Code Snippet)

Define a tool schema for a `search_database` tool that takes a `query` string (required), a `table` string (required, must be one of "users", "orders", "products"), and an optional `limit` integer with a default of 10.

Write the JSON tool definition.

### Q19. (Multiple Choice)

What is the purpose of `tool_choice: {"type": "any"}` in an API request?

- A) Claude will randomly select a tool
- B) Claude must use at least one tool (cannot respond with text only)
- C) All tools will be called in parallel
- D) Claude will use every available tool

### Q20. (Short Answer)

Explain the difference between the ReAct pattern and the plan-execute-reflect pattern for building agents. When would you choose one over the other?

### Q21. (Code Snippet)

This tool use loop has a bug that could cause an infinite loop. Find and fix it.

```python
def ask_with_tools(question):
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

### Q22. (Multiple Choice)

When should you return an error message as a `tool_result` instead of raising an exception in your tool executor?

- A) Never — always raise exceptions
- B) Always — Claude handles error messages gracefully and can adjust its approach
- C) Only for authentication errors
- D) Only when the user requests error handling

### Q23. (Short Answer)

What are guardrails in the context of the Agent SDK? Describe one input guardrail and one output guardrail you might use for a financial services chatbot.

### Q24. (Multiple Choice)

What is a "handoff" in a multi-agent system?

- A) When an agent saves its state to disk
- B) When one agent transfers control to a more specialized agent
- C) When an agent asks the user for clarification
- D) When an agent retries a failed tool call

---

## Domain 4: Enterprise Integration (8 questions)

### Q25. (Multiple Choice)

What is the primary cost benefit of prompt caching?

- A) Cached prompts run on faster hardware
- B) Cache read tokens cost 90% less than regular input tokens
- C) Caching eliminates output token costs
- D) Caching removes rate limits

### Q26. (Short Answer)

Describe the three components of MCP architecture (host, client, server) and give a concrete example of each when using Claude Code with a filesystem MCP server.

### Q27. (Code Snippet)

Write a Python function using the Anthropic SDK that makes a streaming API call and prints each text chunk as it arrives. Include token usage reporting at the end.

```python
def stream_response(prompt):
    # Your code here
    pass
```

### Q28. (Multiple Choice)

In a RAG pipeline, what is the purpose of "chunking"?

- A) Breaking documents into smaller pieces that fit in the context window and can be selectively retrieved
- B) Compressing documents to reduce storage costs
- C) Encrypting documents for security
- D) Converting documents from PDF to text

### Q29. (Short Answer)

You're building a RAG system and the retrieved chunks are often irrelevant, leading to poor answers. Name three strategies to improve retrieval quality.

### Q30. (Code Snippet)

This prompt caching code isn't working — cache reads always show 0. Find the issue.

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    system="You are a helpful assistant with expertise in Python programming.",
    messages=[{"role": "user", "content": question}],
)
```

### Q31. (Multiple Choice)

When using extended thinking, what happens if you set a budget of 4,000 tokens but the problem only needs 500 tokens of reasoning?

- A) Claude always uses the full budget
- B) Claude uses only what it needs — the budget is a maximum, not a target
- C) The remaining 3,500 tokens are charged but not used
- D) The API returns an error

### Q32. (Short Answer)

You need to process 10,000 customer support tickets with Claude for classification. Each ticket is independent. Describe the most cost-effective approach using the Anthropic API, and estimate the cost savings compared to the standard approach.

---

## Domain 5: Safety and Responsible AI (8 questions)

### Q33. (Multiple Choice)

What is Constitutional AI (CAI)?

- A) A legal framework for AI regulation
- B) Anthropic's approach to training Claude with a set of principles, using AI feedback instead of only human feedback
- C) A type of prompt engineering technique
- D) A compliance certification for AI models

### Q34. (Short Answer)

Explain the difference between a direct prompt injection and an indirect prompt injection. Which is harder to defend against, and why?

### Q35. (Code Snippet)

This summarizer is vulnerable to prompt injection. Add defenses using at least two of these three layers: input screening, system prompt hardening, output filtering.

```python
def summarize(user_text):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize: {user_text}"}],
    )
    return response.content[0].text
```

### Q36. (Multiple Choice)

Which of these is the BEST practice for handling user-provided content in a Claude API call?

- A) Include it directly in the prompt text
- B) Wrap it in XML tags to create a clear boundary between instructions and data
- C) Base64 encode it to prevent injection
- D) Truncate it to 100 characters

### Q37. (Short Answer)

Describe the "LLM-as-judge" evaluation pattern. What are its strengths, and what is one important limitation?

### Q38. (Multiple Choice)

According to Anthropic's usage policy, which of these use cases is NOT allowed?

- A) Automated customer support with human escalation
- B) Code generation and review
- C) Generating deceptive content designed to mislead people
- D) Summarizing medical research papers

### Q39. (Short Answer)

You're deploying a Claude-powered application that handles sensitive financial data. Name four production safety measures you would implement.

### Q40. (Code Snippet)

Write a simple output guardrail function that checks a Claude response for potential data leakage. It should flag responses that contain patterns resembling API keys, email addresses, or SSNs.

```python
def check_output_safety(response_text: str) -> dict:
    """Return {"safe": bool, "flags": [...]} """
    # Your code here
    pass
```

---

## Answer Key

*Distributed to facilitators only. Participants receive individual feedback after the knowledge check review session.*

---

## Scoring Guide

| Score | Level | Interpretation |
|-------|-------|---------------|
| 36-40 | Expert | Ready to teach others. Strong candidate for trainer pipeline. |
| 28-35 | Proficient | Solid across all domains. Minor gaps to address in Week 2. |
| 20-27 | Developing | Good foundation, some domains need reinforcement. Focus Week 2 labs on weak areas. |
| Below 20 | Foundational | Significant gaps. Pair with a proficient participant for Week 2 build track. |

**Remember:** This is diagnostic, not evaluative. Every score gives us useful information for making Week 2 as effective as possible.
