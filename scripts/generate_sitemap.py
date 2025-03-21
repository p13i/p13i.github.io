import os
import re
from dataclasses import dataclass

# Configuration
OUTPUT_FILE = "sitemap.md"
PAGE_DIRS = ["_bytes", "_tweets", "_posts", '.']

@dataclass
class Page:
    name: str
    url: str
    subpages: list['Page']

    def GenerateSitemap(self, indent:int=0):
        if self.name == '.':
            return ''
        if self.name.startswith('_'):
            self.name = self.name[1:].capitalize()
        s = ' ' * indent + f'- [`{self.name} {self.url}`]({self.url})\n'
        for page in self.subpages:
            s += page.GenerateSitemap(indent=indent + 2)
        return s

def get_url(folder: str, post_title: str) -> str:
    if folder[0] == '_':
        folder = folder[1:]
    REGEX = r'(\d{4})-(\d{2})-(\d{2})-([\w\-]+)\.md'
    matches = re.search(REGEX, post_title)
    if not matches:
        return f'/{folder}/{post_title.rstrip('.md')}/'
    return f'/{folder}/{matches.group(1)}/{matches.group(2)}/{matches.group(4)}/'

def CollectPages():
    """Collect posts from all directories and root."""
    top_level_pages: list[Page] = []

    # Collect posts from specified directories
    for dir in PAGE_DIRS:
        page_name: str = dir
        page_url: str = f'/{dir.lstrip('_')}/'
        page_subpages: list[str] = []
        for filename in os.listdir(dir):
            if filename.endswith(".md"):
                with open(os.path.join(dir, filename)) as f:
                    contents = f.read()
                    REGEX = r'title: (.*)\n'
                    matches = re.search(REGEX, contents)
                    if not matches:
                        REGEX = '---\n\n(.*)\n'
                        matches = re.search(REGEX, contents)
                        if not matches:
                            title = 'unknown'
                        else:
                            title = matches.group(1)[:32]
                    else:
                        title = matches.group(1)
                    url = get_url(dir, filename)
                new_page = Page(name=title, url=url, subpages=[])
                if dir == '.':
                    top_level_pages.append(new_page)
                else:
                    page_subpages.append(new_page)
        page_for_dir = Page(name=page_name, url=page_url, subpages=page_subpages)
        top_level_pages.append(page_for_dir)
    
    root = Page(name='p13i.io', url='/', subpages=top_level_pages)
    return root.GenerateSitemap()

def generate_sitemap():
    """Generate sitemap.md with nested lists."""
    sitemap = CollectPages()

    with open(OUTPUT_FILE, "w") as f:
        f.write(f"""---
layout: base
title: "Sitemap"
---
# Sitemap

{sitemap}

""")

    print(f"Sitemap generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sitemap()
