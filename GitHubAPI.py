# Dev: 3mjms
# 1 - Create a GitHub API
# 2 - Get user repos
# 3 - Get languages from a repo
#

import json
from github import Github, GithubException
from pprint import pprint as pp
import requests


class GithubAPI(object):
    def __init__(self):
        with open('keys.json') as keys_file:
            keys = json.load(keys_file)

        # get access_token from external file
        self.access_token = keys["github"]["access_token"]
        # self.g = Github(self.access_token, per_page=100)
        self.g = Github(self.access_token)
        try:
            self.g.get_user().login
        # test the token
        except GithubException as e:
            print e.status + e.message

        self.user = self.g.get_user()
        self.repo = None
        # self.repo = self.user.get_repo(repo)

    def getOneRepo(self, repo):
        self.repo = self.user.get_repos(repo)
        return self.repo

    # get the repos that belong to self.user
    def getRepos(self):
        repos = [self.repo.name for self.repo in self.g.get_user(self.user.name).get_repos()]
        return repos

    # get the languages from a repo
    def getLangsFromRepo(self, repo=None):
        # if the user passes in a repo
        # return the languages from that repo
        # else return the languages from the self.repo
        self.repo = self.user.get_repo(repo)
        return [self.repo.get_languages()]

    # get the public repos
    def getPubRepos(self, repoUrl):
        # make http request to get the json
        resp = requests.get(repoUrl).json()
        return [(repo['name'],
                 repo['url'])
                for repo in resp]

    # get issues from a repo
    def getIssues(self):
        q = 'label:bug+language:python&sort=created&order=asc'
        # resp = requests.get(Github.search_repositories(query=q))
        resp = self.g.search_issues(query=q)
        pp(resp)
