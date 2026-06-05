# Lab 02: CLAUDE.md Mastery + Slash Commands

**Day 1 | 30 min | Hands-on**

---

## Learning Objectives

- Write an effective CLAUDE.md that shapes Claude Code's behavior
- See the before/after difference a CLAUDE.md makes
- Create a custom slash command
- Understand the CLAUDE.md hierarchy (project, user, workspace)

## Prerequisites

- Lab 01 completed (working `word_counter` project)

---

## Part 1: CLAUDE.md Impact (10 min)

### 1.1 Baseline: No CLAUDE.md

Navigate to your lab-01 project:

```bash
cd ~/lab-01
```

Start Claude Code and ask it to add a new feature:

```bash
claude "Add a function to count the average word length in the text file"
```

Note the coding style Claude uses (variable names, comments, docstrings, etc.).

### 1.2 Add a CLAUDE.md

Create a CLAUDE.md in the project root:

```bash
cat > CLAUDE.md << 'EOF'
# Word Counter Project

## Coding Standards
- Use snake_case for all functions and variables
- Every function must have a Google-style docstring
- Use type hints on all function signatures
- Keep functions under 20 lines
- Use pathlib.Path instead of os.path
- Prefer list comprehensions over map/filter

## Project Context
- This is a CLI tool for text analysis
- Target audience: data analysts who are not Python experts
- Error messages should be user-friendly, not stack traces
- All output should be formatted for terminal readability

## Testing
- Use pytest for all tests
- Test files go in tests/ directory
- Aim for one test per function, plus edge cases
EOF
```

### 1.3 See the Difference

Now ask the same thing again:

```bash
claude "Add a function to count the average word length in the text file"
```

**Compare:**
- Does the new code have type hints?
- Does it have a Google-style docstring?
- Does it use pathlib?
- Is the function under 20 lines?

### 1.4 Test the Boundaries

Try asking Claude to do something that conflicts with your CLAUDE.md:

```bash
claude "Add a function using os.path to check if the file exists"
```

Does Claude follow your CLAUDE.md and use pathlib instead?

---

## Part 2: Custom Slash Commands (15 min)

### 2.1 Create a Command Directory

```bash
mkdir -p ~/lab-01/.claude/commands
```

### 2.2 Write a Review Command

Create a slash command that reviews code quality:

```bash
cat > ~/lab-01/.claude/commands/review.md << 'EOF'
Review the current project for code quality issues. Check for:

1. Functions missing type hints
2. Functions missing docstrings
3. Functions longer than 20 lines
4. Any use of os.path (should be pathlib)
5. Missing error handling for file I/O
6. Hardcoded values that should be constants

For each issue found, show the file, line number, and a suggested fix.
Format as a checklist with [ ] for each issue.
EOF
```

### 2.3 Use the Command

```bash
cd ~/lab-01
claude
```

In the session, type:

```
/review
```

Claude runs your custom review command against the project. Review the output.

### 2.4 Create a Test Generator Command

```bash
cat > ~/lab-01/.claude/commands/generate-tests.md << 'EOF'
Look at all Python files in this project. For each function that doesn't have
a corresponding test, generate a test in the tests/ directory.

Requirements:
- Use pytest
- Include at least one happy-path test and one edge case per function
- Use descriptive test names: test_<function_name>_<scenario>
- Add a conftest.py with any shared fixtures

Create the tests/ directory if it doesn't exist.
EOF
```

Test it:

```
/generate-tests
```

### 2.5 Run the Generated Tests

Exit Claude Code and run:

```bash
pip install pytest
python3 -m pytest tests/ -v
```

---

## Part 3: CLAUDE.md Hierarchy (5 min)

### 3.1 Understand the Layers

Claude Code reads CLAUDE.md from multiple locations (highest to lowest priority):

1. **Project:** `./CLAUDE.md` (repo root) — project-specific rules
2. **User:** `~/.claude/CLAUDE.md` — your personal preferences across all projects
3. **Workspace parent:** `../CLAUDE.md` — shared rules for a directory of repos

### 3.2 Check Your User-Level CLAUDE.md

```bash
cat ~/.claude/CLAUDE.md
```

If it exists, read it. If not, consider creating one with your personal coding preferences.

---

## Deliverables

- [ ] A CLAUDE.md that demonstrably changes Claude's coding behavior
- [ ] At least one working custom slash command
- [ ] Generated tests that pass

## Stretch Goals

1. Create a `/document` slash command that generates README sections for the project
2. Create a `/security` slash command that checks for common security issues
3. Add a `.claude/commands/commit.md` that creates well-formatted commit messages
