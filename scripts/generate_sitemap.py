import os
import re

# Configuration
OUTPUT_FILE = "sitemap.md"
POST_DIRS = ["_bytes", "_tweets", "_posts"]

# Regex to match Jekyll's post filenames: YYYY-MM-DD-title.md
POST_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md")

def get_post_data(folder, filename):
    """Extract title and URL from Jekyll post filename."""
    match = POST_PATTERN.match(filename)
    if match:
        _, _, _, title = match.groups()
    else:
        title = filename.replace(".md", "")
    
    title = title.replace("-", " ").title()
    if folder == "root":
        url = f"/{filename.replace('.md', '').replace(' ', '-').lower()}"
    else:
        url = f"/{folder.strip('_')}/{filename.replace('.md', '').replace(' ', '-').lower()}"
    
    return title, url

def collect_posts():
    """Collect posts from all directories and root."""
    sitemap = {"root": []}

    # Collect posts from specified directories
    for folder in POST_DIRS:
        sitemap[folder] = []
        for filename in os.listdir(folder):
            if filename.endswith(".md"):
                title, url = get_post_data(folder, filename)
                sitemap[folder].append((title, url))

    # Collect root-level markdown files
    for filename in os.listdir():
        if filename.endswith(".md") and not filename.startswith("_"):
            title, url = get_post_data("root", filename)
            sitemap["root"].append((title, url))

    # Sort items alphabetically
    for folder in sitemap:
        sitemap[folder].sort(key=lambda x: x[0].lower())

    return sitemap

def generate_sitemap():
    """Generate sitemap.md with nested lists."""
    sitemap = collect_posts()

    with open(OUTPUT_FILE, "w") as f:
        f.write("""---
layout: base
title: "Sitemap"
---

""")

        f.write("# {{ page.title }}\n\n")

        # Root-level posts
        if sitemap["root"]:
            f.write("- Root\n")
            for title, url in sitemap["root"]:
                f.write(f"  - [{title}]({url})\n")

        # Posts by directory
        for folder, posts in sitemap.items():
            if folder == "root":
                continue
            f.write(f"- {folder.strip('_').capitalize()}\n")
            for title, url in posts:
                f.write(f"  - [{title}]({url})\n")

    print(f"Sitemap generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sitemap()
