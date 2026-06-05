# Lab 09: Build an Agentic Workflow

**Day 3 | 60 min | Hands-on**

---

## Learning Objectives

- Implement the ReAct (Reason + Act) pattern
- Build a multi-step agent that plans, executes, and reflects
- Handle agent failures and recovery
- Understand when agentic patterns add value vs. overkill

## Prerequisites

- Labs 07-08 completed

---

## Setup

```bash
mkdir ~/lab-09 && cd ~/lab-09
```

---

## Part 1: ReAct Pattern (25 min)

Build an agent that explicitly reasons before each action.

Create `react_agent.py`:

```python
import anthropic
import json
import subprocess
from pathlib import Path

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "run_shell",
        "description": "Run a shell command and return its output. Only use for safe, read-only commands like ls, cat, wc, grep, find, python3 (for running scripts).",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"}
            },
            "required": ["command"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "think",
        "description": "Use this tool to reason about the current situation before taking action. Record your observations, analysis, and next step plan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "observation": {"type": "string", "description": "What you observe from the last action"},
                "analysis": {"type": "string", "description": "Your analysis of the situation"},
                "next_step": {"type": "string", "description": "What you plan to do next and why"},
            },
            "required": ["observation", "analysis", "next_step"],
        },
    },
]

# Safety: blocked commands
BLOCKED = {"rm", "rmdir", "mv", "cp", "chmod", "chown", "sudo", "su", "kill", "pkill"}

def execute_tool(name, input_data):
    if name == "run_shell":
        cmd = input_data["command"]
        first_word = cmd.split()[0] if cmd.split() else ""
        if first_word in BLOCKED:
            return json.dumps({"error": f"Blocked command: {first_word}"})
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=10, cwd=str(Path.cwd())
            )
            output = result.stdout + result.stderr
            return output[:3000] if output else "(no output)"
        except subprocess.TimeoutExpired:
            return json.dumps({"error": "Command timed out (10s limit)"})

    elif name == "write_file":
        path = Path(input_data["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(input_data["content"])
        return f"Written to {path}"

    elif name == "think":
        # The think tool doesn't execute anything — it just records the agent's reasoning
        return "Reasoning recorded. Proceed with your next action."

    return json.dumps({"error": f"Unknown tool: {name}"})


SYSTEM = """You are a methodical software agent that uses the ReAct pattern.

For every task:
1. THINK first — use the think tool to reason about what you know and plan your next step
2. ACT — use a tool to gather information or make changes
3. OBSERVE — analyze the tool result
4. REPEAT until the task is complete

Always use the think tool before taking action. Never skip the reasoning step.
If something fails, use the think tool to analyze why and plan recovery."""


def run_react_agent(task, max_turns=15):
    messages = [{"role": "user", "content": task}]

    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        # Print text blocks
        for block in response.content:
            if hasattr(block, "text") and block.text:
                print(f"\nAgent: {block.text}")

        if response.stop_reason != "tool_use":
            break

        # Execute tools
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "think":
                    print(f"\n  [THINK]")
                    print(f"    Observation: {block.input.get('observation', '')[:150]}")
                    print(f"    Analysis: {block.input.get('analysis', '')[:150]}")
                    print(f"    Next step: {block.input.get('next_step', '')[:150]}")
                else:
                    print(f"\n  [ACT: {block.name}] {json.dumps(block.input)[:120]}")

                result = execute_tool(block.name, block.input)

                if block.name != "think":
                    print(f"  [RESULT] {result[:200]}{'...' if len(result) > 200 else ''}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    print(f"\n[Completed in {turn + 1} turns]")


# Create a test scenario: a buggy Python project
Path("project").mkdir(exist_ok=True)
Path("project/app.py").write_text('''
def fibonacci(n):
    """Return the nth fibonacci number."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    """Return n factorial."""
    result = 1
    for i in range(n):  # Bug: should be range(1, n+1)
        result *= i
    return result

def is_palindrome(s):
    """Check if a string is a palindrome."""
    s = s.lower()
    return s == s[::-1]

if __name__ == "__main__":
    print(f"fib(10) = {fibonacci(10)}")
    print(f"5! = {factorial(5)}")
    print(f"racecar is palindrome: {is_palindrome('racecar')}")
    print(f"hello is palindrome: {is_palindrome('hello')}")
''')

Path("project/test_app.py").write_text('''
from app import fibonacci, factorial, is_palindrome

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

def test_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello") == False
    assert is_palindrome("A man a plan a canal Panama".replace(" ", "")) == True
''')

# Run the agent
run_react_agent("""
Examine the Python project in the project/ directory.
1. Read the source code
2. Run the tests and identify failures
3. Fix any bugs you find
4. Run the tests again to confirm they pass
""")
```

Run it: `python3 react_agent.py`

Watch the agent think → act → observe → repeat.

---

## Part 2: Plan-Execute Pattern (20 min)

Create `plan_execute.py`:

```python
import anthropic
import json

client = anthropic.Anthropic()

def create_plan(task):
    """Have Claude create a plan before executing."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a planning agent. Break the given task into numbered steps. Each step should be concrete and actionable. Output ONLY a JSON array of step strings.",
        messages=[
            {"role": "user", "content": f"Create a step-by-step plan for: {task}"},
            {"role": "assistant", "content": "["},
        ],
    )
    try:
        return json.loads("[" + response.content[0].text)
    except json.JSONDecodeError:
        return [response.content[0].text]

def execute_step(step, context):
    """Execute a single step with context from previous steps."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are an execution agent. Complete the given step. Be thorough and show your work.",
        messages=[
            {
                "role": "user",
                "content": f"Previous context:\n{context}\n\nCurrent step: {step}\n\nExecute this step.",
            }
        ],
    )
    return response.content[0].text

def reflect(task, results):
    """Reflect on whether the task was completed successfully."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system="You are a review agent. Evaluate whether the task was completed successfully. Be honest about gaps.",
        messages=[
            {
                "role": "user",
                "content": f"Task: {task}\n\nResults from each step:\n{results}\n\nWas the task completed successfully? What gaps remain?",
            }
        ],
    )
    return response.content[0].text

# Run the plan-execute pattern
task = "Write a comprehensive comparison of Python vs JavaScript for backend development, covering performance, ecosystem, ease of use, and job market."

print("=== PLANNING ===")
plan = create_plan(task)
for i, step in enumerate(plan, 1):
    print(f"  {i}. {step}")

print("\n=== EXECUTING ===")
context = ""
results = []
for i, step in enumerate(plan, 1):
    print(f"\n--- Step {i}: {step} ---")
    result = execute_step(step, context)
    print(result[:300] + "..." if len(result) > 300 else result)
    context += f"\nStep {i} result: {result[:500]}"
    results.append(f"Step {i}: {result[:500]}")

print("\n=== REFLECTING ===")
reflection = reflect(task, "\n".join(results))
print(reflection)
```

---

## Part 3: When NOT to Use Agents (15 min)

### 3.1 Discussion Exercise

For each scenario, decide: **Agent or direct prompt?**

1. Classify an email into one of 5 categories → **Direct prompt** (single step, deterministic)
2. Research a topic across multiple documents and write a report → **Agent** (multi-step, needs tools)
3. Translate a paragraph from English to French → **Direct prompt**
4. Debug a failing test suite in an unfamiliar codebase → **Agent** (exploration, iteration)
5. Generate a JSON object from a form description → **Direct prompt**
6. Monitor a deployment, check logs, and rollback if errors detected → **Agent** (multi-step, conditional)

### 3.2 The Agent Decision Framework

Create `decision.md` with your own notes:

```
Use an agent when:
- The task requires multiple steps that depend on intermediate results
- You need to interact with external systems (files, APIs, databases)
- The path to completion isn't known upfront
- Recovery from failures requires adaptation

Use a direct prompt when:
- The task is a single transformation (in → out)
- The output format is well-defined
- No external tool access is needed
- The task is deterministic
```

---

## Deliverables

- [ ] `react_agent.py` — ReAct agent that finds and fixes bugs
- [ ] `plan_execute.py` — plan-execute-reflect pattern
- [ ] `decision.md` — your agent decision framework

## Stretch Goals

1. Add a "retry with different approach" mechanism when a step fails 3 times
2. Add agent memory: save successful strategies to a file for future reference
3. Make the ReAct agent interactive — after each think step, let the user override the plan
