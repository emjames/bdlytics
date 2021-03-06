# Dev: 3mjms
# Crawl github to find issues in different repositories
#
# GitHub API
import datetime as dt
import json
import logging
import time
from datetime import date
import io

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
    logging.debug("jms:Saved " + name)
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


# method of checking if there is a saved list of previously crawled repositories
# returns the saved list of crawled repos
def getList(fName):
    try:
        with open(fName) as crawledRepos_file:
            crawledRepos = json.load(crawledRepos_file)
            logging.debug("jms:File crawled repo exists")
            crawledRepos_file.close()
            return crawledRepos
    except IOError:
        # if there isn't a list file, create one with an empty list
        logging.debug("jms:File crawled repo doesn't exists")
        saveList(fName, [])


# method of saving previously crawled repositories
# creates a new file (existing file with same name will be erased)
# at fPathName with data
def saveList(fPathName, data):
    mode = 'w'
    with io.open(fPathName, mode, encoding='utf-8') as outFile:
        outFile.write(unicode(json.dumps(data, ensure_ascii=False)))  # python 2.7
        # outFile.write(json.dumps(data, ensure_ascii=False))  # python 3
        outFile.close()


# main runner
def main():
    # query for language and repositories in trend
    language = "python"
    # a list of previously crawled repos
    # repoList = ["httpie", "thefuck", "awesome-python", "flask", "requests", "django", "youtube-dl", "ansible",
    #             "letsencrypt", "scrapy", "shadowsocks", "awesome-machine-learning",
    #             "big-list-of-naughty-strings", "tornado"]
    repoList = getList("list")
    for repo in git.getTrendByLang(language):
        # check if the repo has already been crawled
        if repo.name in repoList:
            # if it has, skip to the next one
            continue
        else:
            # reset the data
            # repoData = {}
            # create a json file for each repo
            repoSaver = IO_json(configs["jsonPath"], repo.name)
            # store the raw_data from the repo class
            # pp(repo.raw_data)
            repoSaver.save(repo.raw_data)
            # repoData['repo'] = json.dumps(repo.raw_data)
            print "DATA"
            # print repoData
            # log the save
            logging.debug("Repo begin: " + repo.name)
            print "REPO: " + repo.name
            # checkLimit(repo.name)
            print "Getting languages "
            repoSaver.save(repo.get_languages())
            # repoData['languages'] = json.dumps(repo.get_languages())
            # repoData = json.dumps(repo.get_languages())
            print "LANGS"
            # print repoData

            # checkLimit("languages")
            print "Getting issues "
            # create empty list to populate all of the issues
            # then add them to repoData
            # tempList = []
            for issue in repo.get_issues():
                repoSaver.save(issue.raw_data)
                print "ISSUE:", json.dumps(issue.raw_data)
                # tempList.append(json.dumps(issue.raw_data))
            # repoData['issues'] = tempList
            checkLimit("repo issues")

            # clear the tempList for storing data in list
            # tempList = []
            # get all the comments in the issue
            print "Getting issues comments"
            for commentsIssue in repo.get_issues_comments():
                repoSaver.save(commentsIssue.raw_data)
                # repoData = json.dumps(commentsIssue.raw_data)
                print "COMMENT:", json.dumps(commentsIssue.raw_data)
                # tempList.append(json.dumps(commentsIssue.raw_data))
            # repoData['issues_comments'] = tempList
            checkLimit("repo issues comments")

            # add the repo to the parsed list
            repoList.append(repo.name)
            # repoSaver.save(repoData)
            # save the crawled repos
            saveList("list", repoList)
            debugmsg = "jms:repo", repo.name, "end"
            logging.debug(debugmsg)
            print "REPO " + repo.name + " END"

    configs_file.close()


if __name__ == '__main__':
    main()
