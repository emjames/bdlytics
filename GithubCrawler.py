# Dev: 3mjms
# Crawl github to find issues in different repositories
#
# GitHub API
from GitHubAPI import GithubAPI
from IO_json import IO_json

# create a new API object
if __name__ == '__main__':
    git = GithubAPI()
    # jsonSaver = IO_json('/Users/james/Desktop', 'gitest')
    # get repositories in trend
    language = "python"
    for repo in git.getTrendByLang(language):
        # name of the repo
        print "Repo: ", repo.name, repo.html_url
        # issues in the repo
        print "Issues: ", repo.issues_url
        print "Commits: ", repo.commits_url
        for c in repo.get_commits():
            print c.commit
            for f in c.files:
                print f.patch
                #     for i in git.getIssues(repo):
                #         print i.body
                #         print i.comments

                # for issue in git.getIssues(repo):
                #     print issue.assignee.id
                #     print issue.assignee.name
                #     print 'Repo: ', repo.name
                #     for issue in repo.get_issues():
                #         print issue.milestone
                #         print issue.state


                # loop through class prop
                # for i in repo.get_issues():
                #     for key, value in i.__dict__.items():
                #         if not key.startswith('__'):
                #             print key, value
                # print i.title
                # print i.url
                # print i.user.name
                # print i.repository.full_name
                # print i.state
