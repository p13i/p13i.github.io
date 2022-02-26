########################################
# Makefile for GNU Make projects 
#
# Usage:
#   make
#   make clean
#   make run
#   make stop
#   make publish
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
	docker-compose up --build

# Stop serving the website
down	:
	docker-compose down

# Adds all files, commits an empty
# message to git, and pushes to GitHub
push	:
	git add .
	git commit --allow-empty-message -m ''
	git push
