#!/bin/bash

# pyuvm Uninstallation Script
# Uninstalls pyuvm installed via this script
# Usage: ./uninstall_pyuvm.sh [--venv DIR] [--keep-submodule]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TOOLS_DIR="$PROJECT_ROOT/tools"
PYUVM_DIR="$TOOLS_DIR/pyuvm"

# Options
VENV_DIR="$PROJECT_ROOT/.venv"
USE_VENV=true
KEEP_SUBMODULE=false

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
    echo "  --venv DIR         Virtual environment directory (default: .venv)"
    echo "  --no-venv          Uninstall from system Python"
    echo "  --keep-submodule   Keep the git submodule (don't remove it)"
    echo "  --help, -h         Show this help message"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to uninstall via pip
uninstall_via_pip() {
    local python_cmd="python3"
    local pip_cmd="pip"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        print_status $BLUE "Using virtual environment at $VENV_DIR..."
        source "$VENV_DIR/bin/activate"
        python_cmd="python"
        pip_cmd="pip"
    elif [[ "$USE_VENV" == true ]]; then
        print_status $YELLOW "Virtual environment not found at $VENV_DIR, using system Python"
    fi
    
    print_status $BLUE "Uninstalling pyuvm via pip..."
    
    # Check if pyuvm is installed
    if $python_cmd -c "import pyuvm" 2>/dev/null; then
        local version=$($python_cmd -c "import pyuvm; print(pyuvm.__version__)" 2>/dev/null || echo "unknown")
        print_status $BLUE "Found pyuvm: version $version"
        $pip_cmd uninstall -y pyuvm || print_status $YELLOW "pip uninstall failed, trying pip3..."
        $python_cmd -m pip uninstall -y pyuvm || true
    else
        print_status $YELLOW "pyuvm is not installed in this environment"
    fi
}

# Function to remove submodule
remove_submodule() {
    if [[ -d "$PYUVM_DIR" ]]; then
        print_status $BLUE "Removing pyuvm git submodule..."
        
        # Check if we're in a git repository
        if git rev-parse --git-dir > /dev/null 2>&1; then
            # Check if it's a submodule
            if git config --file .gitmodules --get-regexp path | grep -q "tools/pyuvm"; then
                print_status $BLUE "Removing git submodule..."
                "$SCRIPT_DIR/remove_submodule.sh" "tools/pyuvm" || {
                    print_status $YELLOW "Failed to remove submodule properly, removing directory..."
                    rm -rf "$PYUVM_DIR"
                    git config --file .gitmodules --remove-section submodule.tools/pyuvm 2>/dev/null || true
                    git config --remove-section submodule.tools/pyuvm 2>/dev/null || true
                }
            else
                print_status $BLUE "Not a git submodule, removing directory..."
                rm -rf "$PYUVM_DIR"
            fi
        else
            print_status $BLUE "Not in a git repository, removing directory..."
            rm -rf "$PYUVM_DIR"
        fi
    else
        print_status $YELLOW "pyuvm directory not found: $PYUVM_DIR"
    fi
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --venv)
                USE_VENV=true
                VENV_DIR="$2"
                shift 2
                ;;
            --no-venv)
                USE_VENV=false
                shift
                ;;
            --keep-submodule)
                KEEP_SUBMODULE=true
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
    print_status $BLUE "Starting pyuvm uninstallation..."
    
    # Parse arguments
    parse_args "$@"
    
    # Uninstall via pip
    uninstall_via_pip
    
    # Remove submodule if not keeping it
    if [[ "$KEEP_SUBMODULE" == false ]]; then
        remove_submodule
    else
        print_status $BLUE "Keeping git submodule as requested"
    fi
    
    # Verify uninstallation
    local python_cmd="python3"
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
        python_cmd="python"
    fi
    
    if $python_cmd -c "import pyuvm" 2>/dev/null; then
        print_status $YELLOW "Warning: pyuvm is still importable. You may need to:"
        echo "  - Check other Python environments"
        echo "  - Restart your terminal"
    else
        print_status $GREEN "pyuvm uninstallation completed successfully!"
    fi
}

# Run main function with all arguments
main "$@"

