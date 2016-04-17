# Dev: 3mjms
# Crawl github to find issues in different repositories
#
# GitHub API
import datetime as dt
import json
import logging
import time
from datetime import date

from utils.GitHubAPI import GithubAPI
from utils.IO_json import IO_json

# setup configs
with open('configs.json') as configs_file:
    configs = json.load(configs_file)

appName = "pygithub"
appFname = appName + date.today().isoformat()
localT = time.localtime()
# create a log file stating the date and hour created
appLogFile = appFname + str(localT[3]) + "h" + str(localT[4]) + "m" + ".log"
logging.basicConfig(filename=appLogFile, level=logging.DEBUG)

# create a new API object
git = GithubAPI()


# helper to check the api's current limit and avoid exceeding
# Github search API allows 30 req / 60s
def checkLimit(name):
    logging.debug("DEBUG:jms:Saved " + name)
    rl = git.getRate()
    limits = rl.raw_data
    rateRemaining = limits['rate']['remaining']  # amount of requests left
    rateReset = limits['rate']['reset']  # amount of time to wait for reset
    searchRemaining = limits['resources']['search']['remaining']  # amount of searches left
    searchReset = limits['resources']['search']['reset']  # amount of time to wait for reset
    # low limits, sleep
    if rateRemaining < 30:
        # if its the rate, wait the rate reset
        logging.debug("Time: " + rateReset)
        dt1 = dt.datetime.fromtimestamp(rateReset)
        dt2 = dt.datetime.fromtimestamp(time.time())
        sleepTime = (dt1 - dt2).total_seconds()
        logging.debug("Sleeping for " + str(sleepTime) + " seconds")
        time.sleep(sleepTime)
    # else wait for the search reset
    elif searchRemaining < 5:
        logging.debug("Time: " + searchReset)
        dt1 = dt.datetime.fromtimestamp(searchReset)
        dt2 = dt.datetime.fromtimestamp(time.time())
        sleepTime = (dt1 - dt2).total_seconds()
        logging.debug("Sleeping for " + str(sleepTime) + " seconds")
        time.sleep(sleepTime)


# main runner
def main():
    # query for language and repositories in trend
    language = "python"
    # a list of previously crawled repos
    repoList = ["httpie", "thefuck", "awesome-python", "flask", "requests", "django", "youtube-dl", "ansible",
                "letsencrypt", "scrapy", "shadowsocks", "awesome-machine-learning",
                "big-list-of-naughty-strings", "tornado"]
    for repo in git.getTrendByLang(language):
        # check if the repo has already been crawled
        if repo.name in repoList:
            continue
        else:
            # crate a json file for each repo
            repoSaver = IO_json(configs["jsonPath"], repo.name)
            # store the raw_data from the repo class
            # pp(repo.raw_data)
            repoSaver.save(repo.raw_data)
            # log the save
            logging.debug("Repo begin: " + repo.name)
            print "REPO: " + repo.name
            checkLimit(repo.name)
            print "Getting languages "
            repoSaver.save(repo.get_languages())
            checkLimit("languages")
            print "Getting issues "
            for issue in repo.get_issues():
                repoSaver.save(issue.raw_data)
            checkLimit("repo issues")
            # get all the comments in the issue
            print "Getting issues comments"
            for commentsIssue in repo.get_issues_comments():
                repoSaver.save(commentsIssue.raw_data)
            checkLimit("repo issues comments")
            checkLimit("Repo end: " + repo.name)
            # add the repo to the parsed list
            # TODO: add a persistence to repoList
            repoList.append(repo.name)
            print "REPO " + repo.name + " END"


if __name__ == '__main__':
    main()
