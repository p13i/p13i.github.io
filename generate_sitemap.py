import os

def generate_sitemap():
    sitemap_content = "---\nlayout: base\ntitle: Site Map\npermalink: /sitemap/\n---\n\n"
    excluded_dirs = ['_site', '.git', 'assets', 'node_modules']
    post_prefix = "/"

    for root, dirs, files in os.walk(".", topdown=True):
        # Exclude specific directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith((".md", ".html")) and not file.startswith("sitemap"):
                # Construct the path relative to the site URL
                path = os.path.join(root, file).replace("./", "").replace("index.html", "").replace("index.md", "")
                title = file.replace(".md", "").replace(".html", "").replace("_", " ").title()
                link = post_prefix + path.replace(" ", "%20")
                sitemap_content += f"- [{title}]({link})\n"

    # Write the sitemap content to sitemap.md

# generate_sitemap("")

def gen2():
    root_files = [filename[:-3] for filename in os.listdir(".") if filename.endswith(".md")]
    collections_dirs = ["_bytes", "_posts", "_tweets"]
    collection_filename_sorters = {
        "_bytes": lambda a: a[:-3],
        "_posts": lambda a: a[:-3],
        "_tweets": lambda f: int(f[:-3])
    }

    sitemap_content = "---\nlayout: base\ntitle: Site Map\npermalink: /sitemap/\n---\n\n## Site Map\n\n"
    for filename in root_files:
        sitemap_content += f"* [{(filename.title())}]({'/' + filename + '/'})\n" 

        for dir_ in collections_dirs:
            # Remove leading underscore `_`
            if filename != dir_[1:]:
                continue
            # Otherwise, add subposts
            dir_files = list(os.listdir(dir_))
            sorter = collection_filename_sorters[dir_]
            dir_files = sorted(dir_files, key=sorter)
            for dir_file in dir_files:
                sitemap_content += f"  * [{dir_file[:-3].replace('_', ' ').title()}]({'/' + filename + '/' + (dir_file[:-3].replace('_', '-')) + '/'})\n"

    print(sitemap_content)
    with open("sitemap.md", "w") as sitemap_file:
        sitemap_file.write(sitemap_content)

gen2()
