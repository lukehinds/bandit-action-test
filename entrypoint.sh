#!/bin/bash


# Use the INPUT_ prefixed environment variables that are passed by GitHub Actions
github_token=$INPUT_GITHUB_TOKEN
github_repository=$INPUT_GITHUB_REPOSITORY

# Initialize the Bandit command
cmd="bandit"

# Check for the path input and add it to the command
if [ -n "${INPUT_PATH}" ]; then
    cmd+=" -r ${INPUT_PATH}"
fi

# Check for the level input and set the severity level
if [ -n "${INPUT_LEVEL}" ]; then
    case "${INPUT_LEVEL}" in
        "low") cmd+=" -l" ;;
        "medium") cmd+=" -ll" ;;
        "high") cmd+=" -lll" ;;
    esac
fi

# Check for the confidence input and set the confidence level
if [ -n "${INPUT_CONFIDENCE}" ]; then
    case "${INPUT_CONFIDENCE}" in
        "low") cmd+=" -i" ;;
        "medium") cmd+=" -ii" ;;
        "high") cmd+=" -iii" ;;
    esac
fi

# Additional flags can be added here following the same pattern

# Specify the output format as JSON and output file
cmd+=" -f json -o report.json"

# Run the Bandit command
echo "Executing command: $cmd"
eval $cmd

# Call post_comment.py to post the Bandit report as a comment on the pull request
python post_comment.py

# If specified, exit with 0 even if issues are found
if [ "${INPUT_EXIT_ZERO}" == "true" ]; then
    exit 0
fi

# Check if report.json exists and is not empty
if [ -s report.json ]; then
    # If you want to fail the action on detected issues, uncomment the next line
    # exit 1
    echo "Bandit scan completed with findings."
else
    echo "Bandit scan completed with no findings."
fi
