FROM ruby:2.4

MAINTAINER Pramod Kotipalli "pramod.kotipalli@gmail.com"

RUN gem install bundler

WORKDIR /www

# Copy the Gemfile and Gemfile.lock
COPY Gemfile .
COPY Gemfile.lock .

# Use bundle to install dependencies from the above files
RUN bundle install
