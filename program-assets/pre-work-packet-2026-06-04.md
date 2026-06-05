# Pre-Work Packet: Anthropic Deep Competency Program

**US Cohort 1 | New York City | June 22 – July 3, 2026**

---

Welcome to the Anthropic Deep Competency Program. You've been selected as one of 12 practitioners for our inaugural immersive training cohort. Over two weeks, you'll gain hands-on mastery of Claude and build a real AI product as a team -- developing the deep competency bench that positions our firm for an Anthropic partnership.

This pre-work packet ensures you walk into Day 1 (Monday, June 22) ready to code. No setup friction, no waiting for installs -- just hands on keyboards from the start.

---

## Timeline

| Tier | Deadline | Effort | Requirement |
| Tier 1: Required | **June 20 (Friday)** | ~4 hours | Must complete to attend |
| Tier 2: Recommended | **June 21 (Saturday)** | ~4 hours | Strongly encouraged |
| Tier 3: Optional | Before June 22 | ~4 hours | For those who want a head start |

**Total estimated effort: 8-12 hours spread over 4-5 days.**

---

## Tier 1: Required (~4 hours)

**You cannot attend without completing these tasks. Submit all verification items by Friday, June 13.**

### 1. Account Setup (30 min)

**Claude.ai Account**

- Go to claude.ai and sign in (or create an account)
- You should have a Pro or Team plan -- facilitators will confirm your plan access
- Verify you can start a conversation with Claude

**API Key**

- Go to console.anthropic.com
- Navigate to **API Keys** in the left sidebar
- Click **Create Key**, name it something like `deep-competency-prework`
- Copy the key and save it securely (you will not be able to see it again)
- Set it as an environment variable:

**macOS/Linux (add to your ~/.zshrc or ~/.bashrc):**

```
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Then run `source ~/.zshrc` (or `source ~/.bashrc`).

**Windows (PowerShell):**

```
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-your-key-here", "User")
```

Restart your terminal after setting the variable.

**Verify your API key works:**

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Say hello in exactly 5 words."}]
  }'
```

You should see a JSON response with Claude's reply. If you get an authentication error, double-check your key.

### 2. Claude Code Installation (30 min)

**Install Node.js 18+**

- Check if you have it: `node --version`
- If not installed or below v18, download from nodejs.org or use your package manager:
  - macOS: `brew install node`
  - Ubuntu/Debian: `sudo apt install nodejs npm`
  - Windows: Download the installer from nodejs.org

**Install Claude Code**

```bash
npm install -g @anthropic-ai/claude-code@latest
```

**Verify installation:**

```bash
claude --version
```

You should see a version number (e.g., `1.x.x`).

**Authenticate:**

```bash
claude auth login
```

Follow the prompts to log in with your Anthropic account.

**Run your first task:**

```bash
claude "What version of Claude am I talking to?"
```

Claude should respond with its model information.

**Set up CLAUDE.md:**

Create a test repo and add a CLAUDE.md file:

```bash
mkdir ~/claude-prework && cd ~/claude-prework
git init
echo "# Test Project\nThis is a test project for the Anthropic Deep Competency Program pre-work." > CLAUDE.md
claude "Read my CLAUDE.md and tell me what you see."
```

### 3. Anthropic Academy -- Core Courses (2 hours)

Complete the following courses on **anthropic.skilljar.com**:

- **Claude 101** -- Covers Claude's capabilities, use cases, and basic interaction patterns
- **Anthropic API Fundamentals** (6 modules) -- How to use the Messages API, parameters, streaming, and error handling

**What to submit:** Completion certificates or screenshots showing course completion status.

### 4. Environment Verification (30 min)

We've provided a verification script that checks your entire setup. Download and run it:

```bash
# Download the script (facilitators will share the link via Slack/Teams)
# Or copy verify_setup.py from the shared drive

python3 verify_setup.py
```

The script checks:

- Python 3.10+ installed
- `anthropic` Python SDK installed and importable
- API key present (environment variable)
- Claude Code CLI installed and responds
- A test Messages API call succeeds
- A test tool use call succeeds

**If you don't have the anthropic SDK:**

```bash
pip install anthropic
```

**What to submit:** Screenshot or copy-paste of the script output showing all checks PASS. If any check fails, the script provides fix instructions -- follow them and re-run.

### 5. Pre-Reading (30 min)

Read the following documentation:

- **Intro to Claude** -- docs.anthropic.com/en/docs/intro-to-claude
  - Understand Claude's architecture, capabilities, and limitations
- **Messages API** -- docs.anthropic.com/en/api/messages
  - Understand the request/response format, roles, and parameters

Skim the **Claude Competency Domains Overview** (1-page summary provided by facilitators). This gives you a preview of the five skill areas we'll cover in Week 1.

---

## Tier 2: Recommended (~4 hours)

**Completing these tasks will make your Week 1 significantly more productive. Strongly encouraged by Saturday, June 14.**

### 6. Anthropic Academy -- Advanced Courses (2 hours)

Complete the following on **anthropic.skilljar.com**:

- **Introduction to MCP** -- Model Context Protocol: how Claude connects to external tools and data sources
- **Claude Code 101** -- Deep dive into Claude Code workflows, commands, and best practices
- **Tool Use & Agents** -- How to define tools, handle tool calls, and build agentic workflows

### 7. MCP Server Setup (1 hour)

MCP (Model Context Protocol) lets Claude Code access external tools and data. Install these three starter servers:

**Filesystem Server** (read/write project files):

```bash
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem ~/claude-prework
```

**GitHub Server** (PRs, issues, code search):

```bash
claude mcp add github -s user -- npx -y @modelcontextprotocol/server-github
```

Note: Set `GITHUB_PERSONAL_ACCESS_TOKEN` env var with a GitHub PAT that has `repo` scope.

**Fetch Server** (web pages, documentation):

```bash
claude mcp add fetch -s user -- npx -y @modelcontextprotocol/server-fetch
```

**Verify MCP works:**

```bash
cd ~/claude-prework
claude "Use the filesystem MCP server to list files in this directory."
```

Claude should use the MCP tool to list your files instead of running a shell command.

### 8. Hands-On Mini-Exercise: Build Something Small (1 hour)

Use Claude Code to build a small Python CLI tool that calls the Claude API.

**Requirements:**

- Uses the Messages API to send a prompt and display the response
- Includes a system prompt that gives Claude a specific persona
- Implements at least one tool (e.g., a calculator, a weather lookup stub, or a file reader)
- Runs from the command line with `python3 your_tool.py "your question"`

**How to build it:**

```bash
cd ~/claude-prework
claude "Build me a Python CLI tool called ask_claude.py that:
1. Takes a user question as a command-line argument
2. Has a system prompt making Claude act as a helpful coding assistant
3. Defines a 'calculate' tool that evaluates math expressions
4. Sends the question to Claude, handles any tool calls, and prints the final response
Use the anthropic Python SDK and argparse."
```

**What to submit:** The repo link (if on GitHub) or a zip of `~/claude-prework/`.

---

## Tier 3: Optional (~4 hours)

**For those who want to explore before Day 1. Self-directed, no submission required.**

### 9. Anthropic Cookbook Exploration (1 hour)

Browse the Anthropic Cookbook at github.com/anthropics/anthropic-cookbook. Try 1-2 recipes that interest you:

- RAG (Retrieval-Augmented Generation) example
- Classification patterns
- Summarization techniques
- Extended thinking

### 10. Advanced Prompt Engineering (2 hours)

Deepen your prompting skills ahead of Week 1:

- Complete the **Prompt Engineering Interactive Tutorial** at github.com/anthropics/courses
- Complete the **Real World Prompting** course
- Review the 5 Claude competency domains (overview provided by facilitators):
  - Domain 1: Claude Fundamentals
  - Domain 2: Prompt Engineering
  - Domain 3: Tool Use and Agents
  - Domain 4: Enterprise Integration
  - Domain 5: Safety and Responsible AI

### 11. Advanced Claude Code Exploration (1 hour)

Experiment with power-user features:

- **CLAUDE.md mastery:** Set up a CLAUDE.md with custom instructions, coding standards, and project context in a real project
- **Plan mode:** Try `claude` then type `/plan` to enter plan mode. Ask Claude to architect a feature before building it
- **Custom slash commands:** Create a `.claude/commands/` directory and add a custom command markdown file

---

## Verification Checklist

Submit the following to the facilitator Slack/Teams channel by **Friday, June 13**:

| Item | How to Submit |
| 1. API key verification | Screenshot of successful curl response |
| 2. Claude Code version | Output of `claude --version` |
| 3. Claude Code first task | Screenshot of Claude responding to your query |
| 4. Academy -- Claude 101 | Completion certificate or screenshot |
| 5. Academy -- API Fundamentals | Completion certificate or screenshot |
| 6. verify_setup.py output | Screenshot showing all checks PASS |
| 7. (Tier 2) Academy advanced courses | Completion certificates or screenshots |
| 8. (Tier 2) MCP verification | Screenshot of Claude using an MCP tool |
| 9. (Tier 2) Mini-exercise | Repo link or zip file |

---

## Troubleshooting FAQ

**Q: I can't install Node.js / npm is not recognized**

- macOS: Install Homebrew first (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`), then `brew install node`
- Windows: Download the LTS installer from nodejs.org. Make sure to check "Add to PATH" during installation
- Linux: Use your distro's package manager or install via nvm (`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash`)

**Q: `claude` command not found after npm install**

- Try: `npx @anthropic-ai/claude-code@latest --version`
- If that works, your npm global bin isn't in PATH. Run `npm config get prefix` and add `<prefix>/bin` to your PATH
- Alternative: Use `npx @anthropic-ai/claude-code@latest` instead of `claude` for all commands

**Q: API key not working / authentication error**

- Verify the key starts with `sk-ant-`
- Make sure you copied the full key (they're long)
- Check that `echo $ANTHROPIC_API_KEY` prints your key (restart terminal after setting it)
- Ensure your API account has credits/an active plan at console.anthropic.com

**Q: `pip install anthropic` fails**

- Try: `pip3 install anthropic` or `python3 -m pip install anthropic`
- If permission error: `pip install --user anthropic`
- If pip not found: Install pip with `python3 -m ensurepip --upgrade`

**Q: Claude Code auth login fails**

- Make sure you have a Claude.ai account (not just an API account)
- Try logging out and back in: `claude auth logout` then `claude auth login`
- Check your internet connection and any corporate proxy settings

**Q: MCP servers fail to start**

- Ensure npx is available: `npx --version`
- Try running the MCP server command manually to see error output
- For GitHub MCP: ensure your `GITHUB_PERSONAL_ACCESS_TOKEN` is set and has `repo` scope
- Check Claude Code logs: `claude --debug`

**Q: Python version is below 3.10**

- macOS: `brew install python@3.12`
- Ubuntu: `sudo apt install python3.12`
- Windows: Download from python.org
- Use pyenv for managing multiple Python versions: `pyenv install 3.12`

**Q: Corporate firewall/proxy blocking installs**

- Ask your IT team for proxy settings
- For npm: `npm config set proxy http://proxy.company.com:8080`
- For pip: `pip install --proxy http://proxy.company.com:8080 anthropic`
- If GitHub is blocked, facilitators can provide offline packages

---

## Need Help?

If you're stuck on any setup step:

- **Slack/Teams channel:** #anthropic-deep-competency (facilitators monitor daily)
- **Email:** deep-competency-support@company.com
- **Office hours:** Thursday June 12, 3-5pm ET (virtual drop-in for setup help)

Don't struggle alone -- reach out early so we can resolve issues before Day 1.

---

*See you in NYC on June 22. Come ready to build.*
