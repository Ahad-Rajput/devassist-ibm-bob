"""
DevAssist - AI-powered developer workflow assistant
IBM Bob 2.0 Hackathon | Team: THE CODERS

Usage:
    python devassist.py structure <path>
    python devassist.py explain   <file>
    python devassist.py issues    <file>
    python devassist.py docs      <path>
"""

import os
import re
import argparse
from datetime import datetime

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea', '.vscode'}


def _tree_lines(root, exclude_files=None):
    """Yield lines of a properly-connected file tree under root.

    Uses ├── for non-last siblings and └── for the last sibling at each level.
    exclude_files: optional set of bare filenames to omit from every directory.
    """
    exclude_files = exclude_files or set()

    def _walk(dirpath, prefix):
        entries_dirs = sorted(
            d for d in os.listdir(dirpath)
            if os.path.isdir(os.path.join(dirpath, d)) and d not in IGNORED_DIRS
        )
        entries_files = sorted(
            f for f in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, f)) and f not in exclude_files
        )
        entries = [(d, True) for d in entries_dirs] + [(f, False) for f in entries_files]

        for idx, (name, is_dir) in enumerate(entries):
            connector = '└── ' if idx == len(entries) - 1 else '├── '
            ext_prefix = '    ' if idx == len(entries) - 1 else '│   '
            yield f"{prefix}{connector}{name}{'/' if is_dir else ''}"
            if is_dir:
                yield from _walk(os.path.join(dirpath, name), prefix + ext_prefix)

    folder = os.path.basename(os.path.abspath(root))
    yield f"{folder}/"
    yield from _walk(root, '')


def iter_source_files(root, exts=('.py', '.js', '.ts', '.java', '.c', '.cpp', '.rb', '.go')):
    """Yield (rel_path, abs_path) for every source file under root."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in sorted(filenames):
            if any(fname.endswith(ext) for ext in exts):
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(abs_path, root)
                yield rel_path, abs_path


# ---------------------------------------------------------------------------
# Command: structure
# ---------------------------------------------------------------------------

def cmd_structure(path):
    """Print a visual file tree of the project."""
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory.")
        return

    print(f"\n📁 Project structure: {os.path.abspath(path)}\n")
    for line in _tree_lines(path):
        print(f"  {line}")
    print()


# ---------------------------------------------------------------------------
# Command: explain
# ---------------------------------------------------------------------------

def cmd_explain(filepath):
    """Print a plain-English summary of a source file."""
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        return

    with open(filepath, encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    total_lines = len(lines)
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
    comment_lines = sum(1 for l in lines if l.strip().startswith('#'))

    functions = [l for l in lines if re.match(r'\s*def ', l)]
    classes = [l for l in lines if re.match(r'\s*class ', l)]
    imports = [l.strip() for l in lines if re.match(r'\s*(import |from .+ import)', l)]

    print(f"\n📄 File explanation: {filepath}\n")
    print(f"  Total lines   : {total_lines}")
    print(f"  Code lines    : {code_lines}")
    print(f"  Comment lines : {comment_lines}")
    print(f"  Classes       : {len(classes)}")
    print(f"  Functions     : {len(functions)}")

    if classes:
        print("\n  Classes defined:")
        for c in classes:
            print(f"    • {c.strip()}")

    if functions:
        print("\n  Functions defined:")
        for fn in functions:
            print(f"    • {fn.strip()}")

    if imports:
        print("\n  Imports:")
        for imp in imports[:10]:
            print(f"    • {imp}")
        if len(imports) > 10:
            print(f"    … and {len(imports) - 10} more")

    print()


# ---------------------------------------------------------------------------
# Command: issues
# ---------------------------------------------------------------------------

def cmd_issues(filepath):
    """Scan a file for common code issues."""
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        return

    with open(filepath, encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    issues = []

    for i, line in enumerate(lines, start=1):
        stripped = line.rstrip('\n')

        if re.search(r'\bexcept\s*:', stripped):
            issues.append((i, 'Bare except clause — catches all exceptions including KeyboardInterrupt', stripped.strip()))

        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', stripped, re.IGNORECASE):
            issues.append((i, 'Unresolved annotation (TODO/FIXME/HACK/XXX)', stripped.strip()))

        if len(stripped) > 120:
            issues.append((i, f'Line too long ({len(stripped)} chars, max recommended 120)', stripped.strip()[:80] + '…'))

        if re.match(r'\s*def ', stripped):
            # Check if next non-empty line is a docstring
            rest = lines[i:]  # lines after this def
            for next_line in rest:
                if next_line.strip():
                    if not next_line.strip().startswith('"""') and not next_line.strip().startswith("'''"):
                        issues.append((i, 'Function missing docstring', stripped.strip()))
                    break

    print(f"\n🔍 Issues found in: {filepath}\n")
    if not issues:
        print("  ✅ No issues detected.\n")
        return

    for lineno, message, snippet in issues:
        print(f"  Line {lineno:>4}: {message}")
        print(f"           ↳ {snippet}\n")

    print(f"  Total: {len(issues)} issue(s) found.\n")


# ---------------------------------------------------------------------------
# Command: docs
# ---------------------------------------------------------------------------

def cmd_docs(path):
    """Generate a DOCS.md file summarising the project."""
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory.")
        return

    output_path = os.path.join(path, 'DOCS.md')
    lines_out = []

    project_name = os.path.basename(os.path.abspath(path))
    lines_out.append(f"# {project_name} — Auto-generated Documentation\n\n")
    lines_out.append(f"_Generated by DevAssist on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
    lines_out.append("---\n\n## Project Structure\n\n```\n")

    for line in _tree_lines(path, exclude_files={'DOCS.md'}):
        lines_out.append(f"  {line}\n")

    lines_out.append("```\n\n---\n\n## File Summaries\n\n")

    for rel_path, abs_path in iter_source_files(path):
        with open(abs_path, encoding='utf-8', errors='replace') as f:
            src_lines = f.readlines()

        functions = [l.strip() for l in src_lines if re.match(r'\s*def ', l)]
        classes = [l.strip() for l in src_lines if re.match(r'\s*class ', l)]

        lines_out.append(f"### `{rel_path}`\n\n")
        lines_out.append(f"- **Lines:** {len(src_lines)}\n")
        lines_out.append(f"- **Classes:** {len(classes)}\n")
        lines_out.append(f"- **Functions:** {len(functions)}\n")

        if classes:
            lines_out.append(f"- **Defined classes:** {', '.join(c.replace('class ', '').split('(')[0].strip() for c in classes)}\n")
        if functions:
            lines_out.append(f"- **Defined functions:** {', '.join(f.replace('def ', '').split('(')[0].strip() for f in functions)}\n")

        lines_out.append("\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines_out)

    print(f"\n📝 Documentation written to: {output_path}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='devassist',
        description='DevAssist — AI-powered developer workflow assistant'
    )
    sub = parser.add_subparsers(dest='command', required=True)

    p_struct = sub.add_parser('structure', help='Print a visual file tree')
    p_struct.add_argument('path', help='Project directory')

    p_explain = sub.add_parser('explain', help='Explain a source file')
    p_explain.add_argument('file', help='Source file path')

    p_issues = sub.add_parser('issues', help='Scan a file for code issues')
    p_issues.add_argument('file', help='Source file path')

    p_docs = sub.add_parser('docs', help='Generate DOCS.md for a project')
    p_docs.add_argument('path', help='Project directory')

    args = parser.parse_args()

    if args.command == 'structure':
        cmd_structure(args.path)
    elif args.command == 'explain':
        cmd_explain(args.file)
    elif args.command == 'issues':
        cmd_issues(args.file)
    elif args.command == 'docs':
        cmd_docs(args.path)


if __name__ == '__main__':
    main()
