#!/bin/bash

# Git Submodule Add Script
# This script adds a new git submodule to the repository
# Usage: ./add_submodule.sh <repository_url> [path] [branch]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <repository_url> [path] [branch]"
    echo ""
    echo "Arguments:"
    echo "  repository_url    The URL of the git repository to add as submodule"
    echo "  path             (Optional) The path where the submodule should be placed"
    echo "  branch           (Optional) The branch to track (default: main/master)"
    echo ""
    echo "Examples:"
    echo "  $0 https://github.com/user/repo.git"
    echo "  $0 https://github.com/user/repo.git external/repo"
    echo "  $0 https://github.com/user/repo.git external/repo develop"
}

# Function to validate git repository URL
validate_repo_url() {
    local url=$1

    # Check if URL is not empty
    if [[ -z "$url" ]]; then
        print_status $RED "Error: Repository URL cannot be empty"
        return 1
    fi

    # Check if URL looks like a git repository
    if [[ ! "$url" =~ ^(https?://|git@|ssh://).*\.git$ ]]; then
        print_status $YELLOW "Warning: URL doesn't end with .git, but proceeding anyway"
    fi

    return 0
}

# Function to check if git is available
check_git() {
    if ! command -v git &> /dev/null; then
        print_status $RED "Error: git is not installed or not in PATH"
        exit 1
    fi
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_status $RED "Error: Not in a git repository"
        exit 1
    fi
}

# Function to check if submodule already exists
check_submodule_exists() {
    local path=$1

    if [[ -d "$path" ]] && [[ -f "$path/.git" ]]; then
        print_status $YELLOW "Warning: Directory $path already exists and appears to be a git submodule"
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status $BLUE "Operation cancelled"
            exit 0
        fi
    fi
}

# Main function
main() {
    # Check arguments
    if [[ $# -lt 1 ]]; then
        print_status $RED "Error: Repository URL is required"
        show_usage
        exit 1
    fi

    local repo_url=$1
    local submodule_path=${2:-}
    local branch=${3:-}

    print_status $BLUE "Starting git submodule addition..."

    # Validate inputs
    check_git
    check_git_repo
    validate_repo_url "$repo_url"

    # If no path specified, extract from URL
    if [[ -z "$submodule_path" ]]; then
        submodule_path=$(basename "$repo_url" .git)
        print_status $YELLOW "No path specified, using: $submodule_path"
    fi

    # Check if submodule already exists
    check_submodule_exists "$submodule_path"

    # Build git submodule add command
    local cmd="git submodule add"

    if [[ -n "$branch" ]]; then
        cmd="$cmd -b $branch"
        print_status $BLUE "Adding submodule with branch: $branch"
    fi

    cmd="$cmd $repo_url $submodule_path"

    print_status $BLUE "Executing: $cmd"

    # Execute the command
    if eval "$cmd"; then
        print_status $GREEN "Successfully added submodule: $submodule_path"
        print_status $BLUE "Repository URL: $repo_url"
        if [[ -n "$branch" ]]; then
            print_status $BLUE "Branch: $branch"
        fi

        # Show next steps
        echo ""
        print_status $YELLOW "Next steps:"
        echo "  1. Review the changes: git status"
        echo "  2. Commit the submodule addition: git commit -m 'Add submodule: $submodule_path'"
        echo "  3. Push the changes: git push"
        echo "  4. Initialize submodules on other machines: git submodule update --init --recursive"
    else
        print_status $RED "Failed to add submodule"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
