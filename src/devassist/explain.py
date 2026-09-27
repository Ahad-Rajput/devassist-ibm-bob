"""`devassist explain <file>` — print a plain-English summary of a source file."""

import os
import re


def cmd_explain(filepath):
    """Print a plain-English summary of a source file."""
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        return

    with open(filepath, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    total_lines = len(lines)
    code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith("#"))
    comment_lines = sum(1 for l in lines if l.strip().startswith("#"))

    functions = [l for l in lines if re.match(r"\s*def ", l)]
    classes = [l for l in lines if re.match(r"\s*class ", l)]
    imports = [l.strip() for l in lines if re.match(r"\s*(import |from .+ import)", l)]

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
