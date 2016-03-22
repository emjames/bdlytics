# Dev: 3mjms
# base of Spark4Python_Twitter_API.py
# AN - version 20150426
#
# 1 - Access Twitter API with OAuth credentials
# 2 - Search Twitter for query = "ApacheSpark" (JSON - Tweets)
# 3 - Parse Tweets (TweetId, CreatedAt, UserId, UserName, TweetText, TweetURL)
#

import json
import twitter
import urlparse


class TwitterAPI(object):
    def __init__(self):
        with open('keys.json') as keys_file:
            keys = json.load(keys_file)

        self.consumer_key = keys["twitter"]["consumer_key"]
        self.consumer_secret = keys["twitter"]["consumer_secret"]
        self.access_token = keys["twitter"]["access_token"]
        self.access_secret = keys["twitter"]["access_secret"]

        # authenticate credentials with twitter using OAuth
        self.auth = twitter.OAuth(self.access_token, self.access_secret, self.consumer_key, self.consumer_secret)
        # create registered twitter API with auth
        self.api = twitter.Twitter(auth=self.auth)

    def searchTwitter(self, q, max_res=10, **kwargs):
        search_results = self.api.search.tweets(q=q, count=10, **kwargs)
        statuses = search_results['statuses']
        max_results = min(1000, max_res)

        for _ in range(10):
            try:
                next_results = search_results['search_metadata']['next_results']
            # Python raises a KeyError whenever a dict() object is requested
            # (using the format a = adict[key]) and the key is not in the dictionary.
            except KeyError as e:
                break

            # [1:] slice [begin:end]
            next_results = urlparse.parse_qsl(next_results[1:])
            # construct a dictionary
            kwargs = dict(next_results)
            search_results = self.api.search.tweets(**kwargs)
            statuses += search_results['statuses']

            if len(statuses) > max_results:
                break
        return statuses

    # ??
    def parseTweets(self, statuses):
        return [(status['id'],
                 status['created_at'],
                 status['user']['id'],
                 status['user']['name'],
                 status['text'],
                 url['expanded_url'])
                for status in statuses
                for url in status['entities']['urls']]
