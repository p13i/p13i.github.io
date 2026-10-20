# Makefile for GNU Make projects 
#
# Usage:
#   make
# 		Runs clean and docker up
#   make clean
#		Deoetes generated files
#   make up
#		docker up
#   make down
#		docker down
#	make push
#		Adds all unstaged changes and commits and pushes
#   make lint
#		Checks formatting with pinned trycopilotai/lint
#   make format
#		Applies formatting with pinned trycopilotai/lint
#   make sync
# 		Pulls changes from git and pushes local commits
#   make newpost
#		Create a new post skeleton in _posts

.ONESHELL:

# Default when make is called w/o args
default:
	make clean
	make up

# Deletes all the generated files
clean:
	make down
    # In order: generated HTML, 2 caches
	rm -rf _site/ .sass-cache/ .jekyll-metadata
	docker-compose rm --force

# Serves the website on localhost:4000
up:
	docker-compose up --force-recreate --always-recreate-deps --build

# Stop serving the website
down:
	docker-compose down

# Adds all files, commits an empty
# message to git, and pushes to GitHub
push:
	git add .
	git commit --allow-empty-message -m "${date}"
	git push

generate-sitemap:
	python3 scripts/generate_sitemap.py

# Creates a new Jekyll post in _posts with today's date and a slugged filename.
# Usage:
#   make newpost                 # prompts for slug
#   SLUG=my-new-post make newpost # non-interactive; must be lowercase/digits/dashes
# The rule aborts if the file already exists or the slug is invalid.
newpost:
	python3 - <<-'PY'
	from datetime import date
	from pathlib import Path
	import os
	import re
	import sys

	slug = (os.getenv("SLUG") or input("New post slug (dash-separated, e.g., my-new-post): ")).strip()
	if not slug: sys.exit("Slug is required.")
	if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug): sys.exit("Slug must be lowercase letters, numbers, and dashes (dash-separated).")

	today = date.today()
	date_str = today.strftime("%Y-%m-%d")
	filename = f"{date_str}-{slug}.md"

	posts_dir = Path.cwd() / "_posts"
	posts_dir.mkdir(parents=True, exist_ok=True)
	target_path = posts_dir / filename
	if target_path.exists(): sys.exit(f"{target_path} already exists; choose a different slug.")

	title = slug.replace("-", " ").title()
	body = (
	    "---\n"
	    f'title: "{title}"\n'
	    f'date: "{date_str}"\n'
	    "categories:\n"
	    "  - writing\n"
	    "layout: post\n"
	    "tags: []\n"
	    "author: Pramod Kotipalli\n"
	    "description:\n"
	    "  TODO: add a short summary for previews.\n"
	    "---\n\n"
	    f"# {title}\n\n"
	    "Start writing here.\n"
	)

	target_path.write_text(body, encoding="utf-8")
	print(f"Created {target_path}")
	PY

setup-scripts:
	pip3 install pillow
	pip3 install requests
	pip3 install pyyaml

write-tweet-titles:
	python3 scripts/update_jekyll_titles.py _tweets

# Clones pinned trycopilotai/lint v0.1.8 into .cache once.
lint-checkout:
	test -f .cache/lint-v0.1.8/lint.py || { rm -rf .cache/lint-v0.1.8 && git -c advice.detachedHead=false clone --quiet --depth 1 --branch v0.1.8 https://github.com/trycopilotai/lint.git .cache/lint-v0.1.8; }

# Checks Markdown, YAML, and Python formatting without writing.
lint: lint-checkout
	python3 .cache/lint-v0.1.8/lint.py --read-only --docker --print-width 60 --language markdown --language yaml --language python

# Applies the formatting that make lint checks.
format: lint-checkout
	python3 .cache/lint-v0.1.8/lint.py --write --docker --print-width 60 --language markdown --language yaml --language python

sync: pull
	git push

pull:
	git pull --rebase --all
