# Lab 08: Multi-Tool Agent

**Day 3 | 45 min | Hands-on**

---

## Learning Objectives

- Build an agent that combines multiple tools to solve complex tasks
- Implement a robust agent loop with conversation history
- Handle parallel tool calls
- Add human-in-the-loop confirmation for sensitive operations

## Prerequisites

- Lab 07 completed

---

## Setup

```bash
mkdir ~/lab-08 && cd ~/lab-08
```

---

## Part 1: Research Agent (25 min)

Build an agent that can search, calculate, and synthesize information.

Create `research_agent.py`:

```python
import anthropic
import json
import os
from pathlib import Path

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file. Returns the file text or an error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to read"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates the file if it doesn't exist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to write to"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and directories at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list", "default": "."}
            },
            "required": [],
        },
    },
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
        "name": "search_notes",
        "description": "Search through all .txt and .md files in the current directory for a keyword. Returns matching lines with filenames.",
        "input_schema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "Keyword to search for (case-insensitive)"}
            },
            "required": ["keyword"],
        },
    },
]

# Safety: restrict file operations to the lab directory
LAB_DIR = Path.cwd().resolve()

def execute_tool(name, input_data):
    try:
        if name == "read_file":
            path = (LAB_DIR / input_data["path"]).resolve()
            if not str(path).startswith(str(LAB_DIR)):
                return json.dumps({"error": "Access denied: path outside lab directory"})
            if not path.exists():
                return json.dumps({"error": f"File not found: {input_data['path']}"})
            return path.read_text()[:5000]  # Limit to 5K chars

        elif name == "write_file":
            path = (LAB_DIR / input_data["path"]).resolve()
            if not str(path).startswith(str(LAB_DIR)):
                return json.dumps({"error": "Access denied: path outside lab directory"})
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(input_data["content"])
            return f"Written {len(input_data['content'])} chars to {input_data['path']}"

        elif name == "list_directory":
            path = (LAB_DIR / input_data.get("path", ".")).resolve()
            if not str(path).startswith(str(LAB_DIR)):
                return json.dumps({"error": "Access denied"})
            entries = sorted(path.iterdir())
            return "\n".join(
                f"{'[DIR] ' if e.is_dir() else ''}{e.name}" for e in entries
            )

        elif name == "calculate":
            expr = input_data["expression"]
            allowed = set("0123456789+-*/.() %")
            if not all(c in allowed for c in expr.replace("**", "")):
                return json.dumps({"error": "Invalid expression"})
            return str(eval(expr))

        elif name == "search_notes":
            keyword = input_data["keyword"].lower()
            results = []
            for f in LAB_DIR.rglob("*"):
                if f.suffix in (".txt", ".md") and f.is_file():
                    for i, line in enumerate(f.read_text().splitlines(), 1):
                        if keyword in line.lower():
                            results.append(f"{f.name}:{i}: {line.strip()}")
            return "\n".join(results[:20]) if results else "No matches found."

    except Exception as e:
        return json.dumps({"error": str(e)})

    return json.dumps({"error": f"Unknown tool: {name}"})


def run_agent(task, max_turns=10):
    messages = [{"role": "user", "content": task}]

    system = """You are a research assistant with access to file and calculation tools.
You can read files, write files, list directories, search notes, and do math.
Break complex tasks into steps. Think about what information you need and which tools to use.
Always explain your reasoning before using tools."""

    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        # Print any text blocks
        for block in response.content:
            if hasattr(block, "text") and block.text:
                print(f"\nAgent: {block.text}")

        if response.stop_reason != "tool_use":
            break

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\n  [{block.name}] {json.dumps(block.input)[:100]}")
                result = execute_tool(block.name, block.input)
                print(f"  -> {result[:200]}{'...' if len(result) > 200 else ''}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    print(f"\n[Agent completed in {turn + 1} turns]")


# Create some test data first
Path("notes").mkdir(exist_ok=True)
Path("notes/meeting-monday.md").write_text(
    "# Monday Meeting\n- Budget: $50,000 allocated for Q3\n- Team size: 8 engineers\n- Deadline: August 15\n- Risk: vendor dependency on Acme Corp\n"
)
Path("notes/meeting-wednesday.md").write_text(
    "# Wednesday Meeting\n- Budget update: $12,000 spent so far\n- Hired 2 more engineers (total: 10)\n- Deadline moved to August 22\n- New risk: API rate limits\n"
)
Path("notes/project-plan.txt").write_text(
    "Project Alpha\nBudget: $50,000\nPhase 1: Design (2 weeks)\nPhase 2: Build (4 weeks)\nPhase 3: Test (2 weeks)\nPhase 4: Deploy (1 week)\nTotal: 9 weeks\n"
)

# Run the agent
run_agent("""
Review all the notes in the notes/ directory and create a summary report called summary.md that includes:
1. Current budget status (allocated vs spent, calculate remaining)
2. Team size changes
3. Deadline changes
4. All identified risks
5. Project timeline overview
""")
```

Run it: `python3 research_agent.py`

Watch the agent:
1. List the directory to find files
2. Read each file
3. Calculate budget remaining
4. Write the summary

---

## Part 2: Human-in-the-Loop (10 min)

### 2.1 Add Confirmation for Write Operations

Modify the `execute_tool` function to ask for confirmation before writing:

```python
def execute_tool_with_confirmation(name, input_data):
    if name == "write_file":
        path = input_data["path"]
        content_preview = input_data["content"][:200]
        print(f"\n  Agent wants to write to: {path}")
        print(f"  Content preview: {content_preview}...")
        confirm = input("  Allow? (y/n): ").strip().lower()
        if confirm != "y":
            return json.dumps({"error": "User denied write operation"})
    return execute_tool(name, input_data)
```

---

## Part 3: Parallel Tool Calls (10 min)

### 3.1 Observe Parallel Execution

Run this task:

```python
run_agent("Read all three files in the notes/ directory and tell me what each one is about.")
```

Claude may call `read_file` three times in a single response (parallel tool calls). Your loop handles this because it processes all `tool_use` blocks in each response.

**Key insight:** Parallel tool calls are more efficient — one round trip instead of three.

---

## Deliverables

- [ ] `research_agent.py` — multi-tool agent with file operations
- [ ] Agent successfully creates `summary.md` from notes
- [ ] Human-in-the-loop confirmation for write operations

## Stretch Goals

1. Add a `run_python` tool that executes Python code in a subprocess (with safety limits)
2. Add conversation memory — save agent conversations to a log file
3. Make the agent interactive: after completing a task, ask the user for follow-up instructions
