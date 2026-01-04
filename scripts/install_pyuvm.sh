#!/bin/bash

# pyuvm Installation Script
# Installs pyuvm from git submodule or via pip
# Usage: ./install_pyuvm.sh [--from-submodule] [--pip] [--venv] [--editable]

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
PYUVM_REPO="git@github.com:pyuvm/pyuvm.git"

# Installation options
INSTALL_MODE="pip"  # pip or submodule
USE_VENV=true
VENV_DIR="$PROJECT_ROOT/.venv"
EDITABLE=false

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
    echo "  --pip              Install via pip (default)"
    echo "  --from-submodule   Install from git submodule in tools/pyuvm"
    echo "  --venv DIR         Use virtual environment at DIR (default: .venv)"
    echo "  --no-venv          Install in system Python (not recommended)"
    echo "  --editable, -e     Install in editable mode (for submodule install)"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                      # Install via pip in .venv"
    echo "  $0 --from-submodule -e  # Install from submodule in editable mode"
    echo "  $0 --no-venv            # Install in system Python (not recommended)"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python installation
check_python() {
    if ! command_exists python3; then
        print_status $RED "Error: python3 is not installed"
        exit 1
    fi
    
    local python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_status $BLUE "Found Python: $python_version"
    
    # Check if Python version is >= 3.8
    local major=$(echo "$python_version" | cut -d. -f1)
    local minor=$(echo "$python_version" | cut -d. -f2)
    
    if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 8 ]]; then
        print_status $RED "Error: Python 3.8+ is required (found $python_version)"
        exit 1
    fi
}

# Function to setup virtual environment
setup_venv() {
    if [[ "$USE_VENV" == false ]]; then
        return
    fi
    
    if [[ ! -d "$VENV_DIR" ]] || [[ ! -f "$VENV_DIR/bin/activate" ]]; then
        if [[ -d "$VENV_DIR" ]]; then
            print_status $YELLOW "Virtual environment directory exists but is invalid, recreating..."
            rm -rf "$VENV_DIR"
        fi
        print_status $BLUE "Creating virtual environment at $VENV_DIR..."
        python3 -m venv "$VENV_DIR"
    else
        print_status $BLUE "Virtual environment already exists at $VENV_DIR"
    fi
    
    # Activate virtual environment
    print_status $BLUE "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    print_status $BLUE "Upgrading pip..."
    pip install --upgrade pip setuptools wheel
}

# Function to setup git submodule
setup_submodule() {
    if [[ ! -d "$PYUVM_DIR" ]]; then
        print_status $BLUE "Setting up pyuvm git submodule..."
        
        # Check if we're in a git repository
        if git rev-parse --git-dir > /dev/null 2>&1; then
            print_status $BLUE "Adding pyuvm as git submodule..."
            "$SCRIPT_DIR/add_submodule.sh" "$PYUVM_REPO" "tools/pyuvm" || {
                print_status $YELLOW "Failed to add as submodule, cloning directly..."
                git clone "$PYUVM_REPO" "$PYUVM_DIR"
            }
        else
            print_status $YELLOW "Not in a git repository, cloning directly..."
            git clone "$PYUVM_REPO" "$PYUVM_DIR"
        fi
    else
        print_status $BLUE "pyuvm submodule directory exists, updating..."
        cd "$PYUVM_DIR"
        git pull || true
        cd "$PROJECT_ROOT"
    fi
}

# Function to install via pip
install_via_pip() {
    print_status $BLUE "Installing pyuvm via pip..."
    
    if [[ "$USE_VENV" == true ]]; then
        setup_venv
    fi
    
    # Install pyuvm
    print_status $BLUE "Installing pyuvm..."
    pip install pyuvm
    
    # Verify installation
    if python3 -c "import pyuvm" 2>/dev/null; then
        local version=$(python3 -c "import pyuvm; print(pyuvm.__version__)" 2>/dev/null || echo "unknown")
        print_status $GREEN "pyuvm installed successfully: version $version"
    else
        print_status $RED "Error: pyuvm installation failed"
        exit 1
    fi
}

# Function to install from submodule
install_from_submodule() {
    print_status $BLUE "Installing pyuvm from git submodule..."
    
    # Setup submodule
    setup_submodule
    
    # Setup virtual environment
    if [[ "$USE_VENV" == true ]]; then
        setup_venv
    fi
    
    # Install dependencies first
    cd "$PYUVM_DIR"
    
    if [[ -f "requirements.txt" ]]; then
        print_status $BLUE "Installing pyuvm dependencies..."
        pip install -r requirements.txt
    fi
    
    if [[ -f "requirements-dev.txt" ]]; then
        print_status $BLUE "Installing pyuvm dev dependencies..."
        pip install -r requirements-dev.txt || true
    fi
    
    if [[ -f "pyproject.toml" ]] || [[ -f "setup.py" ]]; then
        # Install pyuvm
        print_status $BLUE "Installing pyuvm from source..."
        if [[ "$EDITABLE" == true ]]; then
            pip install -e .
            print_status $BLUE "Installed in editable mode"
        else
            pip install .
        fi
    else
        print_status $RED "Error: Could not find setup.py or pyproject.toml in $PYUVM_DIR"
        exit 1
    fi
    
    cd "$PROJECT_ROOT"
    
    # Verify installation
    if python3 -c "import pyuvm" 2>/dev/null; then
        local version=$(python3 -c "import pyuvm; print(pyuvm.__version__)" 2>/dev/null || echo "unknown")
        print_status $GREEN "pyuvm installed successfully: version $version"
    else
        print_status $RED "Error: pyuvm installation failed"
        exit 1
    fi
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --pip)
                INSTALL_MODE="pip"
                shift
                ;;
            --from-submodule)
                INSTALL_MODE="submodule"
                shift
                ;;
            --venv)
                USE_VENV=true
                VENV_DIR="$2"
                shift 2
                ;;
            --no-venv)
                USE_VENV=false
                shift
                ;;
            --editable|-e)
                EDITABLE=true
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
    print_status $BLUE "Starting pyuvm installation..."
    
    # Parse arguments
    parse_args "$@"
    
    # Check Python
    check_python
    
    # Create tools directory if it doesn't exist
    mkdir -p "$TOOLS_DIR"
    
    # Install based on mode
    case $INSTALL_MODE in
        pip)
            install_via_pip
            ;;
        submodule)
            install_from_submodule
            ;;
        *)
            print_status $RED "Error: Unknown installation mode: $INSTALL_MODE"
            exit 1
            ;;
    esac
    
    print_status $GREEN "pyuvm installation completed successfully!"
    
    if [[ "$USE_VENV" == true ]]; then
        print_status $BLUE "Virtual environment is at: $VENV_DIR"
        print_status $BLUE "To activate: source $VENV_DIR/bin/activate"
    fi
    
    print_status $BLUE "Verify installation with: python3 -c 'import pyuvm; print(pyuvm.__version__)'"
}

# Run main function with all arguments
main "$@"

