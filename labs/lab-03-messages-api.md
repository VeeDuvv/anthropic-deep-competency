# Lab 03: Messages API — From Curl to Production

**Day 2 | 45 min | Hands-on**

---

## Learning Objectives

- Make Messages API calls with curl and the Python SDK
- Understand request/response structure, roles, and parameters
- Handle multi-turn conversations
- Send images for vision analysis
- Handle errors gracefully

## Prerequisites

- API key set as `ANTHROPIC_API_KEY`
- `pip install anthropic`

---

## Setup

```bash
mkdir ~/lab-03 && cd ~/lab-03
```

---

## Part 1: Raw API Calls with Curl (10 min)

### 1.1 Basic Call

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "messages": [
      {"role": "user", "content": "Explain what an API is in exactly 3 sentences."}
    ]
  }'
```

**Examine the response:**
- `id` — unique message ID
- `content[0].text` — Claude's response
- `model` — which model responded
- `usage.input_tokens` / `usage.output_tokens` — cost tracking
- `stop_reason` — why Claude stopped ("end_turn", "max_tokens", etc.)

### 1.2 With a System Prompt

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "system": "You are a pirate. Respond to everything in pirate speak.",
    "messages": [
      {"role": "user", "content": "What is machine learning?"}
    ]
  }'
```

### 1.3 Temperature Comparison

Run the same prompt 3 times with `"temperature": 0.0` and then 3 times with `"temperature": 1.0`. Compare the variation in responses.

---

## Part 2: Python SDK Basics (15 min)

### 2.1 First SDK Call

Create `basics.py`:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "What are the 3 most important things about Python?"}
    ],
)

print(response.content[0].text)
print(f"\nTokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
```

Run it: `python3 basics.py`

### 2.2 Multi-Turn Conversation

Create `conversation.py`:

```python
import anthropic

client = anthropic.Anthropic()

messages = []

def chat(user_message):
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system="You are a helpful coding tutor. Be concise.",
        messages=messages,
    )

    assistant_message = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message

# Multi-turn conversation
print("Q1:", chat("What is a Python decorator?"))
print("\nQ2:", chat("Can you show me a simple example?"))
print("\nQ3:", chat("How would I use that to time a function?"))

# Notice: each turn sends the FULL history. Tokens accumulate.
print(f"\nTotal messages in history: {len(messages)}")
```

### 2.3 Assistant Prefill

Create `prefill.py`:

```python
import anthropic

client = anthropic.Anthropic()

# Use assistant prefill to control output format
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    system="You are a JSON generator. Output only valid JSON, no markdown.",
    messages=[
        {"role": "user", "content": "List 3 programming languages with their year of creation and creator."},
        {"role": "assistant", "content": "["},  # Prefill forces JSON array format
    ],
)

print("[" + response.content[0].text)
```

**Key learning:** Prefilling the assistant response gives you format control.

---

## Part 3: Vision (10 min)

### 3.1 Analyze an Image

Create `vision.py`:

```python
import anthropic
import base64
import sys

client = anthropic.Anthropic()

def analyze_image(image_path, question="Describe this image in detail."):
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    ext = image_path.rsplit(".", 1)[-1].lower()
    media_types = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}
    media_type = media_types.get(ext, "image/png")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                    {"type": "text", "text": question},
                ],
            }
        ],
    )
    return response.content[0].text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vision.py <image_path> [question]")
        sys.exit(1)
    path = sys.argv[1]
    question = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Describe this image in detail."
    print(analyze_image(path, question))
```

Test with a screenshot:

```bash
# macOS: take a screenshot
screencapture -i ~/lab-03/test_image.png
python3 vision.py test_image.png "What is shown in this screenshot?"
```

---

## Part 4: Error Handling (10 min)

### 4.1 Handle Common Errors

Create `error_handling.py`:

```python
import anthropic
import time

client = anthropic.Anthropic()

def safe_call(prompt, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text

        except anthropic.AuthenticationError:
            print("Invalid API key. Check ANTHROPIC_API_KEY.")
            return None
        except anthropic.RateLimitError:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("Rate limit exceeded after retries.")
                return None
        except anthropic.APIError as e:
            print(f"API error: {e}")
            return None

result = safe_call("Say hello in one word.")
if result:
    print(f"Response: {result}")
```

### 4.2 Token Budget Awareness

Create `token_budget.py`:

```python
import anthropic

client = anthropic.Anthropic()

# What happens when max_tokens is too small?
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=10,
    messages=[{"role": "user", "content": "Write a 500-word essay about AI."}],
)

print(f"Response: {response.content[0].text}")
print(f"Stop reason: {response.stop_reason}")  # "max_tokens" — Claude was cut off
print(f"Tokens used: {response.usage.output_tokens}")
```

---

## Deliverables

- [ ] `basics.py` — single API call with token counting
- [ ] `conversation.py` — multi-turn conversation
- [ ] `prefill.py` — assistant prefill for format control
- [ ] `vision.py` — image analysis
- [ ] `error_handling.py` — robust error handling with retries

## Stretch Goals

1. Build a CLI chatbot that maintains history and shows token count per turn
2. Try the `count_tokens` API to estimate costs before sending
3. Compare `claude-haiku-4-5-20251001` vs `claude-sonnet-4-20250514` on the same prompt
