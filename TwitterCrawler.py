# Dev: 3mjms
# Crawl Twitter's public timeline
#
# Twitter API
from utils.TwitterAPI import TwitterAPI

# twitter keys and base api
twitter = TwitterAPI()
# statuses iterator
iterator = twitter.stream().statuses.sample()
# print the tweet
for tweet in iterator:
    twitter.saveTweets(tweet)
