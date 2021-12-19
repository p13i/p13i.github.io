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

build-site	:
	docker-compose run www bash -c "bundle exec jekyll build"

build	:
	docker-compose build
	make build-site

# Build without using caches
build-from-scratch	:
	docker-compose build --no-cache
	make build-site

# Bring the app online after building from scratch
online	:
	python3 -m http.server --directory "_site" 1337

# https://stackoverflow.com/a/18346041
watch	:
	while inotifywait -qqre modify,create,delete,move ./;do make;done

# Get CLI access
bashin	:
	docker-compose www exec bash

# Stop serving the website
stop	:
	docker-compose down

# Shortcut
up		:
	docker-compose up

publish	:
	git add .
	git commit -m msg
	git push