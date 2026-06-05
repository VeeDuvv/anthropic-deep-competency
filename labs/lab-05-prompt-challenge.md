# Lab 05: Prompt Engineering Challenge

**Day 2 | 45 min | Competitive**

---

## Learning Objectives

- Apply prompt engineering under constraints
- Optimize for accuracy, consistency, and cost simultaneously
- Learn from other participants' approaches

## Prerequisites

- Labs 03-04 completed

---

## Setup

```bash
mkdir ~/lab-05 && cd ~/lab-05
```

---

## The Challenge

You have **3 tasks**. For each task, you must write a prompt that achieves the target accuracy on a test set. You're scored on:

1. **Accuracy** (60%) — correct outputs on test cases
2. **Consistency** (20%) — same output on repeated runs
3. **Efficiency** (20%) — fewer tokens = more points

---

## Task 1: Sentiment Scorer (15 min)

Write a prompt that classifies product reviews on a 1-5 scale.

Create `challenge_sentiment.py`:

```python
import anthropic

client = anthropic.Anthropic()

# --- YOUR PROMPT HERE ---
SYSTEM_PROMPT = ""  # Optional
USER_TEMPLATE = """
TODO: Write your prompt here.
The review text will replace {{REVIEW}}.
You must output ONLY a single digit 1-5.
"""
# --- END YOUR PROMPT ---

TEST_CASES = [
    ("Absolute garbage. Broke after one day. Want my money back.", 1),
    ("Not great. The quality is poor and shipping was slow.", 2),
    ("It's okay. Does what it says but nothing special.", 3),
    ("Really good product! A few minor issues but overall happy.", 4),
    ("Best purchase I've ever made. Exceeded all expectations. 10/10!", 5),
    ("Meh. It works I guess. Wouldn't buy again.", 2),
    ("Fantastic quality, fast shipping, great customer service!", 5),
    ("Terrible experience. Product was damaged and support was useless.", 1),
    ("Pretty decent for the price. Some room for improvement.", 3),
    ("Love it! My whole family uses it now. Already ordered a second one.", 5),
]

def score_review(review):
    prompt = USER_TEMPLATE.replace("{{REVIEW}}", review)
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": "claude-sonnet-4-20250514", "max_tokens": 10, "messages": messages}
    if SYSTEM_PROMPT:
        kwargs["system"] = SYSTEM_PROMPT
    response = client.messages.create(**kwargs)
    return response.content[0].text.strip()

correct = 0
for review, expected in TEST_CASES:
    result = score_review(review)
    match = "OK" if result == str(expected) else "MISS"
    if result == str(expected):
        correct += 1
    print(f"  [{match}] Expected={expected} Got={result} | {review[:50]}...")

print(f"\nAccuracy: {correct}/{len(TEST_CASES)} ({100*correct/len(TEST_CASES):.0f}%)")
```

**Target:** 8/10 correct (80%).

---

## Task 2: Entity Extractor (15 min)

Write a prompt that extracts person names, organizations, and locations from text.

Create `challenge_entities.py`:

```python
import anthropic
import json

client = anthropic.Anthropic()

# --- YOUR PROMPT HERE ---
USER_TEMPLATE = """
TODO: Write your prompt here.
The text will replace {{TEXT}}.
You must output valid JSON with keys: persons, organizations, locations.
Each value is a list of strings.
"""
# --- END YOUR PROMPT ---

TEST_CASES = [
    {
        "text": "Tim Cook announced at Apple's headquarters in Cupertino that the company would partner with OpenAI.",
        "expected": {"persons": ["Tim Cook"], "organizations": ["Apple", "OpenAI"], "locations": ["Cupertino"]},
    },
    {
        "text": "The United Nations held a summit in Geneva where Secretary-General Antonio Guterres spoke about climate change.",
        "expected": {"persons": ["Antonio Guterres"], "organizations": ["United Nations"], "locations": ["Geneva"]},
    },
    {
        "text": "Dr. Sarah Chen from MIT published her research in Nature about CRISPR applications at her lab in Cambridge.",
        "expected": {"persons": ["Sarah Chen"], "organizations": ["MIT", "Nature"], "locations": ["Cambridge"]},
    },
]

def extract_entities(text):
    prompt = USER_TEMPLATE.replace("{{TEXT}}", text)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "{"},
        ],
    )
    raw = "{" + response.content[0].text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  JSON parse error: {raw[:100]}")
        return {"persons": [], "organizations": [], "locations": []}

for tc in TEST_CASES:
    result = extract_entities(tc["text"])
    print(f"\nText: {tc['text'][:60]}...")
    print(f"  Expected: {tc['expected']}")
    print(f"  Got:      {result}")
    # Score: check if all expected entities are found
    for key in ["persons", "organizations", "locations"]:
        expected_set = set(tc["expected"][key])
        result_set = set(result.get(key, []))
        found = expected_set & result_set
        missed = expected_set - result_set
        if missed:
            print(f"  Missed {key}: {missed}")
```

**Target:** Extract all entities from all 3 test cases.

---

## Task 3: Code Reviewer (15 min)

Write a prompt that identifies bugs in Python code and suggests fixes.

Create `challenge_reviewer.py`:

```python
import anthropic

client = anthropic.Anthropic()

# --- YOUR PROMPT HERE ---
USER_TEMPLATE = """
TODO: Write your prompt here.
The code will replace {{CODE}}.
Output format: one JSON array of objects with keys: line, bug, fix
"""
# --- END YOUR PROMPT ---

TEST_CASES = [
    {
        "code": '''def divide_list(numbers, divisor):
    results = []
    for n in numbers:
        results.append(n / divisor)
    return results

data = [10, 20, 30, 0, 50]
print(divide_list(data, 0))''',
        "bugs": ["division by zero"],
    },
    {
        "code": '''def find_user(users, name):
    for user in users:
        if user["name"] == name:
            return user
    return user  # bug: returns last user instead of None

result = find_user([], "Alice")
print(result["email"])''',
        "bugs": ["returns last user instead of None", "accessing email on potentially None result"],
    },
    {
        "code": '''import json

def load_config(path):
    f = open(path)
    data = json.load(f)
    return data["settings"]["theme"]''',
        "bugs": ["file not closed", "no error handling for missing keys", "no error handling for missing file"],
    },
]

def review_code(code):
    prompt = USER_TEMPLATE.replace("{{CODE}}", code)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

for i, tc in enumerate(TEST_CASES):
    print(f"\n{'='*50}")
    print(f"  Code Sample {i+1}")
    print(f"{'='*50}")
    result = review_code(tc["code"])
    print(result)
    print(f"\n  Expected bugs: {tc['bugs']}")
```

**Target:** Identify at least 1 bug per code sample.

---

## Scoring

When done, share your prompts with the group. Facilitators will run all prompts against a hidden extended test set.

| Metric | Weight | How Measured |
|--------|--------|-------------|
| Accuracy | 60% | Correct outputs on hidden test set |
| Consistency | 20% | Run 3 times, same result each time |
| Efficiency | 20% | Total input + output tokens (lower = better) |

---

## Deliverables

- [ ] `challenge_sentiment.py` with your prompt (80%+ accuracy)
- [ ] `challenge_entities.py` with your prompt (all entities found)
- [ ] `challenge_reviewer.py` with your prompt (all bugs found)

## Discussion

After scoring:
- Which prompting techniques worked best for each task?
- Where did extra specificity help vs. hurt?
- How much did few-shot examples improve consistency?
