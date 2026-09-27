"""File-tree walking helpers shared by the `structure` and `docs` commands."""

import os

from .constants import IGNORED_DIRS, SOURCE_EXTENSIONS


def tree_lines(root, exclude_files=None):
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
            connector = "└── " if idx == len(entries) - 1 else "├── "
            ext_prefix = "    " if idx == len(entries) - 1 else "│   "
            yield f"{prefix}{connector}{name}{'/' if is_dir else ''}"
            if is_dir:
                yield from _walk(os.path.join(dirpath, name), prefix + ext_prefix)

    folder = os.path.basename(os.path.abspath(root))
    yield f"{folder}/"
    yield from _walk(root, "")


def iter_source_files(root, exts=SOURCE_EXTENSIONS):
    """Yield (rel_path, abs_path) for every source file under root."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in sorted(filenames):
            if any(fname.endswith(ext) for ext in exts):
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(abs_path, root)
                yield rel_path, abs_path
