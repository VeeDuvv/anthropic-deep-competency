#!/usr/bin/env python3
"""Anthropic Deep Competency Program — Environment Verification Script.

Run this script to verify your development environment is ready for Day 1.
It checks Python, the Anthropic SDK, API key, Claude Code CLI, and live API calls.

Usage:
    python3 verify_setup.py
    python3 verify_setup.py --skip-api    # skip live API calls (offline check only)
    python3 verify_setup.py --verbose      # show detailed output
    python3 verify_setup.py --help
"""

import argparse
import json
import os
import shutil
import subprocess
import sys


def color(text, code):
    """Apply ANSI color if terminal supports it."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def green(text):
    return color(text, "32")


def red(text):
    return color(text, "31")


def yellow(text):
    return color(text, "33")


def bold(text):
    return color(text, "1")


def check_python_version(verbose=False):
    """Check that Python >= 3.10 is installed."""
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v.major == 3 and v.minor >= 10:
        return True, f"Python {version_str}", None
    else:
        return (
            False,
            f"Python {version_str} (need 3.10+)",
            "Install Python 3.10+:\n"
            "  macOS:   brew install python@3.12\n"
            "  Ubuntu:  sudo apt install python3.12\n"
            "  Windows: download from python.org\n"
            "  Any:     pyenv install 3.12",
        )


def check_anthropic_sdk(verbose=False):
    """Check that the anthropic Python SDK is installed and importable."""
    try:
        import anthropic

        version = getattr(anthropic, "__version__", "unknown")
        return True, f"anthropic SDK v{version}", None
    except ImportError:
        return (
            False,
            "anthropic SDK not found",
            "Install with:\n"
            "  pip install anthropic\n"
            "  # or: pip3 install anthropic\n"
            "  # or: python3 -m pip install anthropic",
        )


def check_api_key(verbose=False):
    """Check that ANTHROPIC_API_KEY is set."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        masked = key[:7] + "..." + key[-4:] if len(key) > 15 else "***"
        if key.startswith("sk-ant-"):
            return True, f"API key set ({masked})", None
        else:
            return (
                False,
                f"API key set but looks malformed ({masked})",
                "Your ANTHROPIC_API_KEY should start with 'sk-ant-'.\n"
                "Get a valid key from console.anthropic.com > API Keys.",
            )
    else:
        return (
            False,
            "ANTHROPIC_API_KEY not set",
            "Set your API key:\n"
            '  export ANTHROPIC_API_KEY="sk-ant-your-key-here"\n'
            "  Add the above line to ~/.zshrc or ~/.bashrc and restart your terminal.\n"
            "  Get a key from console.anthropic.com > API Keys.",
        )


def check_claude_code_cli(verbose=False):
    """Check that Claude Code CLI is installed and responds."""
    claude_path = shutil.which("claude")
    if not claude_path:
        return (
            False,
            "Claude Code CLI not found",
            "Install with:\n"
            "  npm install -g @anthropic-ai/claude-code@latest\n"
            "If npm not found, install Node.js 18+ first:\n"
            "  macOS: brew install node\n"
            "  Other: download from nodejs.org",
        )

    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        version = result.stdout.strip() or result.stderr.strip()
        if result.returncode == 0 and version:
            return True, f"Claude Code CLI v{version}", None
        else:
            return (
                False,
                "Claude Code CLI found but --version failed",
                f"Output: {version}\n"
                "Try reinstalling: npm install -g @anthropic-ai/claude-code@latest",
            )
    except subprocess.TimeoutExpired:
        return (
            False,
            "Claude Code CLI timed out",
            "The 'claude --version' command timed out.\n"
            "Try running it manually to diagnose the issue.",
        )
    except Exception as e:
        return (
            False,
            f"Claude Code CLI error: {e}",
            "Try running 'claude --version' manually to diagnose.",
        )


def check_messages_api(verbose=False):
    """Make a test Messages API call."""
    try:
        import anthropic
    except ImportError:
        return False, "Cannot test API (SDK not installed)", "Install anthropic SDK first."

    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return False, "Cannot test API (no API key)", "Set ANTHROPIC_API_KEY first."

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Reply with exactly: VERIFICATION_OK"}],
        )
        reply = response.content[0].text.strip()
        if verbose:
            print(f"    API response: {reply}")
        return True, "Messages API call succeeded", None
    except anthropic.AuthenticationError:
        return (
            False,
            "Messages API: authentication failed",
            "Your API key is invalid or expired.\n"
            "Generate a new key at console.anthropic.com > API Keys.",
        )
    except anthropic.RateLimitError:
        return (
            False,
            "Messages API: rate limited",
            "You're being rate-limited. Wait a minute and try again.\n"
            "Check your plan limits at console.anthropic.com.",
        )
    except anthropic.APIConnectionError as e:
        return (
            False,
            "Messages API: connection error",
            f"Cannot reach the Anthropic API: {e}\n"
            "Check your internet connection and any proxy/firewall settings.",
        )
    except Exception as e:
        return (
            False,
            f"Messages API: unexpected error — {e}",
            "Try running a manual curl test (see pre-work packet).",
        )


def check_tool_use(verbose=False):
    """Make a test tool use API call."""
    try:
        import anthropic
    except ImportError:
        return False, "Cannot test tool use (SDK not installed)", "Install anthropic SDK first."

    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return False, "Cannot test tool use (no API key)", "Set ANTHROPIC_API_KEY first."

    tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ]

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            tools=tools,
            messages=[
                {"role": "user", "content": "What's the weather in New York City?"}
            ],
        )

        tool_used = any(block.type == "tool_use" for block in response.content)
        if tool_used:
            tool_block = next(b for b in response.content if b.type == "tool_use")
            if verbose:
                print(f"    Tool called: {tool_block.name}({json.dumps(tool_block.input)})")
            return True, "Tool use API call succeeded", None
        else:
            return (
                True,
                "Tool use API call succeeded (model responded without tool call, but API works)",
                None,
            )
    except anthropic.AuthenticationError:
        return (
            False,
            "Tool use API: authentication failed",
            "Your API key is invalid or expired.",
        )
    except Exception as e:
        return (
            False,
            f"Tool use API: unexpected error — {e}",
            "Check your API key and internet connection.",
        )


def main():
    parser = argparse.ArgumentParser(
        description="Anthropic Deep Competency Program — Environment Verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run all checks to verify your setup before Day 1.\n"
        "Submit the output (screenshot or copy-paste) to the facilitator channel.",
    )
    parser.add_argument(
        "--skip-api",
        action="store_true",
        help="Skip live API calls (check local setup only)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output for each check",
    )
    args = parser.parse_args()

    print()
    print(bold("=" * 60))
    print(bold("  Anthropic Deep Competency Program"))
    print(bold("  Environment Verification"))
    print(bold("=" * 60))
    print()

    checks = [
        ("Python 3.10+", check_python_version),
        ("Anthropic Python SDK", check_anthropic_sdk),
        ("API Key (ANTHROPIC_API_KEY)", check_api_key),
        ("Claude Code CLI", check_claude_code_cli),
    ]

    if not args.skip_api:
        checks.append(("Messages API Call", check_messages_api))
        checks.append(("Tool Use API Call", check_tool_use))

    results = []

    for name, check_fn in checks:
        passed, detail, fix = check_fn(verbose=args.verbose)
        results.append((name, passed, detail, fix))

        status = green("PASS") if passed else red("FAIL")
        print(f"  [{status}] {name}")
        print(f"         {detail}")

        if not passed and fix:
            print()
            for line in fix.split("\n"):
                print(f"         {yellow(line)}")
            print()

    # Summary
    total = len(results)
    passed = sum(1 for _, p, _, _ in results if p)
    failed = total - passed

    print()
    print(bold("-" * 60))
    if failed == 0:
        print(green(bold(f"  ALL {total} CHECKS PASSED")))
        print()
        print("  Your environment is ready for Day 1!")
        print("  Submit a screenshot of this output to the facilitator channel.")
    else:
        print(red(bold(f"  {failed} of {total} CHECKS FAILED")))
        print()
        print("  Fix the issues above and re-run this script.")
        print("  If you're stuck, reach out on the #anthropic-deep-competency channel.")
    print(bold("-" * 60))
    print()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
