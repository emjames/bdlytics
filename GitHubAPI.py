# Dev: 3mjms
# 1 - Create a GitHub API
# 2 - Get user repos
# 3 - Get languages from a repo
#

import json
from github import Github
from pprint import pprint as pp
import requests


class GithubAPI(object):
    def __init__(self, user='emjames'):
        with open('keys.json') as keys_file:
            keys = json.load(keys_file)

        # get access_token from external file
        self.access_token = keys["github"]["access_token"]
        self.g = Github(self.access_token, per_page=100)
        self.user = self.g.get_user(user)
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
