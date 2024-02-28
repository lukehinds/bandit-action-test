import os
from github import Github

# Initialize GitHub client
g = Github(os.getenv('GITHUB_TOKEN'))

# Get repository and pull request
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
pr = repo.get_pull(int(os.getenv('GITHUB_REF').split('/')[-1]))

# Read the Bandit report
with open('report.json', 'r') as file:
    report = file.read()

# Post the report as a comment on the pull request
pr.create_issue_comment('### Bandit Scan Results\n```json\n' + report + '\n```')
