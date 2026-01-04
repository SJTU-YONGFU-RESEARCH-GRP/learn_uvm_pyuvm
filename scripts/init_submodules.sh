#!/bin/bash

# Git Submodule Init Script
# This script initializes and updates all git submodules in the repository
# Usage: ./init_submodules.sh [--recursive] [--force]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
RECURSIVE=false
FORCE=false

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --recursive, -r    Initialize submodules recursively (including nested submodules)"
    echo "  --force, -f        Force update even if submodules are already initialized"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Initialize all submodules"
    echo "  $0 --recursive     # Initialize submodules recursively"
    echo "  $0 --force         # Force update all submodules"
    echo "  $0 -r -f           # Force recursive initialization"
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

# Function to check if .gitmodules file exists
check_gitmodules() {
    if [[ ! -f ".gitmodules" ]]; then
        print_status $YELLOW "Warning: No .gitmodules file found. This repository may not have any submodules."
        print_status $BLUE "Checking for submodules anyway..."
    fi
}

# Function to get list of submodules
get_submodules() {
    local submodules=()

    # Get submodules from .gitmodules file
    if [[ -f ".gitmodules" ]]; then
        while IFS= read -r line; do
            if [[ $line =~ ^[[:space:]]*path[[:space:]]*=[[:space:]]*(.+)$ ]]; then
                submodules+=("${BASH_REMATCH[1]}")
            fi
        done < ".gitmodules"
    fi

    # Also check for submodules in git config
    local config_submodules
    config_submodules=$(git config --file .gitmodules --get-regexp path | cut -d' ' -f2 2>/dev/null || true)

    for submodule in $config_submodules; do
        if [[ ! " ${submodules[*]} " =~ " ${submodule} " ]]; then
            submodules+=("$submodule")
        fi
    done

    echo "${submodules[@]}"
}

# Function to initialize submodules
init_submodules() {
    local recursive_flag=""
    local force_flag=""

    if [[ "$RECURSIVE" == true ]]; then
        recursive_flag="--recursive"
        print_status $BLUE "Initializing submodules recursively..."
    else
        print_status $BLUE "Initializing submodules..."
    fi

    if [[ "$FORCE" == true ]]; then
        force_flag="--force"
        print_status $YELLOW "Force flag enabled - will update even if already initialized"
    fi

    # Initialize submodules
    local cmd="git submodule update --init $recursive_flag $force_flag"
    print_status $BLUE "Executing: $cmd"

    if eval "$cmd"; then
        print_status $GREEN "Successfully initialized submodules"
    else
        print_status $RED "Failed to initialize submodules"
        exit 1
    fi
}

# Function to show submodule status
show_submodule_status() {
    print_status $BLUE "Submodule status:"
    git submodule status
}

# Function to show submodule summary
show_submodule_summary() {
    print_status $BLUE "Submodule summary:"
    git submodule summary
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --recursive|-r)
                RECURSIVE=true
                shift
                ;;
            --force|-f)
                FORCE=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_status $RED "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Main function
main() {
    print_status $BLUE "Starting git submodule initialization..."

    # Parse arguments
    parse_args "$@"

    # Validate environment
    check_git
    check_git_repo
    check_gitmodules

    # Get list of submodules
    local submodules
    submodules=($(get_submodules))

    if [[ ${#submodules[@]} -eq 0 ]]; then
        print_status $YELLOW "No submodules found in this repository"
        exit 0
    fi

    print_status $BLUE "Found ${#submodules[@]} submodule(s):"
    for submodule in "${submodules[@]}"; do
        echo "  - $submodule"
    done
    echo

    # Initialize submodules
    init_submodules

    # Show status and summary
    echo
    show_submodule_status
    echo
    show_submodule_summary

    print_status $GREEN "Submodule initialization completed successfully!"

    # Show next steps
    echo ""
    print_status $YELLOW "Next steps:"
    echo "  1. Navigate to submodule directories to work on them"
    echo "  2. Use 'git submodule update --remote' to update submodules to latest commits"
    echo "  3. Use 'git submodule foreach git pull origin main' to pull latest changes"
}

# Run main function with all arguments
main "$@"
