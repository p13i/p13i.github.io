# Makefile for GNU Make

# Call: make
default	:
	make clean
	make run

# Deletes all the generated files
clean	:
	make stop
	rm -rf _site/
	rm -rf .sass-cache/
	rm -rf .jekyll-metadata
	docker-compose rm --force

# Serves the website on localhost:4000
run		:
	docker-compose up

# Stop serving the website
stop	:
	docker-compose down

# Adds all files, commits an empty
# message to git, and pushes to GitHub
publish	:
	git add .
	git commit --allow-empty-message -m ''
	git push