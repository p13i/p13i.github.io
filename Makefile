# Makefile for GNU Make

# Stop containers, clean, build without cache, and serve
default	:
	make stop
	make clean
	make build

# Clean state repo
clean	:
	rm -rf _site/
	rm -rf .sass-cache/
	rm -rf .jekyll-metadata
	docker-compose rm --force

# Build without using caches
build	:
	docker-compose build --no-cache
	docker-compose run www bash -c "bundle exec jekyll build"

# Bring the app online
online	:	
	# docker-compose up
	python3 -m http.server --directory "_site" 1337

# Get CLI access
bashin	:
	docker-compose www exec bash

# Stop serving the website
stop	:
	docker-compose down

