# claude-md-viewer

> Zero-dependency HTML navigator for Claude Code context files.  
> Browse, search and read your `CLAUDE.md` and memory files — **one file, offline, no build step.**

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Zero dependencies](https://img.shields.io/badge/dependencies-zero-blue)
![Works offline](https://img.shields.io/badge/offline-yes-brightgreen)

---

## What it does

When you work with [Claude Code](https://claude.ai/code), your context lives in `.md` files scattered across your project. `claude_md_viewer.html` turns that folder into a **searchable, navigable knowledge base** — like a streaming catalog for your own brain.

- **One HTML file.** Drop it anywhere. Open in any browser.
- **No server, no npm, no Python.** Pure vanilla JS.
- **Full-text search** across all your `.md` files instantly.
- **Dark mode** by default.
- **Works with any `.md` structure** — not just Claude Code.

---

## Demo

Open `claude_md_viewer.html` directly in your browser → [Live demo via GitHub Pages](https://virgil-libria.github.io/claude-md-viewer/)

---

## Quick start

```bash
# 1. Clone or download
git clone https://github.com/visioncreativeflow/claude-md-viewer.git

# 2. Drop claude_md_viewer.html into your project root
cp claude-md-viewer/claude_md_viewer.html ./

# 3. Open it
open claude_md_viewer.html   # macOS
start claude_md_viewer.html  # Windows
xdg-open claude_md_viewer.html  # Linux
```

That's it. No install. No config.

---

## Who it's for

| Use case | How it helps |
|---|---|
| **Claude Code users** | Navigate your `CLAUDE.md`, memory files and context docs in one place |
| **PKM practitioners** | Browse Obsidian-style vaults without Obsidian |
| **Developers** | Searchable local documentation with zero overhead |
| **AI-agnostic workflows** | Works with files from Claude, GPT, Gemini — any `.md` output |

---

## The "Point Zero" philosophy

This tool is built on a simple principle: **your files own your context, not the AI.**

The viewer is a window into your local filesystem. The AI is a processor. You are the operator.  
Switch AI providers tomorrow — your `.md` files stay, your knowledge stays.

---

## File structure (recommended)

```
your-project/
├── claude_md_viewer.html     ← drop here
├── CLAUDE.md                 ← main context file
├── memory/
│   ├── projects.md
│   ├── decisions.md
│   └── glossary.md
└── technical/
    └── architecture.md
```

---

## Contributing

PRs welcome. Keep it zero-dependency. Keep it one file.

---

## License

MIT — do whatever you want with it.

---

*Built in a single session. Shipped because it works.*
