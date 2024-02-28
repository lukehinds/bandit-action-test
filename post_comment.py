from github import Github
import os

# Make sure to get the GITHUB_TOKEN from the environment variables
github_token = os.getenv('GITHUB_TOKEN')

if not github_token:
    raise Exception('The GITHUB_TOKEN environment variable is not set.')

# Get repository
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# Extract pull request number from GITHUB_REF
ref_parts = os.getenv('GITHUB_REF').split('/')
if 'pull' in ref_parts:
    pr_number = int(ref_parts[ref_parts.index('pull') + 1])
else:
    raise ValueError(f"Invalid GITHUB_REF for a pull request: {os.getenv('GITHUB_REF')}")

# Get pull request
pr = repo.get_pull(pr_number)

# Read the Bandit report
with open('report.json', 'r') as file:
    report = file.read()

# Post the report as a comment on the pull request
pr.create_issue_comment('### Bandit Scan Results\n```json\n' + report + '\n```')
