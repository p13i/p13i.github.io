# p13i.github.io

Personal website

[http://p13i.io/](http://p13i.io/)

## Build and run this site locally

1. Install [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Run `git clone https://github.com/p13i/p13i.github.io.git`
3. Run `docker-compose up`
4. Open `localhost:4000`

## One-off builds

### For Stanford website

```shell
docker-compose run www bash -c "JEKYLL_ENV=stanford bundle exec jekyll build"
```
