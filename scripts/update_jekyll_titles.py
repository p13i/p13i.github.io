#!/usr/bin/env python3
"""
update_jekyll_titles.py

Scan a folder of Jekyll Markdown files and set/reset the YAML `title:` field based on the Markdown content
(after front matter). The resulting title contains only alphanumeric characters (Unicode), space, period (.)
and comma (,). Whitespace is normalized. The output title is at most 64 characters; if truncation occurs the
script uses a 3-character ASCII ellipsis "..." as the last 3 characters (so final length <= 64).

Usage:
    python3 update_jekyll_titles.py /path/to/folder [--recursive] [--backup] [--dry-run] [--ext .md .markdown] [--max-len 64]

Examples:
    python3 update_jekyll_titles.py ./_posts --recursive --backup
    python3 update_jekyll_titles.py ./posts --dry-run --ext .md .markdown

Notes:
- The script expects YAML front matter delimited by '---' on the first line, and a closing '---'.
- If no front matter is present the script will create one and place the new title there.
- No external packages required.
"""

from __future__ import annotations
import argparse
import re
from pathlib import Path
import shutil
import sys
from typing import Tuple, Optional

ELLIPSIS = "..."
DEFAULT_MAX_LEN = 64
DEFAULT_EXTS = {".md", ".markdown"}


def extract_front_matter_and_content(text: str) -> Tuple[Optional[str], str]:
    """
    If text begins with a YAML front matter block delimited by '---' on its own line,
    return (yaml_body, content_after_front_matter). Otherwise return (None, original_text).
    """
    # Match front matter only at the start of the file
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n)?", text, flags=re.DOTALL)
    if m:
        yaml_body = m.group(1)
        rest = text[m.end() :]
        return yaml_body, rest
    else:
        return None, text


def remove_existing_title_from_yaml(yaml_text: str) -> str:
    """
    Remove any existing `title:` entry from yaml_text, including multiline wrapped values.
    """
    if yaml_text is None:
        return ""
    # Remove any line that begins with 'title:' (leading whitespace allowed). Use multiline.
    cleaned = re.sub(r"(?im)^[ \t]*title[ \t]*:[ \t]*.*(?:\n|$)", "", yaml_text)
    # Strip leading/trailing newlines/spaces
    return cleaned.strip()


def compute_title_from_content(
    content: str, fallback: str, max_len: int = DEFAULT_MAX_LEN
) -> str:
    """
    Compute the title from content. Steps:
      1. Remove fenced code blocks, inline code, HTML comments, simple HTML tags, and reference-style link defs.
      2. Collapse whitespace to single spaces.
      3. Keep only characters that are (a) Unicode alphanumeric, or (b) space, or (c) period '.' or (d) comma ','.
      4. Collapse repeated spaces and strip.
      5. If empty after filtering, fall back to a sanitized filename-derived string.
      6. Truncate to max_len; if truncation needed, produce a final string that is max_len with '...' as the last 3 chars.
    """
    if content is None:
        content = ""

    # Remove fenced code blocks ``` ... ```
    s = re.sub(r"```.*?```", " ", content, flags=re.DOTALL)
    # Remove inline code `...`
    s = re.sub(r"`[^`]*`", " ", s)
    # Remove HTML comments <!-- ... -->
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.DOTALL)
    # Remove simple HTML tags <...>
    s = re.sub(r"<[^>]+>", " ", s)
    # Remove reference-style link definitions like: [id]: http://...
    s = re.sub(
        r"(?m)^\s*$begin:math:display$[^$end:math:display$]+\]:\s*\S+.*$", " ", s
    )

    # Normalize whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # Keep only allowed characters: Unicode alphanumeric OR space OR '.' OR ','
    allowed_chars = []
    for ch in s:
        if ch.isalnum() or ch in (" ", ".", ","):
            allowed_chars.append(ch)
    filtered = "".join(allowed_chars)
    # Collapse spaces again
    filtered = re.sub(r" {2,}", " ", filtered).strip()

    if not filtered:
        filtered = fallback

    if not filtered:
        filtered = "untitled"

    if len(filtered) <= max_len:
        return filtered
    else:
        if max_len <= len(ELLIPSIS):
            return ELLIPSIS[:max_len]
        head_len = max_len - len(ELLIPSIS)
        truncated = filtered[:head_len].rstrip()
        if not truncated:
            truncated = filtered[:head_len]
        return truncated + ELLIPSIS


def yaml_quote(value: str) -> str:
    """
    Minimal safe double-quoting for YAML scalar: escape backslashes and double quotes.
    We assume the content contains no line breaks (title generation strips them).
    """
    v = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{v}"'


def sanitize_filename_for_fallback(name: str) -> str:
    base = Path(name).stem
    chars = []
    for ch in base:
        if ch.isalnum() or ch in (" ", ".", ","):
            chars.append(ch)
        else:
            chars.append(" ")
    s = "".join(chars)
    s = re.sub(r"\s+", " ", s).strip()
    return s or base or "untitled"


import shutil
import yaml
from pathlib import Path
from typing import Tuple


def process_file(
    path: Path,
    max_len: int = DEFAULT_MAX_LEN,
    make_backup: bool = False,
    dry_run: bool = False,
) -> Tuple[bool, str, str]:
    """
    Process a single file. Returns a tuple (changed: bool, old_title_repr, new_title_repr).
    """
    text = path.read_text(encoding="utf-8")
    yaml_body, content = extract_front_matter_and_content(text)

    # Parse YAML safely
    try:
        front_matter = yaml.safe_load(yaml_body) if yaml_body else {}
    except Exception as e:
        print(f"Skipping {path}: YAML parse error {e}")
        return False, "", ""

    if front_matter is None:
        front_matter = {}

    # Old title (whatever YAML parsed it to)
    old_title = str(front_matter.get("title", "")).strip()

    # Compute new title
    fallback = sanitize_filename_for_fallback(path.name)
    new_title_plain = compute_title_from_content(content, fallback, max_len=max_len)

    # Update front matter
    front_matter["title"] = new_title_plain

    # Dump YAML with preserved ordering (title first)
    # Note: sort_keys=False preserves insertion order of dict
    # We want `title` at the top
    items = [("title", front_matter.pop("title"))] + list(
        front_matter.items()
    )
    ordered_front_matter = {k: v for k, v in items}

    new_yaml = yaml.dump(
        ordered_front_matter,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).strip()

    new_text = f"---\n{new_yaml}\n---\n\n"
    # Keep original leading/trailing whitespace of content
    if content.startswith("\n"):
        new_text += content.lstrip("\n")
    else:
        new_text += content

    changed = text != new_text
    if changed and not dry_run:
        if make_backup:
            bak = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, bak)
        path.write_text(new_text, encoding="utf-8")

    return changed, old_title, new_title_plain


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Set/reset YAML title fields for Jekyll Markdown posts based on content."
    )
    p.add_argument(
        "folder", type=Path, help="Folder containing Markdown files to process."
    )
    p.add_argument(
        "--recursive", "-r", action="store_true", help="Search recursively (rglob)."
    )
    p.add_argument(
        "--backup",
        "-b",
        action="store_true",
        help="Create a .bak copy next to each file before modifying.",
    )
    p.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Do not write changes; only report what would change.",
    )
    p.add_argument(
        "--ext",
        nargs="+",
        default=list(DEFAULT_EXTS),
        help="File extensions to process (default: .md .markdown).",
    )
    p.add_argument(
        "--max-len",
        type=int,
        default=DEFAULT_MAX_LEN,
        help="Maximum title length (default 64).",
    )
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose output.")
    args = p.parse_args(argv)

    folder = args.folder
    if not folder.exists() or not folder.is_dir():
        print(
            f"Error: folder '{folder}' does not exist or is not a directory.",
            file=sys.stderr,
        )
        sys.exit(2)

    exts = {
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.ext
    }
    files = []
    if args.recursive:
        files = [
            pth
            for pth in folder.rglob("*")
            if pth.is_file() and pth.suffix.lower() in exts
        ]
    else:
        files = [
            pth
            for pth in folder.iterdir()
            if pth.is_file() and pth.suffix.lower() in exts
        ]

    if not files:
        print("No matching markdown files found.")
        return

    changed_count = 0
    for f in sorted(files):
        try:
            changed, old_title, new_title = process_file(
                f, max_len=args.max_len, make_backup=args.backup, dry_run=args.dry_run
            )
            if changed:
                changed_count += 1
                print(f"[CHANGED] {f}  -> new title: '{new_title}'")
                if args.verbose and old_title:
                    print(f"    old title: {old_title}")
            else:
                if args.verbose:
                    print(f"[SKIP]    {f} (no change needed)")
        except Exception as e:
            print(f"[ERROR] {f}: {e}", file=sys.stderr)

    print(f"Processed {len(files)} files. {changed_count} changed.")
    if args.dry_run:
        print("Dry-run: no files were modified.")


if __name__ == "__main__":
    main()
