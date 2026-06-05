# Lab 06: Build a Streaming Chat App

**Day 2 | 45 min | Hands-on**

---

## Learning Objectives

- Implement streaming responses with the Anthropic SDK
- Use prompt caching to reduce costs on repeated context
- Build a functional terminal chat application
- Understand token economics: counting, caching, model routing

## Prerequisites

- Labs 03-04 completed
- `anthropic` SDK installed

---

## Setup

```bash
mkdir ~/lab-06 && cd ~/lab-06
```

---

## Part 1: Streaming Basics (10 min)

### 1.1 Your First Stream

Create `stream_basic.py`:

```python
import anthropic

client = anthropic.Anthropic()

print("Claude: ", end="", flush=True)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[{"role": "user", "content": "Explain how streaming APIs work in 3 paragraphs."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # newline at the end

# Access the final message for usage stats
final = stream.get_final_message()
print(f"\nTokens: {final.usage.input_tokens} in, {final.usage.output_tokens} out")
```

Run it: `python3 stream_basic.py`

Watch the text appear word-by-word instead of all at once.

### 1.2 Stream Events

Create `stream_events.py`:

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[{"role": "user", "content": "Write a haiku about programming."}],
) as stream:
    for event in stream:
        # See all the event types
        print(f"Event: {event.type}")
        if hasattr(event, "delta") and hasattr(event.delta, "text"):
            print(f"  Text: {event.delta.text!r}")
```

**Key events:**
- `message_start` — message metadata (model, usage estimate)
- `content_block_start` — beginning of a content block
- `content_block_delta` — chunk of text
- `content_block_stop` — end of a content block
- `message_stop` — message complete

---

## Part 2: Prompt Caching (15 min)

### 2.1 Cache a Large System Prompt

Create `caching.py`:

```python
import anthropic
import time

client = anthropic.Anthropic()

# A large system prompt (imagine this is a full style guide or knowledge base)
LARGE_SYSTEM = """You are an expert Python code reviewer. Here is your complete review checklist:

""" + "\n".join([f"- Rule {i}: Check for common Python anti-pattern #{i} and suggest improvements." for i in range(1, 101)])

# This makes the system prompt large enough to cache (1024+ tokens for Sonnet)

def ask_with_cache(question, use_cache=True):
    system_content = [
        {
            "type": "text",
            "text": LARGE_SYSTEM,
            **({"cache_control": {"type": "ephemeral"}} if use_cache else {}),
        }
    ]

    start = time.time()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        system=system_content,
        messages=[{"role": "user", "content": question}],
    )
    elapsed = time.time() - start

    usage = response.usage
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0

    print(f"  Time: {elapsed:.2f}s")
    print(f"  Input tokens: {usage.input_tokens}")
    print(f"  Cache creation: {cache_create}")
    print(f"  Cache read: {cache_read}")
    print(f"  Output tokens: {usage.output_tokens}")
    print(f"  Response: {response.content[0].text[:100]}...")
    return response

# First call: creates the cache
print("=== Call 1 (cache creation) ===")
ask_with_cache("Review this code: x = [i for i in range(100)]")

# Second call: reads from cache (should be faster and cheaper)
print("\n=== Call 2 (cache read) ===")
ask_with_cache("Review this code: def foo(): pass")

# Third call: confirms cache reuse
print("\n=== Call 3 (cache read) ===")
ask_with_cache("Review this code: import os; os.system('rm -rf /')")
```

Run it: `python3 caching.py`

**Look for:**
- Call 1: `cache_creation` tokens > 0, `cache_read` = 0
- Calls 2-3: `cache_creation` = 0, `cache_read` > 0

**Cost savings:** Cache reads are 90% cheaper than normal input tokens.

---

## Part 3: Terminal Chat App (20 min)

### 3.1 Build the Chat

Create `chat.py`:

```python
import anthropic
import sys

client = anthropic.Anthropic()

SYSTEM_PROMPT = "You are a helpful assistant. Be concise but thorough."

def chat():
    messages = []
    total_input = 0
    total_output = 0

    print("Chat with Claude (type 'quit' to exit, 'clear' to reset)")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            messages.clear()
            total_input = 0
            total_output = 0
            print("Conversation cleared.")
            continue

        messages.append({"role": "user", "content": user_input})

        print("\nClaude: ", end="", flush=True)

        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

        print()

        messages.append({"role": "assistant", "content": full_response})

        final = stream.get_final_message()
        total_input += final.usage.input_tokens
        total_output += final.usage.output_tokens

        print(f"  [{final.usage.input_tokens} in / {final.usage.output_tokens} out | "
              f"session: {total_input} in / {total_output} out | "
              f"{len(messages)} messages]")

    # Session summary
    print(f"\n{'='*50}")
    print(f"Session totals: {total_input} input + {total_output} output tokens")
    print(f"Messages exchanged: {len(messages)}")

if __name__ == "__main__":
    chat()
```

Run it: `python3 chat.py`

### 3.2 Add Prompt Caching to the Chat

Modify `chat.py` to cache the system prompt. Change the `system` parameter:

```python
system=[
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

Ask multiple questions and watch the cache read tokens appear.

---

## Deliverables

- [ ] `stream_basic.py` — streaming response
- [ ] `caching.py` — prompt caching with cost comparison
- [ ] `chat.py` — terminal chat with streaming and token tracking

## Stretch Goals

1. Add a `--model` flag to `chat.py` that lets you switch models mid-conversation
2. Add conversation export: type `save` to write the conversation to a JSON file
3. Add a `--cache-system` flag that loads a large file as additional system context with caching
