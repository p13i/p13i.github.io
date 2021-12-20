FROM ruby:2.4

RUN gem install bundler

WORKDIR /www

# Copy the Gemfile and Gemfile.lock
COPY Gemfile.lock .

# Use bundle to install dependencies from the above files
RUN bundle install
