# Dev: 3mjms
# Crawl github to find issues in different repositories
#
# GitHub API
from GitHubAPI import GithubAPI
from IO_json import IO_json
from datetime import date
import datetime as dt
import time
import logging
import json
from pprint import pprint as pp

# setup configs
with open('configs.json') as configs_file:
    configs = json.load(configs_file)

appName = "pygithub"
appFname = appName + date.today().isoformat()
appLogFile = appFname + ".log"
logging.basicConfig(filename=appLogFile, level=logging.DEBUG)
requests = 0

# create a new API object
git = GithubAPI()


# helper to check the api's current limit and avoid exceeding
# Github API allows 30 req / 60s
def checkLimit(name):
    logging.debug("Saved " + name)
    limits = git.getRate()
    # low limits, sleep
    if limits[0] < 30:
        logging.debug("Time: " + limits[1])
        dt1 = dt.datetime.fromtimestamp(limits[1])
        dt2 = dt.datetime.fromtimestamp(time.time())
        sleepTime = (dt1 - dt2).total_seconds()
        logging.debug("Sleeping for " + str(sleepTime) + " seconds")
        time.sleep(sleepTime)


# main runner
def main():
    # get repositories in trend
    language = "python"
    for repo in git.getTrendByLang(language):
        # crate a json file for each repo
        repoSaver = IO_json(configs["jsonPath"], repo.name)
        # store the raw_data from the repo class
        # pp(repo.raw_data)
        repoSaver.save(repo.raw_data)
        # log the save
        logging.debug("Repo begin: " + repo.name)
        checkLimit(repo.name)
        # print "Repo saved: ", repo.name
        # save the languages in the repo
        repoSaver.save(repo.get_languages())
        checkLimit("languages")
        # save the readme of the repo
        repoSaver.save(repo.get_readme().raw_data)
        checkLimit("readme")
        # save the amount of stargazers
        for sg in repo.get_stargazers():
            repoSaver.save(sg.raw_data)
        checkLimit("stargazers")
        # contributor list
        # repoSaver.savePP(repo.get_stats_contributors().raw_data)
        for statContrib in repo.get_stats_contributors():
            repoSaver.save(statContrib.raw_data)
        checkLimit("stats contributors")
        for commitAct in repo.get_stats_commit_activity():
            repoSaver.save(commitAct.raw_data)
        checkLimit("stats contributors")
        # repoSaver.savePP(repo.get_stats_code_frequency().raw_data)
        for codeFreq in repo.get_stats_code_frequency():
            repoSaver.save(codeFreq.raw_data)
        checkLimit("code frequency")
        repoSaver.save(repo.get_stats_participation().raw_data)
        # number of commits per hour in each day
        checkLimit("stats participations")
        repoSaver.save(repo.get_stats_punch_card().raw_data)
        checkLimit("stats punch card")
        # repoSaver.savePP(repo.get_subscribers().raw_data)
        for sub in repo.get_subscribers():
            repoSaver.save(sub.raw_data)
        checkLimit("repo subscribers")
        # repoSaver.savePP(repo.get_teams().raw_data)
        for team in repo.get_teams():
            repoSaver.save(team.raw_data)
            checkLimit("team")
            for member in team.get_members():
                repoSaver.save(member.raw_data)
            checkLimit("members in team")
        for watcher in repo.get_watchers():
            repoSaver.save(watcher.raw_data)
        checkLimit("watchers")
        # loop through the commits in the repo
        for commit in repo.get_commits():
            # and store them
            # repoSaver.save(commit.raw_data)
            repoSaver.save(commit.raw_data)
            # log the commit save
            print "Commit saved"
            # loop through the files in the commits
            for f in commit.files:
                # and store them
                repoSaver.savePP("LOGR_FILE")
                repoSaver.save(f.raw_data)
                # log the save
                print "File saved"
            # iterate through the comments of each commit
            for comment in commit.get_comments():
                # and store them
                repoSaver.save(comment.raw_data)
            # iterate through the statuses of each commit
            for status in commit.get_statuses():
                # and store them
                repoSaver.save(status.raw_data)
            checkLimit("commits")
        # iterate through the contributors of the repository
        for contrib in repo.get_contributors():
            # store the contributor
            repoSaver.save(contrib.raw_data)
            # get contributor followers
            for follower in contrib.get_followers():
                # store the follower
                repoSaver.save(follower.raw_data)
        checkLimit("contributors")
        # iterate through the forks of the repository
        for fork in repo.get_forks():
            # store each fork
            repoSaver.save(fork.raw_data)
        checkLimit("forks")
        # iterate through the references
        for ref in repo.get_git_refs():
            # store each reference
            repoSaver.save(ref.raw_data)
        checkLimit("git references")
        # iterate through the issues in the repo
        for issue in repo.get_issues():
            repoSaver.save(issue.raw_data)
        checkLimit("repo issues")
        # get all the comments in the issue
        for commentsIssue in repo.get_issues_comments():
            repoSaver.save(commentsIssue.raw_data)
        checkLimit("repo issues comments")
        for issueEvent in repo.get_issues_events():
            repoSaver.save(issueEvent.raw_data)
        checkLimit("repo events")
        for label in repo.get_labels():
            repoSaver.save(label.raw_data)
        checkLimit("repo labels")
        for ms in repo.get_milestones():
            repoSaver.save(ms.raw_data)
            for lbl in ms.get_labels():
                repoSaver.save(lbl.raw_data)
        checkLimit("repo milestones")
        # iterate through the pull requests in the repo
        for pr in repo.get_pulls():
            repoSaver.save(pr.raw_data)
            for commit in pr.get_commits():
                repoSaver.save(commit.raw_data)
                for comment in commit.get_comments():
                    repoSaver.save(comment.raw_data)
                for status in commit.get_statuses():
                    repoSaver.save(status.raw_data)
            checkLimit("commit pulls")
            # get the files for the pull request
            for fi in pr.get_files():
                repoSaver.save(fi.raw_data)
            checkLimit("pull files")
        # iterate through the pull requests comments
        for comment in repo.get_pulls_comments():
            repoSaver.save(comment.raw_data)
        checkLimit("repo comments")
        # iterate through the pull review comments
        for comment in repo.get_pulls_review_comments():
            repoSaver.save(comment.raw_data)
        checkLimit("repo pulls review comments")
        checkLimit("Repo end: " + repo.name)


if __name__ == '__main__':
    main()
