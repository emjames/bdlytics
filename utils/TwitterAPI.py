# Dev: 3mjms
# base of Spark4Python_Twitter_API.py
# AN - version 20150426
#
# 1 - Access Twitter API with OAuth credentials
# 2 - Search Twitter for query = "ApacheSpark" (JSON - Tweets)
# 3 - Parse Tweets (TweetId, CreatedAt, UserId, UserName, TweetText, TweetURL)
#

import json
import logging
# import IO_json as IO_json
from utils import IO_json, IO_mongo

import sys

import time
import twitter
import urlparse


class TwitterAPI(object):
    def __init__(self):
        # get keys in keys.json file
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

        # get configs in config.json
        with open('configs.json') as configs_file:
            configs = json.load(configs_file)
        # logger init
        appName = configs["appName"]
        self.logger = logging.getLogger(appName)
        # self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        logPath = configs["logFolder"]
        fileName = appName
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addFilter(fileHandler)
        self.logger.setLevel(logging.DEBUG)

        # save to JSON file init
        jsonFpath = configs["jsonPath"]
        jsonFname = appName
        # self.jsonSaver = IO_json(jsonFpath, jsonFname)
        self.jsonSaver = IO_json.IO_json(jsonFpath, jsonFname)

        # save to MongoDB init
        # self.mongoSaver = IO_mongo.IO_mongo(db='twtr001_db', coll='twtr001_coll')
        self.mongoSaver = IO_mongo.IO_mongo(db=configs["db"], coll=configs["coll"])

    def searchTwitter(self, q, max_res=10, **kwargs):
        search_results = self.api.search.tweets(q=q, count=10, **kwargs)
        statuses = search_results['statuses']
        max_results = min(1000, max_res)

        for _ in range(10):
            try:
                next_results = search_results['search_metadata']['next_results']
                # self.logger.info('info in searchTwitter - next_results: %s'% next_results[1:])
            # Python raises a KeyError whenever a dict() object is requested
            # (using the format a = adict[key]) and the key is not in the dictionary.
            except KeyError as e:
                # self.logger.error('error in searchTwitter: %s', %(e))
                break

            # [1:] slice [begin:end]
            next_results = urlparse.parse_qsl(next_results[1:])
            # self.logger.info('info in searchTwitter - next_results[max_id]:', next_results[0:])

            # construct a dictionary
            kwargs = dict(next_results)
            # self.logger.info('info in searchTwitter - next_results[max_id]:', kwars['max_id'])
            search_results = self.api.search.tweets(**kwargs)
            statuses += search_results['statuses']

            if len(statuses) > max_results:
                self.logger.info('info in searchTwitter - got %i tweets - max: %i' % (len(statuses), max_results))
                break
        return statuses

    # returns a stream of the public streams availabe on Twitter
    def stream(self):
        return twitter.TwitterStream(auth=self.auth)

    def saveTweets(self, statuses):
        # saving to JSON file
        print 'Saving to json'
        print statuses
        self.jsonSaver.save(statuses)

        # save to MongoDB
        # for s in statuses:
        #     self.mongoSaver.save(s)

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

    def getTweets(self, q, max_res=10):
        """
        Make a Twitter API call whilst managing rate limit and errors
        :param q:  query
        :param max_res:
        :return:
        """

        def handleError(e, wait_period=2, sleep_when_rate_limited=True):

            if wait_period > 3600:  # seconds
                # self.logger.error('Too many retries in getTweets: %s', %(e))
                raise e
            if e.e.code == 401:
                # self.logger.error('error 401 * Not Authorised * in getTweets: %s', %(e))
                return None
            elif e.e.code == 404:
                # self.logger.error('error 404 * Not Found * in getTweets: %s', %(e))
                return None
            elif e.e.code == 429:
                # self.logger.error('error 429 * API Rate Limit Exceeded* in getTweets: %s', %(e))
                if sleep_when_rate_limited:
                    # self.logger.error('error 429 * Retrying in 15 minutes * in getTweets: %s', %(e))
                    sys.stderr.flush()
                    time.sleep(60 * 15 + 5)
                    # self.logger.error('error 429 * Retrying Now * in getTweets: %s', %(e))
                    return 2
                else:
                    raise e  # caller must handle the rate limiting issue
            elif e.e.code in (500, 502, 503, 504):
                self.logger.info('Encontered %i Error. Retrying in %i seconds' % (e.e.code, wait_period))
                time.sleep(wait_period)
                wait_period *= 1.5
                return wait_period
            else:
                # self.logger.error('Exit - aborting - %s', %(e))
                raise e

        while True:
            try:
                self.searchTwitter(q, max_res=10)
            except twitter.api.TwitterHTTPError as e:
                error_count = 0
                wait_period = handleError(e, wait_period)
                if wait_period is None:
                    return
