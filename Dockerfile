FROM ruby:2.4

RUN gem install bundler -v 2.3.26

WORKDIR /www

# Copy the Gemfile and Gemfile.lock
COPY Gemfile .
COPY Gemfile.lock .

# Use bundle to install dependencies from the above files
RUN bundle install
