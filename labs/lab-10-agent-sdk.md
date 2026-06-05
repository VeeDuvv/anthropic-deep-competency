# Lab 10: Claude Agent SDK Quickstart

**Day 3 | 30 min | Hands-on**

---

## Learning Objectives

- Set up the Claude Agent SDK
- Build an agent with tools using the SDK's declarative API
- Implement guardrails for input/output validation
- Understand handoffs between multiple agents

## Prerequisites

- Labs 07-09 completed
- `pip install claude-agent-sdk`

---

## Setup

```bash
mkdir ~/lab-10 && cd ~/lab-10
pip install claude-agent-sdk
```

---

## Part 1: Your First SDK Agent (10 min)

### 1.1 Basic Agent with a Tool

Create `basic_agent.py`:

```python
from claude_agent_sdk import Agent, Tool, Runner
import json

# Define a tool using the SDK's decorator
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    """
    # Simulated prices
    prices = {
        "AAPL": 195.23,
        "GOOGL": 178.45,
        "MSFT": 420.10,
        "AMZN": 185.67,
        "TSLA": 248.90,
    }
    price = prices.get(symbol.upper())
    if price:
        return json.dumps({"symbol": symbol.upper(), "price": price, "currency": "USD"})
    return json.dumps({"error": f"Unknown symbol: {symbol}"})


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Math expression to evaluate (e.g., '2 + 3 * 4')
    """
    allowed = set("0123456789+-*/.() %")
    if not all(c in allowed for c in expression.replace("**", "")):
        return json.dumps({"error": "Invalid expression"})
    try:
        return str(eval(expression))
    except Exception as e:
        return json.dumps({"error": str(e)})


# Create an agent
agent = Agent(
    name="Financial Assistant",
    instructions="""You are a helpful financial assistant.
You can look up stock prices and do calculations.
Always show your math when computing portfolio values.""",
    tools=[get_stock_price, calculate],
)

# Run the agent
result = Runner.run_sync(
    agent=agent,
    messages=[
        {"role": "user", "content": "What's the total value of a portfolio with 100 shares of AAPL and 50 shares of GOOGL?"}
    ],
)

# Print the result
for message in result.messages:
    if hasattr(message, "content") and isinstance(message.content, str):
        print(message.content)
```

Run it: `python3 basic_agent.py`

**Compare to Lab 07:** Notice how much less boilerplate the SDK requires vs. the manual tool loop.

---

## Part 2: Guardrails (10 min)

### 2.1 Input and Output Validation

Create `guarded_agent.py`:

```python
from claude_agent_sdk import Agent, Runner, InputGuardrail, OutputGuardrail
import json

def lookup_employee(employee_id: str) -> str:
    """Look up an employee by their ID.

    Args:
        employee_id: The employee's ID number
    """
    employees = {
        "E001": {"name": "Alice Smith", "department": "Engineering", "salary": 150000},
        "E002": {"name": "Bob Jones", "department": "Marketing", "salary": 120000},
        "E003": {"name": "Carol White", "department": "Engineering", "salary": 160000},
    }
    emp = employees.get(employee_id)
    if emp:
        return json.dumps(emp)
    return json.dumps({"error": f"Employee {employee_id} not found"})


# Input guardrail: block requests asking for salary comparisons
async def block_salary_comparison(messages, context):
    last_message = messages[-1]["content"] if messages else ""
    if isinstance(last_message, str):
        sensitive_terms = ["salary comparison", "who earns more", "highest paid", "pay gap"]
        for term in sensitive_terms:
            if term.lower() in last_message.lower():
                return {"blocked": True, "reason": f"Request involves sensitive salary data: '{term}'"}
    return {"blocked": False}

# Output guardrail: redact salary information from responses
async def redact_salary(response_text, context):
    import re
    # Replace dollar amounts that look like salaries
    redacted = re.sub(r'\$\d{3},?\d{3}', '$[REDACTED]', response_text)
    return redacted

agent = Agent(
    name="HR Assistant",
    instructions="""You are an HR assistant. You can look up employee information.
You should help with department and role questions.
Never reveal exact salary figures — refer users to HR for compensation details.""",
    tools=[lookup_employee],
    input_guardrails=[InputGuardrail(block_salary_comparison)],
    output_guardrails=[OutputGuardrail(redact_salary)],
)

# Test: normal query
print("=== Normal query ===")
result = Runner.run_sync(
    agent=agent,
    messages=[{"role": "user", "content": "What department does employee E001 work in?"}],
)
for msg in result.messages:
    if hasattr(msg, "content") and isinstance(msg.content, str):
        print(msg.content)

# Test: blocked query
print("\n=== Blocked query ===")
try:
    result = Runner.run_sync(
        agent=agent,
        messages=[{"role": "user", "content": "Who earns more, E001 or E003?"}],
    )
    for msg in result.messages:
        if hasattr(msg, "content") and isinstance(msg.content, str):
            print(msg.content)
except Exception as e:
    print(f"Blocked: {e}")
```

---

## Part 3: Multi-Agent Handoffs (10 min)

### 3.1 Specialist Agents

Create `handoff_agent.py`:

```python
from claude_agent_sdk import Agent, Runner
import json

# Specialist: Technical Support
tech_agent = Agent(
    name="Tech Support",
    instructions="""You are a technical support specialist.
You help with software bugs, installation issues, and technical questions.
If the question is about billing or accounts, hand off to the appropriate agent.""",
)

# Specialist: Billing
billing_agent = Agent(
    name="Billing Support",
    instructions="""You are a billing specialist.
You help with payment issues, invoices, refunds, and subscription changes.
If the question is technical, hand off to tech support.""",
)

# Router: decides which specialist to use
router_agent = Agent(
    name="Support Router",
    instructions="""You are a support router. Analyze the customer's question and
hand off to the appropriate specialist:
- Tech Support: for bugs, errors, installation, how-to questions
- Billing Support: for payments, invoices, refunds, subscriptions

Always hand off — never try to answer directly.""",
    handoffs=[tech_agent, billing_agent],
)

# Test routing
queries = [
    "The app crashes when I try to export a PDF",
    "I was double-charged on my credit card last month",
    "How do I install the latest update on my Mac?",
]

for query in queries:
    print(f"\nCustomer: {query}")
    result = Runner.run_sync(
        agent=router_agent,
        messages=[{"role": "user", "content": query}],
    )
    # Show which agent handled it
    print(f"Handled by: {result.last_agent.name}")
    for msg in result.messages:
        if hasattr(msg, "content") and isinstance(msg.content, str):
            print(f"Response: {msg.content[:200]}")
```

---

## Deliverables

- [ ] `basic_agent.py` — SDK agent with tools
- [ ] `guarded_agent.py` — agent with input/output guardrails
- [ ] `handoff_agent.py` — multi-agent routing

## Important Note

The Agent SDK is evolving rapidly. If you encounter API differences from this lab, check the latest documentation. The concepts (agents, tools, guardrails, handoffs) are stable even if the exact syntax changes.

## Stretch Goals

1. Add tracing to the basic agent and inspect the trace output
2. Build a 3-agent pipeline: researcher → writer → editor
3. Add a "fallback" agent that handles cases no specialist can answer
