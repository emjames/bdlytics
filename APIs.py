# Single file to import separate APIs
# GitHub API
from GitHubAPI import GithubAPI
# Twitter API
from TwitterAPI import TwitterAPI
from pprint import pprint as pp


def runTwitter():
    # run twitter API
    q = raw_input('query--> ')
    t = TwitterAPI()

    if not q:
        q = 'Python'

    print 'querying for', q
    tsearch = t.searchTwitter(q)
    tparsed = t.parseTweets(tsearch)
    pp(tparsed)


def runGithub():
    # run GitHub API
    print 'GitHub API'
    user = raw_input('Which user?> ')
    # show a list of public repos to choose from
    # create a new api object
    git = GithubAPI(user=user)
    print 'repos owned by', user
    print 'public repos: '
    # get the public repos and pp them
    pp(git.getPubRepos(git.user.repos_url))
    # print 'one repo', git.getPubRepos(git.user.repos_url)[0][0]
    repo = raw_input('Which repo?> ')
    print 'Languages on', repo, 'repo'
    langs = git.getLangsFromRepo(repo)
    pp(langs)
    # print 'Repo length:', (len(git.getRepos()))
    # print 'Languages:'
    # langs = git.getLangs()
    # pp(langs)


# get input from stdin to decide which API we want to use
op = raw_input('Twitter [0]\nGitHub [1]\n?>> ').lower()

# if it's for Twitter then expect: twitter or 0 [string]
if op == 'twitter' or op == '0':
    runTwitter()
# if it's for GitHub then expect: git or 1 [string]
elif op == 'git' or op == '1':
    runGithub()
