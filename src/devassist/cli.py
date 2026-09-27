"""DevAssist CLI entry point.

Usage:
    devassist structure <path>
    devassist explain   <file>
    devassist issues    <file>
    devassist docs      <path>
"""

import argparse

from .structure import cmd_structure
from .explain import cmd_explain
from .issues import cmd_issues
from .docs import cmd_docs


def build_parser():
    parser = argparse.ArgumentParser(
        prog="devassist",
        description="DevAssist — AI-powered developer workflow assistant",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_struct = sub.add_parser("structure", help="Print a visual file tree")
    p_struct.add_argument("path", help="Project directory")

    p_explain = sub.add_parser("explain", help="Explain a source file")
    p_explain.add_argument("file", help="Source file path")

    p_issues = sub.add_parser("issues", help="Scan a file for code issues")
    p_issues.add_argument("file", help="Source file path")

    p_docs = sub.add_parser("docs", help="Generate DOCS.md for a project")
    p_docs.add_argument("path", help="Project directory")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "structure":
        cmd_structure(args.path)
    elif args.command == "explain":
        cmd_explain(args.file)
    elif args.command == "issues":
        cmd_issues(args.file)
    elif args.command == "docs":
        cmd_docs(args.path)


if __name__ == "__main__":
    main()
