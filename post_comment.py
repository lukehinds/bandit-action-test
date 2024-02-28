import os
from github import Github
import json

# Define emoji for each severity level
severity_emoji = {
    "HIGH": "🔴",
    "MEDIUM": "🟠",
    "LOW": "🟡",
    "UNDEFINED": "⚪"
}

# Access the GITHUB_TOKEN environment variable
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise Exception('GITHUB_TOKEN is not set or empty')

# Initialize the GitHub client with the token
g = Github(github_token)

# Get the repository and pull request objects
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
pr_number = int(os.getenv('GITHUB_REF').split('/')[-2])
pr = repo.get_pull(pr_number)

# Read the Bandit report
with open('report.json', 'r') as file:
    report_data = json.load(file)

# Start formatting the comment
comment = "## Bandit Scan Results\n\n"

# Add table header
comment += "| Severity | Issue | File | Line | Confidence |\n"
comment += "| -------- | ----- | ---- | ---- | ---------- |\n"

# Iterate through the results and add table rows
for result in report_data.get('results', []):
    severity = result['issue_severity']
    issue_text = result['issue_text']
    filename = result['filename']
    line_number = result['line_range'][0]
    confidence = result['issue_confidence']
    # Add row to the comment
    comment += f"| {severity_emoji.get(severity, '⚪')} {severity} | {issue_text} | {filename} | {line_number} | {confidence} |\n"

# Post the comment
pr.create_issue_comment(comment)
