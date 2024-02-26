import os

# Created by ChatGPT
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
    with open("sitemap.md", "w") as sitemap_file:
        sitemap_file.write(sitemap_content)

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

# gen2()

def gen3():
    class JekyllMarkdownFileYamlFrontMatter:
        def __init__(self, filename):
            self.filename = filename
            self.date_in_filename = filename[7:17]
            self.title = None
            self.date = None
            self.year = None
            self.month = None
            self.day = None
            
            # Parse into fields on this class
            with open(filename, "r") as f:
                for line in f:
                    if line.startswith("---"):
                        reading_front_matter = True
                        continue
                    if reading_front_matter:
                        if line.startswith("---"):
                            reading_front_matter = False
                            continue
                        elif line.startswith("title:"):
                            self.title = line.split(":")[1].strip()
                            continue
                        elif line.startswith("date:"):
                            # Remove quote marks.
                            self.date = line.split(":")[1].strip().replace('"', '')
                            self.year = self.date[:4]
                            self.month = self.date[5:7]
                            self.day = self.date[8:10]
                            continue
        
        def __str__(self):
            return f"JekyllMarkdownFileYamlFrontMatter(filename={self.filename}, title={self.title}, date={self.date}, year={self.year}, month={self.month}, day={self.day}, url={self.get_url()}, date_in_filename={self.date_in_filename})"

        def get_url(self):
            return f"/posts/{self.year or self.date_in_filename[:4]}/{self.month or self.date_in_filename[5:7]}/{self.filename[18:].replace('_', '-')[:-3]}/"

    _posts = []
    for file in os.listdir("_posts"):
        file_meta = JekyllMarkdownFileYamlFrontMatter(os.path.join("_posts", file))
        _posts.append(file_meta)
        # print(file_meta)
    
    # print([str(post) for post in _posts])

    sitemap_content = "---\nlayout: base\ntitle: Site Map\npermalink: /sitemap/\n---\n\n## Site Map\n\n"
    sitemap_content += "* [Posts](/posts/)\n"
    for post in _posts:
        sitemap_content += f"  * [{post.title or 'None'}]({post.get_url()})\n"
    
    print(sitemap_content)

    with open("sitemap.md", "w") as sitemap_file:
        sitemap_file.write(sitemap_content)

gen3()
