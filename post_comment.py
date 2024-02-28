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
comment = "## 🛡️ Bandit Scan Results Summary\n\n"

# Prepare a summary of findings
severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNDEFINED": 0}
for result in report_data.get('results', []):
    severity_counts[result['issue_severity']] += 1

comment += f"We found **{severity_counts['HIGH']} High**, **{severity_counts['MEDIUM']} Medium**, and **{severity_counts['LOW']} Low** severity issues. Great job keeping the codebase secure! Remember, security is a journey, not a destination.\n\n"

# Add detailed findings header
comment += "### Detailed Findings\n---\n"

# Add table header
comment += "| Severity | Issue | File | Line | Confidence | More Info | Test ID |\n"
comment += "| -------- | ----- | ---- | ---- | ---------- | --------- | ------- |\n"

# Iterate through the results and add table rows
for result in report_data.get('results', []):
    severity = result['issue_severity']
    issue_text = result['issue_text']
    filename = result['filename']
    line_number = result['line_range'][0]
    confidence = result['issue_confidence']
    more_info_url = result['more_info']
    test_id = result['test_id']
    # Add row to the comment with the new columns
    comment += f"| {severity_emoji.get(severity, '⚪')} {severity} | {issue_text} | {filename} | {line_number} | {confidence} | [More Info]({more_info_url}) | {test_id} |\n"

# Add collapsible section for recommendations
comment += "\n<details>\n<summary>🔍 View detailed recommendations for fixing issues</summary>\n\n"
comment += "- For high-severity issues, prioritize fixes to mitigate potential security risks.\n"
comment += "- Review the [Bandit documentation](https://bandit.readthedocs.io/) for detailed explanations and remediation strategies.\n"
comment += "</details>\n\n"

# Add tips and sign-off
comment += "---\n\n### Tips 💡\n"
comment += "- Regular code reviews and security scans can significantly reduce security risks.\n\n"
comment += "Happy coding! 😊 Feel free to reach out if you need any help with these issues."

# Post the comment
pr.create_issue_comment(comment)
