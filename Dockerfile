FROM ruby:2.4

RUN set -eux; \
    sed -i \
    's|http://deb.debian.org/debian|http://archive.debian.org/debian|g; s|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' \
    /etc/apt/sources.list; \
    printf 'Acquire::Check-Valid-Until "false";\n' > /etc/apt/apt.conf.d/99archive

RUN gem install bundler -v 2.3.26

WORKDIR /www

# Copy the Gemfile and Gemfile.lock
COPY Gemfile .
COPY Gemfile.lock .

# Use bundle to install dependencies from the above files
RUN bundle install
