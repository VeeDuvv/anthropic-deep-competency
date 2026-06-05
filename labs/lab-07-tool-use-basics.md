# Lab 07: Build Your First Tool-Using App

**Day 3 | 60 min | Hands-on**

---

## Learning Objectives

- Define tools with JSON Schema input schemas
- Implement the tool use loop: `tool_use` → execute → `tool_result` → final response
- Handle tool inputs, validation, and error cases
- Understand tool choice modes: `auto`, `any`, `tool`

## Prerequisites

- Labs 03-04 completed
- `anthropic` SDK installed

---

## Setup

```bash
mkdir ~/lab-07 && cd ~/lab-07
```

---

## Part 1: A Single Tool (20 min)

### 1.1 Define a Calculator Tool

Create `calculator.py`:

```python
import anthropic
import json

client = anthropic.Anthropic()

# Define the tool
TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, %, and parentheses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g. '(2 + 3) * 4'",
                }
            },
            "required": ["expression"],
        },
    }
]

def execute_tool(name, input_data):
    """Execute a tool and return the result."""
    if name == "calculate":
        expr = input_data["expression"]
        # Safety: only allow math characters
        allowed = set("0123456789+-*/.() %")
        if not all(c in allowed for c in expr.replace("**", "")):
            return f"Error: expression contains invalid characters: {expr}"
        try:
            result = eval(expr)  # Safe because we validated the input
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    return f"Unknown tool: {name}"

def ask_with_tools(question):
    messages = [{"role": "user", "content": question}]

    # Step 1: Send the question with tools
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages,
    )

    print(f"Stop reason: {response.stop_reason}")

    # Step 2: Check if Claude wants to use a tool
    if response.stop_reason == "tool_use":
        # Process each content block
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Tool call: {block.name}({json.dumps(block.input)})")
                result = execute_tool(block.name, block.input)
                print(f"Tool result: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Step 3: Send tool results back to Claude
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        # Step 4: Get final response
        final = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        print(f"\nClaude: {final.content[0].text}")
    else:
        # No tool use needed
        print(f"\nClaude: {response.content[0].text}")

# Test it
ask_with_tools("What is 15% of 847.50?")
print("\n" + "=" * 50 + "\n")
ask_with_tools("If I invest $10,000 at 7% annual return for 10 years, how much will I have? Use compound interest.")
```

Run it: `python3 calculator.py`

### 1.2 Examine the Flow

Add print statements to see the full request/response cycle. Understand:
- Claude's response includes a `tool_use` block with `id`, `name`, and `input`
- You execute the tool locally and return a `tool_result` with the matching `tool_use_id`
- Claude then generates a natural language response incorporating the result

---

## Part 2: Multiple Tools (20 min)

### 2.1 Add a Weather and Time Tool

Create `multi_tool.py`:

```python
import anthropic
import json
from datetime import datetime

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time in a specified timezone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone name, e.g. 'US/Eastern', 'Europe/London', 'Asia/Tokyo'",
                    "default": "US/Eastern",
                }
            },
            "required": [],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Returns simulated weather data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'New York'"},
                "units": {
                    "type": "string",
                    "enum": ["fahrenheit", "celsius"],
                    "description": "Temperature units",
                    "default": "fahrenheit",
                },
            },
            "required": ["city"],
        },
    },
]

def execute_tool(name, input_data):
    if name == "calculate":
        expr = input_data["expression"]
        allowed = set("0123456789+-*/.() %")
        if not all(c in allowed for c in expr.replace("**", "")):
            return f"Error: invalid expression"
        try:
            return str(eval(expr))
        except Exception as e:
            return f"Error: {e}"

    elif name == "get_current_time":
        # Simplified: just return local time
        now = datetime.now()
        tz = input_data.get("timezone", "local")
        return f"Current time ({tz}): {now.strftime('%Y-%m-%d %H:%M:%S')}"

    elif name == "get_weather":
        # Simulated weather data
        city = input_data["city"]
        units = input_data.get("units", "fahrenheit")
        temp = 72 if units == "fahrenheit" else 22
        return json.dumps({
            "city": city,
            "temperature": temp,
            "units": units,
            "condition": "partly cloudy",
            "humidity": "65%",
            "wind": "10 mph SW",
        })

    return f"Unknown tool: {name}"

def ask_with_tools(question):
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Tool: {block.name}({json.dumps(block.input)})")
                    result = execute_tool(block.name, block.input)
                    print(f"  Result: {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # Final response
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\nClaude: {block.text}")
            break

# Test with questions that need multiple tools
print("=== Single tool ===")
ask_with_tools("What's the weather in New York?")

print("\n=== Multiple tools ===")
ask_with_tools("What time is it, and what's the weather in Tokyo in celsius?")

print("\n=== Tool + reasoning ===")
ask_with_tools("If it's 72F in New York and 22C in London, what's the difference in fahrenheit?")
```

**Key learning:** The `while True` loop handles multi-step tool use — Claude may call tools multiple times before giving a final answer.

---

## Part 3: Tool Choice Modes (10 min)

### 3.1 Experiment with Tool Choice

Add this to the bottom of `multi_tool.py`:

```python
# Force a specific tool
print("\n=== Forced tool use (any) ===")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    tools=TOOLS,
    tool_choice={"type": "any"},  # Must use at least one tool
    messages=[{"role": "user", "content": "Hello, how are you?"}],
)
for block in response.content:
    if block.type == "tool_use":
        print(f"  Forced tool: {block.name}({json.dumps(block.input)})")

# Force a specific tool
print("\n=== Forced specific tool ===")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    tools=TOOLS,
    tool_choice={"type": "tool", "name": "get_weather"},
    messages=[{"role": "user", "content": "What's 2+2?"}],
)
for block in response.content:
    if block.type == "tool_use":
        print(f"  Forced tool: {block.name}({json.dumps(block.input)})")
```

**Tool choice modes:**
- `auto` (default) — Claude decides whether to use tools
- `any` — Claude must use at least one tool
- `{"type": "tool", "name": "..."}` — Claude must use this specific tool

---

## Part 4: Error Handling (10 min)

### 4.1 Graceful Tool Errors

Create `tool_errors.py`:

```python
import anthropic
import json

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "lookup_user",
        "description": "Look up a user by their ID. Returns user info or an error if not found.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "The user's numeric ID"}
            },
            "required": ["user_id"],
        },
    }
]

FAKE_DB = {1: {"name": "Alice", "email": "alice@example.com"}, 2: {"name": "Bob", "email": "bob@example.com"}}

def execute_tool(name, input_data):
    if name == "lookup_user":
        uid = input_data["user_id"]
        if uid in FAKE_DB:
            return json.dumps(FAKE_DB[uid])
        else:
            return json.dumps({"error": f"User {uid} not found"})
    return json.dumps({"error": f"Unknown tool: {name}"})

def ask(question):
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=512, tools=TOOLS, messages=messages
        )
        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    print(f"  {block.name}({block.input}) -> {result}")
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": results})
        else:
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"Claude: {block.text}")
            break

# Successful lookup
print("=== Existing user ===")
ask("Look up user 1")

# Failed lookup — Claude should handle gracefully
print("\n=== Non-existent user ===")
ask("Look up user 999")
```

**Key learning:** Return errors as tool results, not exceptions. Claude handles error messages gracefully and explains the situation to the user.

---

## Deliverables

- [ ] `calculator.py` — single tool with full tool use loop
- [ ] `multi_tool.py` — three tools with iterative tool calling
- [ ] `tool_errors.py` — graceful error handling in tool results

## Stretch Goals

1. Add a `read_file` tool that reads local files (with path validation!)
2. Add a `search_web` tool stub that returns simulated search results
3. Build a tool that queries a SQLite database
