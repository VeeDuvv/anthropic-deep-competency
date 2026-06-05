# Lab 01: Claude Code Basics

**Day 1 | 45 min | Hands-on**

---

## Learning Objectives

- Launch Claude Code and navigate core commands
- Use Claude Code to scaffold a project from scratch
- Experience the plan → build → test workflow
- Understand how Claude Code reads, edits, and creates files

## Prerequisites

- Claude Code installed and authenticated (pre-work steps 1-2)
- A terminal open in your home directory

---

## Part 1: Orientation (10 min)

### 1.1 Launch Claude Code

```bash
mkdir ~/lab-01 && cd ~/lab-01
git init
claude
```

You're now in an interactive Claude Code session.

### 1.2 Explore Built-in Commands

Try each of these inside the Claude Code session:

```
/help
/status
/model
```

- `/help` — shows available commands
- `/status` — shows current context (files read, tokens used)
- `/model` — shows which Claude model you're talking to

### 1.3 Ask Claude About Itself

Type this prompt:

```
What tools do you have access to? List them briefly.
```

Notice how Claude describes its file reading, editing, searching, and shell execution capabilities.

---

## Part 2: Scaffold a Project (20 min)

### 2.1 Build a Python Project from a Single Prompt

Type this into Claude Code:

```
Create a Python project called "word_counter" that:
1. Has a main.py that reads a text file and counts word frequencies
2. Has a sample.txt with 3 paragraphs of placeholder text
3. Has a requirements.txt (no external deps needed)
4. Prints the top 10 most common words with their counts
5. Accepts the filename as a command-line argument
```

**Watch what happens:**
- Claude creates multiple files in sequence
- It uses the Write tool for new files
- It may run the code to verify it works

### 2.2 Verify the Output

After Claude finishes, exit the session (`/exit` or Ctrl+C) and check:

```bash
ls -la
cat main.py
python3 main.py sample.txt
```

**Questions to consider:**
- Did Claude create all the files you asked for?
- Does the code run without errors?
- Is the code style clean and readable?

### 2.3 Modify the Project

Start a new Claude Code session and ask for changes:

```bash
claude
```

```
Modify main.py to also:
1. Accept an optional --ignore-case flag
2. Accept an optional --min-count N flag that only shows words appearing N+ times
3. Add a --help flag with usage instructions
Use argparse.
```

**Watch how Claude:**
- Reads the existing file before editing
- Uses the Edit tool (not rewriting the whole file)
- May run the modified code to test it

### 2.4 Test the Changes

```bash
python3 main.py sample.txt --ignore-case --min-count 2
python3 main.py --help
```

---

## Part 3: Plan Mode (15 min)

### 3.1 Enter Plan Mode

```bash
claude
```

Type `/plan` to enter plan mode. Now ask:

```
I want to add a web interface to word_counter using Flask. The user uploads a text file,
and the page shows a bar chart of the top 20 words. Plan this out before building anything.
```

**In plan mode, Claude will:**
- Analyze the existing codebase
- Propose an architecture
- List files to create/modify
- NOT make any changes yet

### 3.2 Review the Plan

Read Claude's plan carefully. Then type:

```
Go ahead and implement the plan.
```

Claude exits plan mode and starts building. Watch the file creation and editing.

### 3.3 Test the Web App

```bash
pip install flask
python3 app.py
```

Open the URL in your browser and upload `sample.txt`.

---

## Deliverables

- [ ] A working `word_counter` project with CLI arguments
- [ ] A Flask web interface (if time permits)
- [ ] Experience with Claude Code's read → edit → run workflow
- [ ] Experience with plan mode

## Stretch Goals

If you finish early:

1. Ask Claude Code to add unit tests with pytest
2. Ask Claude Code to add a `Dockerfile` that containerizes the app
3. Try: `claude "Refactor main.py to separate the counting logic into a module called counter.py"`

---

## Facilitator Notes

- Most participants will complete Parts 1-2 in 30 min. Part 3 is stretch.
- Common issue: Flask not installed. Have participants `pip install flask` before the web step.
- If anyone's Claude Code isn't working, pair them with a neighbor and debug during the break.
