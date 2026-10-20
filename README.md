# p13i.github.io

Personal website

[http://p13i.io/](http://p13i.io/)

## Build and run this site locally

1. Install
   [Docker](https://docs.docker.com/engine/installation/)
   and
   [Docker Compose](https://docs.docker.com/compose/install/).
2. Run
   `git clone https://github.com/p13i/p13i.github.io.git`
3. Run `make up`
4. Open `localhost:4000`

## Check formatting

`make lint` checks Markdown, YAML, and Python formatting
with pinned
[trycopilotai/lint](https://github.com/trycopilotai/lint)
v0.1.8 and does not write. `make format` applies that
formatting. Both need Docker and Python 3.11 or newer.
