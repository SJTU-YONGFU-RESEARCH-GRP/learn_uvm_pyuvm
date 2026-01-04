#!/bin/bash

# Git Submodule Remove Script
# This script safely removes a git submodule from the repository
# Usage: ./remove_submodule.sh <submodule_path> [--force]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
FORCE=false
SUBMODULE_PATH=""

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <submodule_path> [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  submodule_path     The path of the submodule to remove"
    echo ""
    echo "Options:"
    echo "  --force, -f        Force removal without confirmation"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 external/repo           # Remove submodule with confirmation"
    echo "  $0 external/repo --force   # Force remove submodule without confirmation"
    echo "  $0 external/repo -f        # Short form of force flag"
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
        print_status $YELLOW "No .gitmodules file found. This repository has no submodules."
        exit 0
    fi
}

# Function to get list of submodules
get_submodules() {
    local submodules=()

    if [[ -f ".gitmodules" ]]; then
        while IFS= read -r line; do
            if [[ $line =~ ^[[:space:]]*path[[:space:]]*=[[:space:]]*(.+)$ ]]; then
                submodules+=("${BASH_REMATCH[1]}")
            fi
        done < ".gitmodules"
    fi

    echo "${submodules[@]}"
}

# Function to check if submodule exists
check_submodule_exists() {
    local submodule_path=$1
    local submodules
    submodules=($(get_submodules))

    for submodule in "${submodules[@]}"; do
        if [[ "$submodule" == "$submodule_path" ]]; then
            return 0
        fi
    done

    return 1
}

# Function to get submodule URL
get_submodule_url() {
    local submodule_path=$1
    git config --file .gitmodules --get "submodule.$submodule_path.url"
}

# Function to backup submodule information
backup_submodule_info() {
    local submodule_path=$1
    local backup_file=".submodule_remove_backup_$(date +%Y%m%d_%H%M%S).txt"

    print_status $BLUE "Creating backup of submodule information..."

    {
        echo "Submodule removal backup created on $(date)"
        echo "Submodule path: $submodule_path"
        echo "Submodule URL: $(get_submodule_url "$submodule_path")"
        echo "Current commit: $(cd "$submodule_path" && git rev-parse HEAD 2>/dev/null || echo 'Not initialized')"
        echo "Current branch: $(cd "$submodule_path" && git branch --show-current 2>/dev/null || echo 'Unknown')"
        echo ""
        echo "Git status before removal:"
        git status --porcelain
        echo ""
        echo ".gitmodules content:"
        cat .gitmodules
    } > "$backup_file"

    print_status $GREEN "Backup saved to: $backup_file"
}

# Function to check for uncommitted changes
check_uncommitted_changes() {
    local submodule_path=$1

    if [[ -d "$submodule_path" ]]; then
        local changes
        changes=$(cd "$submodule_path" && git status --porcelain 2>/dev/null || echo "")

        if [[ -n "$changes" ]]; then
            print_status $YELLOW "Warning: Submodule '$submodule_path' has uncommitted changes:"
            echo "$changes"
            echo

            if [[ "$FORCE" != true ]]; then
                read -p "Do you want to continue anyway? (y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    print_status $BLUE "Operation cancelled"
                    exit 0
                fi
            fi
        fi
    fi
}

# Function to remove submodule
remove_submodule() {
    local submodule_path=$1

    print_status $BLUE "Removing submodule: $submodule_path"

    # Step 1: Remove the submodule from the working tree and index
    print_status $BLUE "Step 1: Removing from working tree and index..."
    git submodule deinit -f "$submodule_path"

    # Step 2: Remove the submodule from .git/modules
    print_status $BLUE "Step 2: Removing from .git/modules..."
    rm -rf ".git/modules/$submodule_path"

    # Step 3: Remove the submodule directory
    print_status $BLUE "Step 3: Removing submodule directory..."
    git rm -f "$submodule_path"

    # Step 4: Remove the submodule entry from .gitmodules
    print_status $BLUE "Step 4: Removing from .gitmodules..."

    # Create a temporary file for the new .gitmodules content
    local temp_file
    temp_file=$(mktemp)

    # Copy .gitmodules content, excluding the submodule to be removed
    local in_submodule=false
    local submodule_name
    submodule_name=$(basename "$submodule_path")

    while IFS= read -r line; do
        if [[ $line =~ ^\[submodule\ \"([^\"]+)\"\]$ ]]; then
            if [[ "${BASH_REMATCH[1]}" == "$submodule_path" ]]; then
                in_submodule=true
            else
                in_submodule=false
                echo "$line" >> "$temp_file"
            fi
        elif [[ "$in_submodule" == false ]]; then
            echo "$line" >> "$temp_file"
        fi
    done < ".gitmodules"

    # Replace .gitmodules with the filtered content
    mv "$temp_file" ".gitmodules"

    # Step 5: Stage the changes
    print_status $BLUE "Step 5: Staging changes..."
    git add .gitmodules

    print_status $GREEN "Submodule removal completed successfully!"
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force|-f)
                FORCE=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            -*)
                print_status $RED "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$SUBMODULE_PATH" ]]; then
                    SUBMODULE_PATH=$1
                else
                    print_status $RED "Multiple submodule paths specified. Only one is allowed."
                    exit 1
                fi
                shift
                ;;
        esac
    done
}

# Function to confirm removal
confirm_removal() {
    local submodule_path=$1
    local submodule_url
    submodule_url=$(get_submodule_url "$submodule_path")

    echo
    print_status $YELLOW "About to remove submodule:"
    echo "  Path: $submodule_path"
    echo "  URL: $submodule_url"
    echo

    if [[ "$FORCE" != true ]]; then
        read -p "Are you sure you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status $BLUE "Operation cancelled"
            exit 0
        fi
    fi
}

# Main function
main() {
    print_status $BLUE "Starting git submodule removal..."

    # Parse arguments
    parse_args "$@"

    # Check if submodule path is provided
    if [[ -z "$SUBMODULE_PATH" ]]; then
        print_status $RED "Error: Submodule path is required"
        show_usage
        exit 1
    fi

    # Validate environment
    check_git
    check_git_repo
    check_gitmodules

    # Check if submodule exists
    if ! check_submodule_exists "$SUBMODULE_PATH"; then
        print_status $RED "Error: Submodule '$SUBMODULE_PATH' not found"
        print_status $BLUE "Available submodules:"
        local submodules
        submodules=($(get_submodules))
        for submodule in "${submodules[@]}"; do
            echo "  - $submodule"
        done
        exit 1
    fi

    # Backup submodule information
    backup_submodule_info "$SUBMODULE_PATH"

    # Check for uncommitted changes
    check_uncommitted_changes "$SUBMODULE_PATH"

    # Confirm removal
    confirm_removal "$SUBMODULE_PATH"

    # Remove the submodule
    remove_submodule "$SUBMODULE_PATH"

    # Show final status
    echo
    print_status $BLUE "Final repository status:"
    git status

    # Show next steps
    echo ""
    print_status $YELLOW "Next steps:"
    echo "  1. Review the changes: git status"
    echo "  2. Commit the submodule removal: git commit -m 'Remove submodule: $SUBMODULE_PATH'"
    echo "  3. Push the changes: git push"
    echo "  4. If you need to restore the submodule later, use the backup file created"
}

# Run main function with all arguments
main "$@"
