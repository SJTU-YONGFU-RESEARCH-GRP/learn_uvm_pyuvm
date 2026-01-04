#!/bin/bash

# Git Submodule Update Script
# This script updates all git submodules to their latest versions
# Usage: ./update_submodules.sh [--recursive] [--remote] [--branch BRANCH|--main] [--force]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
RECURSIVE=false
REMOTE=false
FORCE=false
SUBMODULE_PATH=""
BRANCH=""

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [submodule_path]"
    echo ""
    echo "Options:"
    echo "  --recursive, -r    Update submodules recursively (including nested submodules)"
    echo "  --remote, -R       Update to the latest commit on the tracked branch"
    echo "  --branch, -b NAME  Checkout and update to latest on specified branch (requires --remote)"
    echo "  --main, -m         Shortcut for --branch main (requires --remote)"
    echo "  --force, -f        Force update even if there are local changes"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Arguments:"
    echo "  submodule_path     (Optional) Path to specific submodule to update"
    echo ""
    echo "Examples:"
    echo "  $0                 # Update all submodules to their tracked commits"
    echo "  $0 --remote        # Update all submodules to latest commits on tracked branches"
    echo "  $0 --remote --main # Update all submodules to latest on main branch"
    echo "  $0 -R -b develop   # Update all submodules to latest on develop branch"
    echo "  $0 --recursive     # Update submodules recursively"
    echo "  $0 external/repo   # Update specific submodule"
    echo "  $0 -r -R -m external/repo  # Update specific submodule recursively to main branch"
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

# Function to check if submodules exist
check_submodules_exist() {
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

# Function to check if specific submodule exists
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

# Function to backup submodule state
backup_submodule_state() {
    local submodule_path=$1
    local backup_file=".submodule_backup_$(date +%Y%m%d_%H%M%S).txt"

    print_status $BLUE "Creating backup of submodule state..."

    {
        echo "Submodule backup created on $(date)"
        echo "Submodule: $submodule_path"
        echo "Current commit: $(cd "$submodule_path" && git rev-parse HEAD 2>/dev/null || echo 'Not initialized')"
        echo "Current branch: $(cd "$submodule_path" && git branch --show-current 2>/dev/null || echo 'Unknown')"
        echo "Status:"
        cd "$submodule_path" && git status --porcelain 2>/dev/null || echo "Not a git repository"
    } > "$backup_file"

    print_status $GREEN "Backup saved to: $backup_file"
}

# Function to checkout branch in submodule
checkout_submodule_branch() {
    local submodule_path=$1
    local branch_name=$2

    if [[ ! -d "$submodule_path" ]]; then
        print_status $YELLOW "Warning: Submodule directory '$submodule_path' does not exist, skipping branch checkout"
        return 1
    fi

    print_status $BLUE "Checking out branch '$branch_name' in submodule: $submodule_path"

    (
        cd "$submodule_path" || exit 1

        # Fetch latest from remote
        print_status $BLUE "Fetching latest from remote..."
        if ! git fetch origin 2>/dev/null; then
            print_status $YELLOW "Warning: Failed to fetch from remote, continuing with existing data"
        fi

        # Check if branch exists remotely
        if git ls-remote --heads origin "$branch_name" >/dev/null 2>&1; then
            # Branch exists remotely
            if git show-ref --verify --quiet refs/heads/"$branch_name"; then
                # Local branch exists, checkout and pull
                git checkout "$branch_name" 2>/dev/null
                git pull origin "$branch_name" 2>/dev/null || true
            else
                # Local branch doesn't exist, create and track remote branch
                git checkout -b "$branch_name" "origin/$branch_name" 2>/dev/null || \
                git checkout --track "origin/$branch_name" 2>/dev/null || {
                    print_status $YELLOW "Warning: Could not checkout branch '$branch_name' for submodule '$submodule_path'"
                    return 1
                }
            fi
            print_status $GREEN "Successfully checked out branch '$branch_name' in submodule '$submodule_path'"
        else
            print_status $YELLOW "Warning: Branch '$branch_name' does not exist on remote for submodule '$submodule_path'"
            print_status $BLUE "Attempting to checkout/create local branch..."
            if git show-ref --verify --quiet refs/heads/"$branch_name"; then
                # Local branch exists
                git checkout "$branch_name" 2>/dev/null
                print_status $GREEN "Checked out local branch '$branch_name' (remote branch does not exist)"
            else
                print_status $YELLOW "Could not checkout branch '$branch_name' - it doesn't exist locally or remotely"
                return 1
            fi
        fi
    )
}

# Function to update submodules
update_submodules() {
    local recursive_flag=""
    local remote_flag=""
    local force_flag=""

    if [[ "$RECURSIVE" == true ]]; then
        recursive_flag="--recursive"
        print_status $BLUE "Updating submodules recursively..."
    else
        print_status $BLUE "Updating submodules..."
    fi

    if [[ "$REMOTE" == true ]]; then
        remote_flag="--remote"
        if [[ -n "$BRANCH" ]]; then
            print_status $BLUE "Will update to latest commits on '$BRANCH' branch after initial update..."
        else
            print_status $BLUE "Updating to latest commits on tracked branches..."
        fi
    fi

    if [[ "$FORCE" == true ]]; then
        force_flag="--force"
        print_status $YELLOW "Force flag enabled - will update even with local changes"
    fi

    # Build the command
    local cmd="git submodule update"

    if [[ -n "$recursive_flag" ]]; then
        cmd="$cmd $recursive_flag"
    fi

    if [[ -n "$remote_flag" ]]; then
        cmd="$cmd $remote_flag"
    fi

    if [[ -n "$force_flag" ]]; then
        cmd="$cmd $force_flag"
    fi

    # Add specific submodule path if provided
    if [[ -n "$SUBMODULE_PATH" ]]; then
        cmd="$cmd $SUBMODULE_PATH"
    fi

    print_status $BLUE "Executing: $cmd"

    # Execute the command
    if eval "$cmd"; then
        print_status $GREEN "Successfully updated submodules"
    else
        print_status $RED "Failed to update submodules"
        exit 1
    fi

    # If branch is specified, checkout that branch in each submodule
    if [[ -n "$BRANCH" ]]; then
        if [[ "$REMOTE" != true ]]; then
            print_status $RED "Error: --branch requires --remote flag"
            exit 1
        fi

        print_status $BLUE "Checking out branch '$BRANCH' in submodules..."

        local submodules_to_update=()
        if [[ -n "$SUBMODULE_PATH" ]]; then
            submodules_to_update=("$SUBMODULE_PATH")
        else
            local submodules
            submodules=($(get_submodules))
            submodules_to_update=("${submodules[@]}")
        fi

        for submodule in "${submodules_to_update[@]}"; do
            if [[ -d "$submodule" ]]; then
                checkout_submodule_branch "$submodule" "$BRANCH"
            fi
        done
    fi
}

# Function to show submodule status
show_submodule_status() {
    print_status $BLUE "Current submodule status:"
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
            --remote|-R)
                REMOTE=true
                shift
                ;;
            --branch|-b)
                if [[ -z "${2:-}" ]] || [[ "${2:-}" =~ ^- ]]; then
                    print_status $RED "Error: --branch requires a branch name"
                    show_usage
                    exit 1
                fi
                BRANCH=$2
                shift 2
                ;;
            --main|-m)
                BRANCH="main"
                REMOTE=true  # --main implies --remote
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

# Main function
main() {
    print_status $BLUE "Starting git submodule update..."

    # Parse arguments
    parse_args "$@"

    # Validate that --branch is only used with --remote
    if [[ -n "$BRANCH" ]] && [[ "$REMOTE" != true ]]; then
        print_status $RED "Error: --branch requires --remote flag"
        show_usage
        exit 1
    fi

    # Validate environment
    check_git
    check_git_repo
    check_submodules_exist

    # Validate specific submodule if provided
    if [[ -n "$SUBMODULE_PATH" ]]; then
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

        print_status $BLUE "Updating specific submodule: $SUBMODULE_PATH"

        # Backup state if updating specific submodule
        if [[ -d "$SUBMODULE_PATH" ]]; then
            backup_submodule_state "$SUBMODULE_PATH"
        fi
    else
        # Show all submodules
        local submodules
        submodules=($(get_submodules))
        print_status $BLUE "Found ${#submodules[@]} submodule(s):"
        for submodule in "${submodules[@]}"; do
            echo "  - $submodule"
        done
        echo
    fi

    # Show current status before update
    show_submodule_status

    # Update submodules
    update_submodules

    # Show status after update
    echo
    show_submodule_status
    echo
    show_submodule_summary

    print_status $GREEN "Submodule update completed successfully!"

    # Show next steps
    echo ""
    print_status $YELLOW "Next steps:"
    echo "  1. Review the changes: git status"
    echo "  2. Commit the submodule updates: git commit -m 'Update submodules'"
    echo "  3. Push the changes: git push"
    echo "  4. If you made changes in submodules, commit and push those too"
}

# Run main function with all arguments
main "$@"
