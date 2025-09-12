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

setup-lint:
	pip3 install pillow
	pip3 install requests
	pip3 install black
	npm install --global prettier

lint-markups:
	npx prettier --write --print-width 60 --trailing-comma=none --prose-wrap always '**/*.{md,html,yml,yaml}'

lint-python: 
	python3 -m black .

web-tiles:
	python3 scripts/make_web_tiles.py

write-tweet-titles:
	python3 scripts/update_jekyll_titles.py _tweets

lint: generate-sitemap web-tiles write-tweet-titles lint-markups lint-python

sync: pull
	git push

pull:
	git pull --rebase
