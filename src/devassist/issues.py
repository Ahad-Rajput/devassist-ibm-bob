"""`devassist issues <file>` — scan a file for common code issues."""

import os
import re


def cmd_issues(filepath):
    """Scan a file for common code issues."""
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        return

    with open(filepath, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    issues = []

    for i, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n")

        if re.search(r"\bexcept\s*:", stripped):
            issues.append((
                i,
                "Bare except clause — catches all exceptions including KeyboardInterrupt",
                stripped.strip(),
            ))

        if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", stripped, re.IGNORECASE):
            issues.append((i, "Unresolved annotation (TODO/FIXME/HACK/XXX)", stripped.strip()))

        if len(stripped) > 120:
            issues.append((
                i,
                f"Line too long ({len(stripped)} chars, max recommended 120)",
                stripped.strip()[:80] + "…",
            ))

        if re.match(r"\s*def ", stripped):
            # Check if next non-empty line is a docstring
            rest = lines[i:]  # lines after this def
            for next_line in rest:
                if next_line.strip():
                    if not next_line.strip().startswith('"""') and not next_line.strip().startswith("'''"):
                        issues.append((i, "Function missing docstring", stripped.strip()))
                    break

    print(f"\n🔍 Issues found in: {filepath}\n")
    if not issues:
        print("  ✅ No issues detected.\n")
        return

    for lineno, message, snippet in issues:
        print(f"  Line {lineno:>4}: {message}")
        print(f"           ↳ {snippet}\n")

    print(f"  Total: {len(issues)} issue(s) found.\n")
