# Lab 12: Extended Thinking for Complex Reasoning

**Day 4 | 45 min | Hands-on**

---

## Learning Objectives

- Enable and use extended thinking in the Messages API
- Control thinking depth with budget tokens
- Stream thinking output for user feedback
- Understand when extended thinking helps vs. adds cost without benefit

## Prerequisites

- Lab 03 completed
- `anthropic` SDK installed

---

## Setup

```bash
mkdir ~/lab-12 && cd ~/lab-12
```

---

## Part 1: Basic Extended Thinking (15 min)

### 1.1 With and Without Thinking

Create `thinking_comparison.py`:

```python
import anthropic
import time

client = anthropic.Anthropic()

PROBLEM = """A farmer has a rectangular field. If the length is increased by 20% and
the width is decreased by 10%, the area increases by 80 square meters.
If the length is decreased by 10% and the width is increased by 20%,
the area increases by 60 square meters.
Find the original dimensions of the field."""

# Without extended thinking
print("=== WITHOUT Extended Thinking ===")
start = time.time()
response_basic = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Solve this math problem:\n{PROBLEM}"}],
)
elapsed_basic = time.time() - start
print(response_basic.content[0].text)
print(f"\nTime: {elapsed_basic:.1f}s | Tokens: {response_basic.usage.input_tokens}in/{response_basic.usage.output_tokens}out")

# With extended thinking
print("\n\n=== WITH Extended Thinking ===")
start = time.time()
response_thinking = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 8000,
    },
    messages=[{"role": "user", "content": f"Solve this math problem:\n{PROBLEM}"}],
)
elapsed_thinking = time.time() - start

for block in response_thinking.content:
    if block.type == "thinking":
        print(f"[THINKING — {len(block.thinking)} chars]")
        print(block.thinking[:500] + "..." if len(block.thinking) > 500 else block.thinking)
    elif block.type == "text":
        print(f"\n[ANSWER]")
        print(block.text)

print(f"\nTime: {elapsed_thinking:.1f}s | Tokens: {response_thinking.usage.input_tokens}in/{response_thinking.usage.output_tokens}out")
```

Run it: `python3 thinking_comparison.py`

**Compare:**
- Is the thinking version's answer more accurate?
- How much longer did it take?
- How many more output tokens were used?

---

## Part 2: Budget Control (15 min)

### 2.1 Varying the Budget

Create `budget_experiment.py`:

```python
import anthropic
import time

client = anthropic.Anthropic()

HARD_PROBLEM = """You have a 3x3 grid. Place the digits 1-9 (each exactly once) so that:
- Each row sums to 15
- Each column sums to 15
- Both diagonals sum to 15
Show the solution grid."""

budgets = [1000, 4000, 10000]

for budget in budgets:
    print(f"\n{'='*50}")
    print(f"  Budget: {budget} tokens")
    print(f"{'='*50}")

    start = time.time()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=budget + 2000,  # Need room for thinking + answer
        thinking={
            "type": "enabled",
            "budget_tokens": budget,
        },
        messages=[{"role": "user", "content": HARD_PROBLEM}],
    )
    elapsed = time.time() - start

    thinking_chars = 0
    answer = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_chars = len(block.thinking)
        elif block.type == "text":
            answer = block.text

    print(f"  Thinking: {thinking_chars} chars")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Answer preview: {answer[:200]}")
    print(f"  Tokens: {response.usage.output_tokens} out")
```

**Key learning:** More budget = deeper thinking = better answers on hard problems, but diminishing returns on easy problems.

---

## Part 3: Streaming Thinking (15 min)

### 3.1 Show Thinking in Real-Time

Create `stream_thinking.py`:

```python
import anthropic

client = anthropic.Anthropic()

CODING_PROBLEM = """Write a Python function that finds the longest palindromic substring
in a given string. Optimize for O(n^2) time complexity or better.
Include test cases."""

print("Thinking", end="", flush=True)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=12000,
    thinking={
        "type": "enabled",
        "budget_tokens": 6000,
    },
    messages=[{"role": "user", "content": CODING_PROBLEM}],
) as stream:
    in_thinking = False
    for event in stream:
        if event.type == "content_block_start":
            if hasattr(event.content_block, "type"):
                if event.content_block.type == "thinking":
                    in_thinking = True
                elif event.content_block.type == "text":
                    if in_thinking:
                        print("\n\n--- Answer ---\n")
                        in_thinking = False

        elif event.type == "content_block_delta":
            if hasattr(event.delta, "thinking"):
                # Show a dot for each thinking chunk (don't reveal full thinking in production)
                print(".", end="", flush=True)
            elif hasattr(event.delta, "text"):
                print(event.delta.text, end="", flush=True)

print()

final = stream.get_final_message()
print(f"\nTokens: {final.usage.input_tokens}in / {final.usage.output_tokens}out")
```

**UX pattern:** In production, show a "thinking..." indicator while thinking blocks stream, then display the answer. Users shouldn't see raw thinking content.

### 3.2 Test the Generated Code

After running the stream, copy the Python function Claude generated and test it:

```bash
python3 -c "
# Paste the generated function here and run the test cases
"
```

---

## When to Use Extended Thinking

| Use Case | Extended Thinking? | Why |
|----------|-------------------|-----|
| Math/logic problems | Yes | Step-by-step reasoning improves accuracy |
| Code debugging | Yes | Systematic analysis of code paths |
| Simple classification | No | Overkill — adds cost without benefit |
| Translation | No | Doesn't need multi-step reasoning |
| Architecture planning | Yes | Benefits from exploring trade-offs |
| Data extraction | No | Pattern matching, not reasoning |
| Multi-step analysis | Yes | Complex chains of inference |

---

## Deliverables

- [ ] `thinking_comparison.py` — with/without thinking comparison
- [ ] `budget_experiment.py` — budget impact analysis
- [ ] `stream_thinking.py` — streaming thinking indicator

## Stretch Goals

1. Build a "hard problem detector" that decides whether to enable thinking based on prompt complexity
2. Compare extended thinking on Sonnet vs. Opus for the same problem
3. Use extended thinking with tool use — note: thinking blocks come before tool calls
