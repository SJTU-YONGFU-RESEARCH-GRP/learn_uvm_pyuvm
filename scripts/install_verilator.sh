#!/bin/bash

# Verilator Installation Script
# Installs Verilator from git submodule or builds from source
# Usage: ./install_verilator.sh [--from-submodule] [--system]

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
VERILATOR_REPO="git@github.com:verilator/verilator.git"
VERILATOR_INSTALL_PREFIX="/usr/local"  # Default system installation
LOCAL_INSTALL=false  # If true, install to project-local directory

# Installation mode
INSTALL_MODE="submodule"  # submodule, system, or source
FORCE_REINSTALL=false

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
    echo "  --from-submodule    Install from git submodule in tools/verilator (default)"
    echo "  --system            Install using system package manager (apt/yum/brew)"
    echo "  --source            Build from source (clone if submodule doesn't exist)"
    echo "  --force             Force reinstall even if Verilator is already installed"
    echo "  --local             Install to project-local directory (no sudo required)"
    echo "  --prefix PREFIX     Installation prefix (default: /usr/local)"
    echo "  --help, -h          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                  # Install from submodule"
    echo "  $0 --system         # Install via package manager"
    echo "  $0 --source         # Build from source"
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
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to install system dependencies
install_system_dependencies() {
    local os=$(detect_os)
    print_status $BLUE "Installing system dependencies for $os..."
    
    case $os in
        debian)
            sudo apt-get update
            sudo apt-get install -y git perl python3 make autoconf g++ flex bison ccache help2man
            sudo apt-get install -y libgoogle-perftools-dev numactl perl-doc
            ;;
        rhel|fedora)
            if command_exists dnf; then
                sudo dnf install -y git perl python3 make autoconf gcc-c++ flex bison ccache
                sudo dnf install -y gperftools-devel numactl perl-Pod-Html
            else
                sudo yum install -y git perl python3 make autoconf gcc-c++ flex bison ccache
                sudo yum install -y gperftools-devel numactl perl-Pod-Html
            fi
            ;;
        macos)
            if ! command_exists brew; then
                print_status $RED "Error: Homebrew is required for macOS installation"
                exit 1
            fi
            brew install git perl python3 autoconf flex bison ccache
            ;;
        *)
            print_status $YELLOW "Warning: Unknown OS. Please install dependencies manually:"
            echo "  git, perl, python3, make, autoconf, g++/gcc-c++, flex, bison, ccache"
            ;;
    esac
}

# Function to check if Verilator is already installed
check_verilator_installed() {
    if command_exists verilator; then
        local version=$(verilator --version 2>&1 | head -1 || echo "unknown")
        print_status $YELLOW "Verilator is already installed: $version"
        
        if [[ "$FORCE_REINSTALL" == true ]]; then
            print_status $BLUE "Force reinstall enabled, proceeding with installation..."
            return 0
        fi
        
        read -p "Do you want to reinstall? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status $BLUE "Skipping installation"
            exit 0
        fi
    fi
}

# Function to install from system package manager
install_from_system() {
    local os=$(detect_os)
    print_status $BLUE "Installing Verilator from system package manager..."
    
    case $os in
        debian)
            sudo apt-get update
            sudo apt-get install -y verilator
            ;;
        rhel|fedora)
            if command_exists dnf; then
                sudo dnf install -y verilator
            else
                sudo yum install -y verilator
            fi
            ;;
        macos)
            brew install verilator
            ;;
        *)
            print_status $RED "Error: System package manager installation not supported on this OS"
            exit 1
            ;;
    esac
    
    # Verify installation
    if command_exists verilator; then
        local version=$(verilator --version 2>&1 | head -1 || echo "unknown")
        print_status $GREEN "Verilator installed successfully: $version"
    else
        print_status $RED "Error: Verilator installation failed"
        exit 1
    fi
}

# Function to setup git submodule
setup_submodule() {
    # Check if directory exists and is a valid git repository
    if [[ -d "$VERILATOR_DIR" ]] && [[ -d "$VERILATOR_DIR/.git" ]]; then
        print_status $BLUE "Verilator submodule directory exists, updating..."
        cd "$VERILATOR_DIR"
        git pull || true
        cd "$PROJECT_ROOT"
    elif [[ -d "$VERILATOR_DIR" ]] && [[ ! -d "$VERILATOR_DIR/.git" ]]; then
        # Directory exists but is not a git repository (empty or corrupted)
        print_status $YELLOW "Verilator directory exists but is not a git repository, removing and re-cloning..."
        rm -rf "$VERILATOR_DIR"
        print_status $BLUE "Setting up Verilator git submodule..."
        
        # Check if we're in a git repository
        if git rev-parse --git-dir > /dev/null 2>&1; then
            print_status $BLUE "Adding Verilator as git submodule..."
            "$SCRIPT_DIR/add_submodule.sh" "$VERILATOR_REPO" "tools/verilator" || {
                print_status $YELLOW "Failed to add as submodule, cloning directly..."
                git clone "$VERILATOR_REPO" "$VERILATOR_DIR"
            }
        else
            print_status $YELLOW "Not in a git repository, cloning directly..."
            git clone "$VERILATOR_REPO" "$VERILATOR_DIR"
        fi
    else
        # Directory doesn't exist
        print_status $BLUE "Setting up Verilator git submodule..."
        
        # Check if we're in a git repository
        if git rev-parse --git-dir > /dev/null 2>&1; then
            print_status $BLUE "Adding Verilator as git submodule..."
            "$SCRIPT_DIR/add_submodule.sh" "$VERILATOR_REPO" "tools/verilator" || {
                print_status $YELLOW "Failed to add as submodule, cloning directly..."
                git clone "$VERILATOR_REPO" "$VERILATOR_DIR"
            }
        else
            print_status $YELLOW "Not in a git repository, cloning directly..."
            git clone "$VERILATOR_REPO" "$VERILATOR_DIR"
        fi
    fi
}

# Function to build and install from source
build_from_source() {
    print_status $BLUE "Building Verilator from source..."
    
    # Setup submodule if needed
    if ! setup_submodule; then
        print_status $RED "Error: Failed to setup Verilator submodule"
        exit 1
    fi
    
    # Verify the directory is now a valid git repository
    if [[ ! -d "$VERILATOR_DIR/.git" ]]; then
        print_status $RED "Error: Verilator directory is not a valid git repository"
        exit 1
    fi
    
    cd "$VERILATOR_DIR" || {
        print_status $RED "Error: Failed to change to Verilator directory: $VERILATOR_DIR"
        exit 1
    }
    
    # Get latest stable version (if not already on a tag)
    print_status $BLUE "Checking out latest stable version..."
    if ! git fetch --tags; then
        print_status $YELLOW "Warning: Failed to fetch tags, continuing with current branch"
    fi
    
    LATEST_TAG=$(git tag | grep -E '^v[0-9]+\.[0-9]+' | sort -V | tail -1 || echo "")
    if [[ -n "$LATEST_TAG" ]]; then
        if ! git checkout "$LATEST_TAG"; then
            print_status $YELLOW "Warning: Could not checkout tag $LATEST_TAG, using current branch"
        else
            print_status $GREEN "Checked out tag: $LATEST_TAG"
        fi
    else
        print_status $YELLOW "Warning: No version tags found, using current branch"
    fi
    
    # Uninstall previous installation if exists
    if command_exists verilator; then
        print_status $YELLOW "Uninstalling previous Verilator installation..."
        sudo make uninstall 2>/dev/null || true
    fi
    
    # Autoconf setup
    print_status $BLUE "Running autoconf..."
    if ! autoconf; then
        print_status $RED "Error: autoconf failed"
        cd "$PROJECT_ROOT"
        exit 1
    fi
    
    # Configure
    print_status $BLUE "Configuring build..."
    if [[ "$LOCAL_INSTALL" == true ]]; then
        VERILATOR_INSTALL_PREFIX="$PROJECT_ROOT/tools/verilator-install"
        mkdir -p "$VERILATOR_INSTALL_PREFIX"
        print_status $BLUE "Installing to local directory: $VERILATOR_INSTALL_PREFIX"
    fi
    
    if ! ./configure --prefix="$VERILATOR_INSTALL_PREFIX"; then
        print_status $RED "Error: configure failed"
        cd "$PROJECT_ROOT"
        exit 1
    fi
    
    # Build
    print_status $BLUE "Building Verilator (this may take several minutes)..."
    local num_cores=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
    
    # Check if help2man is available (needed for man pages, but not critical)
    local has_help2man=false
    if command_exists help2man; then
        has_help2man=true
    else
        print_status $YELLOW "Warning: help2man not found - man pages will not be generated"
    fi
    
    # Build - if help2man is missing, the build may fail on man page generation
    # but the verilator binary should still be built
    set +e  # Temporarily disable exit on error for build
    make -j"$num_cores"
    local make_exit_code=$?
    set -e  # Re-enable exit on error
    
    # Check if verilator binary was built (even if man page generation failed)
    if [[ ! -f "bin/verilator" ]] && [[ ! -f "bin/verilator_bin" ]]; then
        print_status $RED "Error: Build failed - verilator binary not found"
        if [[ "$has_help2man" == false ]]; then
            print_status $YELLOW "Note: help2man is missing. Install it with: sudo apt-get install help2man"
        fi
        cd "$PROJECT_ROOT"
        exit 1
    fi
    
    # Build succeeded (even if man page generation failed)
    if [[ $make_exit_code -ne 0 ]] && [[ "$has_help2man" == false ]]; then
        print_status $YELLOW "Build completed (verilator binary built, man pages skipped due to missing help2man)"
    elif [[ $make_exit_code -eq 0 ]]; then
        print_status $GREEN "Build completed successfully"
    fi
    
    # Install
    if [[ "$LOCAL_INSTALL" == true ]]; then
        print_status $BLUE "Installing Verilator to local directory..."
        if ! make install; then
            print_status $RED "Error: Installation failed"
            cd "$PROJECT_ROOT"
            exit 1
        fi
        print_status $GREEN "Verilator installed to: $VERILATOR_INSTALL_PREFIX"
        print_status $YELLOW "Add to PATH: export PATH=\"$VERILATOR_INSTALL_PREFIX/bin:\$PATH\""
    else
        print_status $BLUE "Installing Verilator (requires sudo)..."
        if ! sudo make install; then
            print_status $RED "Error: Installation failed"
            cd "$PROJECT_ROOT"
            exit 1
        fi
    fi
    
    # Verify installation
    if [[ "$LOCAL_INSTALL" == true ]]; then
        # For local install, check the installed binary directly
        if [[ -f "$VERILATOR_INSTALL_PREFIX/bin/verilator" ]]; then
            local version=$("$VERILATOR_INSTALL_PREFIX/bin/verilator" --version 2>&1 | head -1 || echo "unknown")
            print_status $GREEN "Verilator installed successfully: $version"
            print_status $YELLOW "Note: Add to PATH: export PATH=\"$VERILATOR_INSTALL_PREFIX/bin:\$PATH\""
        else
            print_status $RED "Error: Verilator installation failed - binary not found"
            cd "$PROJECT_ROOT"
            exit 1
        fi
    else
        # For system install, check if verilator is in PATH
        if command_exists verilator; then
            local version=$(verilator --version 2>&1 | head -1 || echo "unknown")
            print_status $GREEN "Verilator installed successfully: $version"
        else
            print_status $RED "Error: Verilator installation failed - command not found"
            print_status $YELLOW "You may need to add $VERILATOR_INSTALL_PREFIX/bin to your PATH"
            cd "$PROJECT_ROOT"
            exit 1
        fi
    fi
    
    cd "$PROJECT_ROOT"
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --from-submodule)
                INSTALL_MODE="submodule"
                shift
                ;;
            --system)
                INSTALL_MODE="system"
                shift
                ;;
            --source)
                INSTALL_MODE="source"
                shift
                ;;
            --force)
                FORCE_REINSTALL=true
                shift
                ;;
            --local)
                LOCAL_INSTALL=true
                shift
                ;;
            --prefix)
                VERILATOR_INSTALL_PREFIX="$2"
                shift 2
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
    print_status $BLUE "Starting Verilator installation..."
    
    # Parse arguments
    parse_args "$@"
    
    # Check if already installed
    check_verilator_installed
    
    # Create tools directory if it doesn't exist
    mkdir -p "$TOOLS_DIR"
    
    case $INSTALL_MODE in
        system)
            install_from_system
            ;;
        source|submodule)
            # Install system dependencies
            install_system_dependencies
            
            # Build from source
            build_from_source
            ;;
        *)
            print_status $RED "Error: Unknown installation mode: $INSTALL_MODE"
            exit 1
            ;;
    esac
    
    print_status $GREEN "Verilator installation completed successfully!"
    print_status $BLUE "Verify installation with: verilator --version"
}

# Run main function with all arguments
main "$@"

