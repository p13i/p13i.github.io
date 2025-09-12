import os
import re
import sys


def clean_content(text: str, max_len: int = 64) -> str:
    """Strip HTML, emojis, non-ASCII chars, markdown symbols, and truncate."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove non-ASCII (emojis, symbols, etc.)
    text = text.encode("ascii", errors="ignore").decode()
    # Remove Markdown-y characters: *, [ ], ( )
    text = re.sub(r"[\*\[\]\(\)]", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Truncate with "..." if needed
    if len(text) > max_len:
        text = text[: max_len - 3].rstrip() + "..."
    return text


def yaml_safe_string(s: str) -> str:
    """
    Escape a string for safe YAML inline usage by wrapping in double quotes
    and escaping special characters.
    """
    s = s.replace("\\", "\\\\")  # escape backslashes
    s = s.replace('"', '\\"')  # escape double quotes
    return f'"{s}"'


def update_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    # Split into parts by front matter markers
    parts = data.split("---", 2)
    if len(parts) < 3:
        return  # no front matter

    before, front_matter, content = parts[0], parts[1], parts[2]

    # Compute new title
    title = clean_content(content)
    safe_title = yaml_safe_string(title)

    # Remove any existing title line(s)
    fm_lines = []
    for line in front_matter.splitlines():
        if not line.strip().startswith("title:"):
            fm_lines.append(line)
    fm_lines.append(f"title: {safe_title}")
    new_front_matter = "\n".join(fm_lines) + "\n"

    # Rebuild file
    new_data = f"---\n{new_front_matter}---{content}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_data)

    print(f"Updated {path} with title: {safe_title}")


def update_folder(folder: str):
    for root, _, files in os.walk(folder):
        for fname in files:
            if fname.endswith((".md", ".markdown", ".html")):
                update_file(os.path.join(root, fname))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <folder>")
        sys.exit(1)
    update_folder(sys.argv[1])
