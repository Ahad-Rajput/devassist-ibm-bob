# DevAssist

**AI-powered developer workflow assistant — CLI prototype**
Built for the **IBM Bob 2.0 Hackathon** by **Team THE CODERS**

DevAssist is a small Python command-line tool that inspects a codebase and
gives a developer a quick, structured view of it: a visual file tree, a
plain-English breakdown of a source file, a scan for common code issues, and
auto-generated project documentation.

## Features

| Command     | What it does                                                        |
|-------------|----------------------------------------------------------------------|
| `structure` | Prints a visual tree of a project directory                          |
| `explain`   | Summarizes a source file (line/function/class/import counts)         |
| `issues`    | Scans a file for common problems (bare `except`, TODOs, long lines, missing docstrings) |
| `docs`      | Generates a `DOCS.md` file summarizing the whole project              |

## Project structure

```
devassist-ibm-bob/
├── pyproject.toml          # uv/hatchling project config, console entry point
├── README.md
├── src/
│   └── devassist/
│       ├── __init__.py
│       ├── cli.py          # argparse entry point, wires subcommands together
│       ├── constants.py    # shared constants (ignored dirs, source extensions)
│       ├── tree.py         # tree-rendering + source-file walking helpers
│       ├── structure.py    # `structure` command
│       ├── explain.py      # `explain` command
│       ├── issues.py       # `issues` command
│       └── docs.py         # `docs` command
├── sample_project/         # small demo project used to try the CLI out on
│   ├── main.py
│   └── utils.py
└── bob_sessions/           # IBM Bob 2.0 Hackathon required evidence screenshots
```

## Setup with `uv`

[uv](https://docs.astral.sh/uv/) is used for dependency management, the
virtual environment, and running the CLI.

```bash
# Install dependencies and create the virtual environment
uv sync

# Run the CLI through uv (no manual venv activation needed)
uv run devassist structure ./sample_project
uv run devassist explain   ./sample_project/utils.py
uv run devassist issues    ./sample_project/utils.py
uv run devassist docs      ./sample_project
```

Alternatively, install it as an editable package and call it directly:

```bash
uv pip install -e .
devassist structure ./sample_project
```

## Example

```bash
$ uv run devassist structure ./sample_project

📁 Project structure: /path/to/sample_project

  sample_project/
  ├── main.py
  └── utils.py
```

```bash
$ uv run devassist issues ./sample_project/utils.py

🔍 Issues found in: ./sample_project/utils.py

  Line   16: Unresolved annotation (TODO/FIXME/HACK/XXX)
           ↳ # FIXME: status comparison should be case-insensitive

  Line   22: Bare except clause — catches all exceptions including KeyboardInterrupt
           ↳ except:

  Total: 2 issue(s) found.
```

## Development

Run tests (if/when added under `tests/`) with:

```bash
uv run pytest
```

## Hackathon notes

This project was built with IBM Bob 2.0 for planning, implementation,
debugging, code review, and documentation. Session evidence (screenshots of
completed Bob task summaries) is kept in [`bob_sessions/`](./bob_sessions),
alongside a supplementary write-up in `bob_sessions/session_01.md`.
