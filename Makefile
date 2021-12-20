# Makefile for GNU Make

# Deletes all the generated files
clean	:
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

publish	:
	git add .
	git commit -m msg
	git push