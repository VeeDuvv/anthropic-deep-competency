# Lab 11: Build a Custom MCP Server

**Day 4 | 60 min | Hands-on**

---

## Learning Objectives

- Understand MCP architecture: hosts, clients, servers, transports
- Build a custom MCP server in Python that exposes domain-specific tools
- Register the server with Claude Code
- Test the server with real Claude Code interactions

## Prerequisites

- Claude Code installed and authenticated
- `pip install mcp`
- Basic understanding of tool use (Labs 07-08)

---

## Setup

```bash
mkdir ~/lab-11 && cd ~/lab-11
pip install mcp
```

---

## Part 1: MCP Architecture (10 min)

### Quick Review

```
┌─────────────┐     ┌──────────┐     ┌──────────────────┐
│  Claude Code │────▶│  Client  │────▶│   MCP Server     │
│  (Host)      │     │          │     │                  │
│              │◀────│          │◀────│  - Tools         │
│              │     │          │     │  - Resources     │
└─────────────┘     └──────────┘     │  - Prompts       │
                                     └──────────────────┘
```

- **Host:** Claude Code (or any application embedding Claude)
- **Client:** Manages the connection to one server
- **Server:** Provides tools, resources, and/or prompts
- **Transport:** How they communicate (stdio for local, HTTP for remote)

---

## Part 2: Build a Project Notes Server (30 min)

We'll build an MCP server that manages project notes — a simple but practical tool.

### 2.1 Create the Server

Create `notes_server.py`:

```python
#!/usr/bin/env python3
"""MCP Server: Project Notes Manager

Provides tools for creating, reading, searching, and listing project notes.
Each note is a JSON file stored in a configurable directory.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Notes directory — configurable via environment variable
NOTES_DIR = Path(os.environ.get("NOTES_DIR", os.path.expanduser("~/lab-11/notes")))
NOTES_DIR.mkdir(parents=True, exist_ok=True)

server = Server("project-notes")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="create_note",
            description="Create a new project note with a title and body. Notes are timestamped automatically.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Note title (used as filename)"},
                    "body": {"type": "string", "description": "Note content (supports markdown)"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization",
                        "default": [],
                    },
                },
                "required": ["title", "body"],
            },
        ),
        Tool(
            name="read_note",
            description="Read a note by its title.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Note title to read"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="list_notes",
            description="List all notes with their titles, dates, and tags.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="search_notes",
            description="Search notes by keyword (searches title, body, and tags).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="delete_note",
            description="Delete a note by its title.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Note title to delete"},
                },
                "required": ["title"],
            },
        ),
    ]


def _note_path(title: str) -> Path:
    safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in title)
    safe_name = safe_name.strip().replace(" ", "-").lower()
    return NOTES_DIR / f"{safe_name}.json"


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "create_note":
        title = arguments["title"]
        path = _note_path(title)
        note = {
            "title": title,
            "body": arguments["body"],
            "tags": arguments.get("tags", []),
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
        }
        path.write_text(json.dumps(note, indent=2))
        return [TextContent(type="text", text=f"Note created: {title}")]

    elif name == "read_note":
        path = _note_path(arguments["title"])
        if not path.exists():
            return [TextContent(type="text", text=f"Note not found: {arguments['title']}")]
        note = json.loads(path.read_text())
        return [TextContent(type="text", text=f"# {note['title']}\n\nTags: {', '.join(note.get('tags', []))}\nCreated: {note['created']}\n\n{note['body']}")]

    elif name == "list_notes":
        notes = []
        for f in sorted(NOTES_DIR.glob("*.json")):
            note = json.loads(f.read_text())
            tags = ", ".join(note.get("tags", []))
            notes.append(f"- {note['title']} [{tags}] ({note['created'][:10]})")
        if not notes:
            return [TextContent(type="text", text="No notes found.")]
        return [TextContent(type="text", text="\n".join(notes))]

    elif name == "search_notes":
        query = arguments["query"].lower()
        matches = []
        for f in NOTES_DIR.glob("*.json"):
            note = json.loads(f.read_text())
            searchable = f"{note['title']} {note['body']} {' '.join(note.get('tags', []))}".lower()
            if query in searchable:
                matches.append(f"- {note['title']}: {note['body'][:100]}...")
        if not matches:
            return [TextContent(type="text", text=f"No notes matching '{arguments['query']}'")]
        return [TextContent(type="text", text=f"Found {len(matches)} match(es):\n" + "\n".join(matches))]

    elif name == "delete_note":
        path = _note_path(arguments["title"])
        if not path.exists():
            return [TextContent(type="text", text=f"Note not found: {arguments['title']}")]
        path.unlink()
        return [TextContent(type="text", text=f"Deleted: {arguments['title']}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 2.2 Test the Server Standalone

```bash
# Quick sanity check — server should start and wait for input
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":{}}}' | python3 notes_server.py
# Press Ctrl+C to exit
```

---

## Part 3: Register with Claude Code (10 min)

### 3.1 Add the Server

```bash
claude mcp add project-notes -s user -- python3 $(pwd)/notes_server.py
```

### 3.2 Verify It Works

```bash
claude
```

In the Claude Code session:

```
List all my MCP tools
```

You should see `create_note`, `read_note`, `list_notes`, `search_notes`, and `delete_note` in the list.

### 3.3 Use It

```
Create a note titled "Lab 11 Progress" with body "Built my first MCP server! It manages project notes with CRUD operations." and tags ["mcp", "lab", "learning"]
```

Then:

```
List all my notes
```

Then:

```
Search my notes for "MCP"
```

---

## Part 4: Add a Resource (10 min)

### 4.1 Expose Notes as Resources

Add this to `notes_server.py` before the `main()` function:

```python
from mcp.types import Resource

@server.list_resources()
async def list_resources():
    resources = []
    for f in sorted(NOTES_DIR.glob("*.json")):
        note = json.loads(f.read_text())
        resources.append(Resource(
            uri=f"notes://{f.stem}",
            name=note["title"],
            description=f"Note: {note['title']} ({note['created'][:10]})",
            mimeType="text/markdown",
        ))
    return resources

@server.read_resource()
async def read_resource(uri: str):
    # uri format: notes://note-name
    note_name = uri.replace("notes://", "")
    path = NOTES_DIR / f"{note_name}.json"
    if not path.exists():
        return f"Note not found: {note_name}"
    note = json.loads(path.read_text())
    return f"# {note['title']}\n\n{note['body']}"
```

**Resources vs Tools:**
- **Tools** are actions (create, delete, search)
- **Resources** are data (files, documents, database records) that Claude can read

---

## Deliverables

- [ ] `notes_server.py` — working MCP server with 5 tools + resources
- [ ] Server registered with Claude Code
- [ ] Successfully created and searched notes via Claude Code

## Stretch Goals

1. Add a `summarize_notes` tool that concatenates all notes for a given tag
2. Add note templates: `create_note_from_template` with predefined structures (meeting, decision, bug)
3. Build a second MCP server for a different domain (bookmarks, tasks, or contacts) and register both
