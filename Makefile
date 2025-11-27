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
#		Appplies code formatting
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

setup-lint:
	pip3 install pillow
	pip3 install requests
	pip3 install black
	pip3 install pyyaml
	npm install --global prettier

lint-markups:
	npx prettier --write --print-width 60 --trailing-comma=none --prose-wrap always '**/*.{md,html,yml,yaml}'

lint-python: 
	python3 -m black .

write-tweet-titles:
	python3 scripts/update_jekyll_titles.py _tweets

lint: write-tweet-titles generate-sitemap lint-markups lint-python

sync: pull
	git push

pull:
	git pull --rebase --all
