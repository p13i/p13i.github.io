########################################
# Makefile for GNU Make projects 
#
# Usage:
#   make
#   make clean
#   make run
#   make stop
#   make publish
#   make fix
########################################

# Default when make is called w/o args
default	:
	make clean
	make up

# Deletes all the generated files
clean	:
	make down
    # In order: generated HTML, 2 caches
	rm -rf _site/ .sass-cache/ .jekyll-metadata
	docker-compose rm --force

# Serves the website on localhost:4000
up		:
	docker-compose up --force-recreate --always-recreate-deps --build

# Stop serving the website
down	:
	docker-compose down

# Adds all files, commits an empty
# message to git, and pushes to GitHub
push	:
	git add .
	git commit --allow-empty-message -m ''
	git push

fix:
	npx prettier '**/*.{json,tsx,md,html,scss,yml,yaml}' --write
