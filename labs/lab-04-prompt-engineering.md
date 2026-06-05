# Lab 04: Prompt Engineering Workshop

**Day 2 | 45 min | Hands-on**

---

## Learning Objectives

- Apply core prompt engineering patterns: specificity, XML tags, role-setting, few-shot
- Measure the impact of each technique on output quality
- Extract structured data reliably with XML tags

## Prerequisites

- Lab 03 completed
- `anthropic` SDK installed

---

## Setup

```bash
mkdir ~/lab-04 && cd ~/lab-04
```

---

## Part 1: The Prompt Quality Ladder (20 min)

You'll send the same task with increasingly better prompts and compare results.

**The Task:** Classify customer support emails into categories.

Create `prompt_ladder.py`:

```python
import anthropic

client = anthropic.Anthropic()

TEST_EMAILS = [
    "I was charged twice for my subscription this month. Please fix this ASAP.",
    "The app crashes every time I try to upload a file larger than 10MB on my iPhone.",
    "I'd like to change the email address associated with my account.",
    "Your product has completely transformed our workflow. The new dashboard is amazing!",
    "Can you tell me when the next version will support dark mode? Also my invoice is wrong.",
]

def classify(prompt_template, email):
    prompt = prompt_template.replace("{{EMAIL}}", email)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


# --- Level 1: Vague ---
LEVEL_1 = "Classify this email: {{EMAIL}}"

# --- Level 2: Specific ---
LEVEL_2 = """Classify this customer support email into one of these categories:
billing, technical, account, feedback, other.

Email: {{EMAIL}}

Category:"""

# --- Level 3: XML Tags + Instructions ---
LEVEL_3 = """Classify the following customer support email into exactly one category.

<categories>
- billing: payment issues, charges, invoices, refunds, subscription plans
- technical: bugs, crashes, errors, performance issues, feature not working
- account: login, password, email change, profile updates, account deletion
- feedback: compliments, suggestions, feature requests (when not reporting a bug)
- other: anything that doesn't fit the above categories
</categories>

<email>
{{EMAIL}}
</email>

Respond with ONLY the category name, nothing else."""

# --- Level 4: Few-Shot ---
LEVEL_4 = """Classify the following customer support email into exactly one category.

<categories>
- billing: payment issues, charges, invoices, refunds, subscription plans
- technical: bugs, crashes, errors, performance issues, feature not working
- account: login, password, email change, profile updates, account deletion
- feedback: compliments, suggestions, feature requests (when not reporting a bug)
- other: anything that doesn't fit the above categories
</categories>

<examples>
<example>
<email>I need a refund for last month's charge.</email>
<category>billing</category>
</example>
<example>
<email>The search function returns no results even though I know the data exists.</email>
<category>technical</category>
</example>
<example>
<email>How do I reset my password?</email>
<category>account</category>
</example>
</examples>

<email>
{{EMAIL}}
</email>

Respond with ONLY the category name, nothing else."""


levels = [
    ("Level 1: Vague", LEVEL_1),
    ("Level 2: Specific", LEVEL_2),
    ("Level 3: XML + Instructions", LEVEL_3),
    ("Level 4: Few-Shot", LEVEL_4),
]

for level_name, template in levels:
    print(f"\n{'='*50}")
    print(f"  {level_name}")
    print(f"{'='*50}")
    for i, email in enumerate(TEST_EMAILS):
        result = classify(template, email)
        print(f"  Email {i+1}: {result}")
```

Run it: `python3 prompt_ladder.py`

**Discussion questions:**
- Which level first gives consistent single-word categories?
- How does the last email (mixed billing + feature request) get handled?
- What's the minimum level you'd ship in production?

---

## Part 2: XML Tags for Structured Extraction (10 min)

Create `extraction.py`:

```python
import anthropic

client = anthropic.Anthropic()

EXTRACT_PROMPT = """Extract structured information from the following job posting.

<job_posting>
We're looking for a Senior Backend Engineer to join our Platform team in San Francisco
or remotely (US only). You'll build and maintain our core API infrastructure serving
10M+ daily requests. Requirements: 5+ years Python/Go, experience with PostgreSQL and
Redis, familiarity with Kubernetes. Competitive salary $180K-$240K plus equity.
Benefits include unlimited PTO, 401k match, and health insurance.
</job_posting>

Return the extracted information in this exact format:

<extracted>
<title>[job title]</title>
<team>[team name]</team>
<location>[location, including remote policy]</location>
<experience>[years required]</experience>
<languages>[programming languages]</languages>
<technologies>[infrastructure/database technologies]</technologies>
<salary_range>[salary range]</salary_range>
<benefits>[comma-separated list]</benefits>
</extracted>"""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[{"role": "user", "content": EXTRACT_PROMPT}],
)

print(response.content[0].text)
```

**Your turn:** Modify `extraction.py` to extract from a different domain — a recipe, a bug report, or a meeting transcript.

---

## Part 3: Chain-of-Thought (15 min)

Create `chain_of_thought.py`:

```python
import anthropic

client = anthropic.Anthropic()

PROBLEM = """A store sells notebooks for $4 each and pens for $1.50 each.
Maria buys some notebooks and pens, spending exactly $23.
She buys more pens than notebooks.
How many of each did she buy? List all valid solutions."""

# Without chain-of-thought
response_direct = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[{"role": "user", "content": f"Solve this problem:\n{PROBLEM}"}],
)

# With chain-of-thought
response_cot = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"""Solve this problem step by step.

<problem>
{PROBLEM}
</problem>

Think through this carefully:
1. First, set up the equation
2. Then find all integer solutions where both values are positive
3. Finally, filter for the constraint that pens > notebooks

Show your work in <thinking> tags, then give the final answer in <answer> tags.""",
        }
    ],
)

print("=== WITHOUT Chain-of-Thought ===")
print(response_direct.content[0].text)
print("\n=== WITH Chain-of-Thought ===")
print(response_cot.content[0].text)
```

**Discussion:** When does chain-of-thought help? When is it overkill?

---

## Deliverables

- [ ] `prompt_ladder.py` — 4-level classification comparison
- [ ] `extraction.py` — XML-tagged structured extraction (modified for a new domain)
- [ ] `chain_of_thought.py` — CoT vs. direct comparison

## Stretch Goals

1. Add a Level 5 that uses a system prompt + few-shot + XML tags together
2. Build a prompt A/B tester that runs two prompts N times and compares consistency
3. Try the same prompts with Haiku — at what level does it match Sonnet?
