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

# Installation mode
INSTALL_MODE="submodule"  # submodule, system, or source

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
            sudo apt-get install -y git perl python3 make autoconf g++ flex bison ccache
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
    if [[ ! -d "$VERILATOR_DIR" ]]; then
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
        print_status $BLUE "Verilator submodule directory exists, updating..."
        cd "$VERILATOR_DIR"
        git pull || true
        cd "$PROJECT_ROOT"
    fi
}

# Function to build and install from source
build_from_source() {
    print_status $BLUE "Building Verilator from source..."
    
    # Setup submodule if needed
    setup_submodule
    
    cd "$VERILATOR_DIR"
    
    # Get latest stable version (if not already on a tag)
    print_status $BLUE "Checking out latest stable version..."
    git fetch --tags
    LATEST_TAG=$(git tag | grep -E '^v[0-9]+\.[0-9]+' | sort -V | tail -1)
    if [[ -n "$LATEST_TAG" ]]; then
        git checkout "$LATEST_TAG" || print_status $YELLOW "Could not checkout tag, using current branch"
    fi
    
    # Uninstall previous installation if exists
    if command_exists verilator; then
        print_status $YELLOW "Uninstalling previous Verilator installation..."
        sudo make uninstall 2>/dev/null || true
    fi
    
    # Autoconf setup
    print_status $BLUE "Running autoconf..."
    autoconf
    
    # Configure
    print_status $BLUE "Configuring build..."
    ./configure --prefix=/usr/local
    
    # Build
    print_status $BLUE "Building Verilator (this may take several minutes)..."
    make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
    
    # Install
    print_status $BLUE "Installing Verilator (requires sudo)..."
    sudo make install
    
    # Verify installation
    if command_exists verilator; then
        local version=$(verilator --version 2>&1 | head -1 || echo "unknown")
        print_status $GREEN "Verilator installed successfully: $version"
    else
        print_status $RED "Error: Verilator installation failed - command not found"
        print_status $YELLOW "You may need to add /usr/local/bin to your PATH"
        exit 1
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

