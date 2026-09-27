# DevAssist

> An AI-assisted developer workflow prototype built with **IBM Bob 2.0** for the IBM Bob 2.0 Hackathon.

## 🎯 Problem

Developers working with unfamiliar codebases can spend significant time understanding project structure, reading source files, identifying issues, and preparing documentation.

## 💡 Solution

**DevAssist** is a zero-dependency Python CLI that helps developers:

| Command | What it does |
|---|---|
| `structure` | Print a visual file tree of any project |
| `explain` | Summarise a source file (classes, functions, imports, line counts) |
| `issues` | Scan a file for common problems (bare excepts, TODOs, long lines, missing docstrings) |
| `docs` | Auto-generate a `DOCS.md` file for an entire project |

## 🚀 Quick Start

Requires Python 3; uses only the standard library (no external package dependencies).

```bash
# 1. See the project structure
python src/devassist.py structure sample_project

# 2. Explain a source file
python src/devassist.py explain sample_project/utils.py

# 3. Find code issues
python src/devassist.py issues sample_project/utils.py

# 4. Generate documentation
python src/devassist.py docs sample_project
```

## 🧠 IBM Bob

**IBM Bob IDE is a core part of this project.**

Bob was used for:

* Project planning & design decisions
* Writing all source code (`src/devassist.py`)
* Creating the demo project (`sample_project/`)
* Generating documentation
* Session logging (`bob_sessions/`)

## 🛠️ Technology

* Python 3 (stdlib only — no pip install needed)
* IBM Bob 2.0 IDE
* GitHub

## 📂 Project Structure

```text
devassist-ibm-bob/
├── bob_sessions/
│   └── session_01.md      # IBM Bob session evidence log
├── sample_project/
│   ├── main.py            # Demo project entry point
│   └── utils.py           # Demo utilities (includes intentional issues for demo)
├── src/
│   └── devassist.py       # Main CLI tool
└── README.md
```

## 🎬 Demo

Running `issues` against the sample project detects real problems:

```
🔍 Issues found in: sample_project/utils.py

  Line  18: Function missing docstring
           ↳ def filter_by_status(tasks, status):

  Line  19: Unresolved annotation (TODO/FIXME/HACK/XXX)
           ↳ # FIXME: status comparison should be case-insensitive

  Line  23: Function missing docstring
           ↳ def summarise(tasks):

  Line  28: Bare except clause — catches all exceptions including KeyboardInterrupt
           ↳ except:

  Total: 4 issue(s) found.
```

## 🚧 Status

**Working Prototype** — Built for the IBM Bob 2.0 Hackathon.

## 👥 Team

**THE CODERS**
