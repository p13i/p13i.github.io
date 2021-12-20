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
	make run

# Deletes all the generated files
clean:
	make stop
    # In order: generated HTML, 2 caches
	rm -rf _site/ .sass-cache/ .jekyll-metadata
	docker-compose rm --force

# Serves the website on localhost:4000
run:
	docker-compose up

# Stop serving the website
stop:
	docker-compose down

# Adds all files, commits an empty
# message to git, and pushes to GitHub
publish:
	git add .
	git commit --allow-empty-message -m ''
	git push
