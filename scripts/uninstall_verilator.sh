#!/bin/bash

# Verilator Uninstallation Script
# Uninstalls Verilator installed via this script
# Usage: ./uninstall_verilator.sh [--system] [--keep-submodule]

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
VERILATOR_DIR="$TOOLS_DIR/verilator"

# Options
UNINSTALL_SYSTEM=false
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
    echo "  --system           Also uninstall system package (apt/yum/brew)"
    echo "  --keep-submodule   Keep the git submodule (don't remove it)"
    echo "  --help, -h         Show this help message"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            echo "debian"
        elif command_exists yum; then
            echo "rhel"
        elif command_exists dnf; then
            echo "fedora"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Function to uninstall from source build
uninstall_from_source() {
    if [[ -d "$VERILATOR_DIR" ]]; then
        print_status $BLUE "Uninstalling Verilator from source build..."
        cd "$VERILATOR_DIR"
        
        if [[ -f "Makefile" ]]; then
            print_status $BLUE "Running make uninstall..."
            sudo make uninstall 2>/dev/null || print_status $YELLOW "make uninstall failed or already uninstalled"
        else
            print_status $YELLOW "Makefile not found, skipping make uninstall"
        fi
        
        cd "$PROJECT_ROOT"
    else
        print_status $YELLOW "Verilator source directory not found: $VERILATOR_DIR"
    fi
}

# Function to uninstall system package
uninstall_system_package() {
    local os=$(detect_os)
    print_status $BLUE "Uninstalling Verilator system package..."
    
    case $os in
        debian)
            sudo apt-get remove -y verilator || true
            sudo apt-get autoremove -y || true
            ;;
        rhel|fedora)
            if command_exists dnf; then
                sudo dnf remove -y verilator || true
            else
                sudo yum remove -y verilator || true
            fi
            ;;
        macos)
            brew uninstall verilator || true
            ;;
        *)
            print_status $YELLOW "Warning: System package uninstallation not supported on this OS"
            ;;
    esac
}

# Function to remove submodule
remove_submodule() {
    if [[ -d "$VERILATOR_DIR" ]]; then
        print_status $BLUE "Removing Verilator git submodule..."
        
        # Check if we're in a git repository
        if git rev-parse --git-dir > /dev/null 2>&1; then
            # Check if it's a submodule
            if git config --file .gitmodules --get-regexp path | grep -q "tools/verilator"; then
                print_status $BLUE "Removing git submodule..."
                "$SCRIPT_DIR/remove_submodule.sh" "tools/verilator" || {
                    print_status $YELLOW "Failed to remove submodule properly, removing directory..."
                    rm -rf "$VERILATOR_DIR"
                    git config --file .gitmodules --remove-section submodule.tools/verilator 2>/dev/null || true
                    git config --remove-section submodule.tools/verilator 2>/dev/null || true
                }
            else
                print_status $BLUE "Not a git submodule, removing directory..."
                rm -rf "$VERILATOR_DIR"
            fi
        else
            print_status $BLUE "Not in a git repository, removing directory..."
            rm -rf "$VERILATOR_DIR"
        fi
    else
        print_status $YELLOW "Verilator directory not found: $VERILATOR_DIR"
    fi
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --system)
                UNINSTALL_SYSTEM=true
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
    print_status $BLUE "Starting Verilator uninstallation..."
    
    # Parse arguments
    parse_args "$@"
    
    # Check if Verilator is installed
    if ! command_exists verilator; then
        print_status $YELLOW "Verilator is not installed or not in PATH"
    else
        local version=$(verilator --version 2>&1 | head -1 || echo "unknown")
        print_status $BLUE "Found Verilator: $version"
    fi
    
    # Uninstall from source build
    uninstall_from_source
    
    # Uninstall system package if requested
    if [[ "$UNINSTALL_SYSTEM" == true ]]; then
        uninstall_system_package
    fi
    
    # Remove submodule if not keeping it
    if [[ "$KEEP_SUBMODULE" == false ]]; then
        remove_submodule
    else
        print_status $BLUE "Keeping git submodule as requested"
    fi
    
    # Verify uninstallation
    if command_exists verilator; then
        print_status $YELLOW "Warning: Verilator command still available. You may need to:"
        echo "  - Restart your terminal"
        echo "  - Check other installation locations"
        echo "  - Remove from PATH manually"
    else
        print_status $GREEN "Verilator uninstallation completed successfully!"
    fi
}

# Run main function with all arguments
main "$@"

