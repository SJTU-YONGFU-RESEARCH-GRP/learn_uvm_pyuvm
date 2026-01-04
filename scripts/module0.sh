#!/bin/bash

# Module 0: Installation and Setup Orchestrator
# This script orchestrates the installation of all tools required for Module 0
# Usage: ./module0.sh [OPTIONS]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Installation options
INSTALL_VERILATOR=true
INSTALL_COCOTB=true
INSTALL_PYUVM=true
VERILATOR_MODE="submodule"  # submodule, system, source
COCOTB_MODE="pip"  # pip, submodule
PYUVM_MODE="pip"  # pip, submodule
USE_VENV=true
VENV_DIR="$PROJECT_ROOT/.venv"
SKIP_CHECKS=false
VERIFY_ONLY=false

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

print_header() {
    local message=$1
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$message${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Module 0: Installation and Setup Orchestrator
This script installs all tools required for pyuvm verification environment.

OPTIONS:
    Installation Control:
        --skip-verilator        Skip Verilator installation
        --skip-cocotb           Skip cocotb installation
        --skip-pyuvm            Skip pyuvm installation
    
    Installation Modes:
        --verilator-mode MODE   Verilator installation mode: submodule (default), system, source
        --cocotb-mode MODE      cocotb installation mode: pip (default), submodule
        --pyuvm-mode MODE       pyuvm installation mode: pip (default), submodule
    
    Environment:
        --venv DIR              Virtual environment directory (default: .venv)
        --no-venv               Install in system Python (not recommended)
    
    Other:
        --skip-checks           Skip pre-installation checks
        --verify-only           Only verify installations (don't install)
        --help, -h              Show this help message

EXAMPLES:
    # Install all tools with default settings
    $0
    
    # Install from git submodules
    $0 --verilator-mode submodule --cocotb-mode submodule --pyuvm-mode submodule
    
    # Install Verilator from system package, Python tools via pip
    $0 --verilator-mode system
    
    # Verify installations only
    $0 --verify-only
    
    # Skip Verilator (if already installed)
    $0 --skip-verilator

TOOLS INSTALLED:
    1. Verilator - Verilog/SystemVerilog simulator
    2. cocotb - Coroutine-based testbench framework
    3. pyuvm - Python implementation of UVM 1.2

EOF
}

# Function to check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local errors=0
    
    # Check Python
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version 2>&1 | awk '{print $2}')
        print_status $GREEN "✓ Python: $python_version"
        
        # Check Python version
        local major=$(echo "$python_version" | cut -d. -f1)
        local minor=$(echo "$python_version" | cut -d. -f2)
        if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 8 ]]; then
            print_status $RED "✗ Python 3.8+ required (found $python_version)"
            errors=$((errors + 1))
        fi
    else
        print_status $RED "✗ Python 3 not found"
        errors=$((errors + 1))
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        local git_version=$(git --version 2>&1 | awk '{print $3}')
        print_status $GREEN "✓ Git: $git_version"
    else
        print_status $RED "✗ Git not found"
        errors=$((errors + 1))
    fi
    
    # Check Make
    if command -v make &> /dev/null; then
        print_status $GREEN "✓ Make: $(make --version 2>&1 | head -1 | awk '{print $3}')"
    else
        print_status $YELLOW "⚠ Make not found (required for building from source)"
    fi
    
    # Check C++ compiler (for Verilator)
    if command -v g++ &> /dev/null || command -v clang++ &> /dev/null; then
        if command -v g++ &> /dev/null; then
            print_status $GREEN "✓ C++ Compiler: $(g++ --version 2>&1 | head -1)"
        else
            print_status $GREEN "✓ C++ Compiler: $(clang++ --version 2>&1 | head -1)"
        fi
    else
        print_status $YELLOW "⚠ C++ Compiler not found (required for Verilator)"
    fi
    
    if [[ $errors -gt 0 ]]; then
        print_status $RED "Prerequisites check failed with $errors error(s)"
        exit 1
    fi
    
    print_status $GREEN "Prerequisites check passed!"
}

# Function to verify installation
verify_tool() {
    local tool_name=$1
    local check_cmd=$2
    
    print_status $BLUE "Verifying $tool_name..."
    
    if eval "$check_cmd" &> /dev/null; then
        print_status $GREEN "✓ $tool_name is installed and working"
        return 0
    else
        print_status $RED "✗ $tool_name is not installed or not working"
        return 1
    fi
}

# Function to verify all installations
verify_installations() {
    print_header "Verifying Installations"
    
    local failed=0
    
    # Verify Verilator
    if [[ "$INSTALL_VERILATOR" == true ]]; then
        if verify_tool "Verilator" "verilator --version"; then
            verilator --version 2>&1 | head -1
        else
            failed=$((failed + 1))
        fi
    fi
    
    # Verify cocotb
    if [[ "$INSTALL_COCOTB" == true ]]; then
        local python_cmd="python3"
        if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
            source "$VENV_DIR/bin/activate"
            python_cmd="python"
        fi
        
        if verify_tool "cocotb" "$python_cmd -c 'import cocotb'"; then
            $python_cmd -c "import cocotb; print(f'  Version: {cocotb.__version__}')" 2>/dev/null || echo "  (version info not available)"
        else
            failed=$((failed + 1))
        fi
    fi
    
    # Verify pyuvm
    if [[ "$INSTALL_PYUVM" == true ]]; then
        local python_cmd="python3"
        if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
            source "$VENV_DIR/bin/activate"
            python_cmd="python"
        fi
        
        if verify_tool "pyuvm" "$python_cmd -c 'import pyuvm'"; then
            $python_cmd -c "import pyuvm; print(f'  Version: {pyuvm.__version__}')" 2>/dev/null || echo "  (version info not available)"
        else
            failed=$((failed + 1))
        fi
    fi
    
    if [[ $failed -eq 0 ]]; then
        print_status $GREEN "All installations verified successfully!"
        return 0
    else
        print_status $RED "Verification failed for $failed tool(s)"
        return 1
    fi
}

# Function to install Verilator
install_verilator() {
    print_header "Installing Verilator"
    
    local args=()
    case $VERILATOR_MODE in
        submodule)
            args+=(--from-submodule)
            ;;
        system)
            args+=(--system)
            ;;
        source)
            args+=(--source)
            ;;
        *)
            print_status $RED "Error: Unknown Verilator mode: $VERILATOR_MODE"
            exit 1
            ;;
    esac
    
    "$SCRIPT_DIR/install_verilator.sh" "${args[@]}"
}

# Function to install cocotb
install_cocotb() {
    print_header "Installing cocotb"
    
    local args=()
    case $COCOTB_MODE in
        pip)
            args+=(--pip)
            ;;
        submodule)
            args+=(--from-submodule --editable)
            ;;
        *)
            print_status $RED "Error: Unknown cocotb mode: $COCOTB_MODE"
            exit 1
            ;;
    esac
    
    if [[ "$USE_VENV" == true ]]; then
        args+=(--venv "$VENV_DIR")
    else
        args+=(--no-venv)
    fi
    
    "$SCRIPT_DIR/install_cocotb.sh" "${args[@]}"
}

# Function to install pyuvm
install_pyuvm() {
    print_header "Installing pyuvm"
    
    local args=()
    case $PYUVM_MODE in
        pip)
            args+=(--pip)
            ;;
        submodule)
            args+=(--from-submodule --editable)
            ;;
        *)
            print_status $RED "Error: Unknown pyuvm mode: $PYUVM_MODE"
            exit 1
            ;;
    esac
    
    if [[ "$USE_VENV" == true ]]; then
        args+=(--venv "$VENV_DIR")
    else
        args+=(--no-venv)
    fi
    
    "$SCRIPT_DIR/install_pyuvm.sh" "${args[@]}"
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-verilator)
                INSTALL_VERILATOR=false
                shift
                ;;
            --skip-cocotb)
                INSTALL_COCOTB=false
                shift
                ;;
            --skip-pyuvm)
                INSTALL_PYUVM=false
                shift
                ;;
            --verilator-mode)
                VERILATOR_MODE="$2"
                shift 2
                ;;
            --cocotb-mode)
                COCOTB_MODE="$2"
                shift 2
                ;;
            --pyuvm-mode)
                PYUVM_MODE="$2"
                shift 2
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
            --skip-checks)
                SKIP_CHECKS=true
                shift
                ;;
            --verify-only)
                VERIFY_ONLY=true
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
    print_header "Module 0: Installation and Setup"
    
    print_status $BLUE "Starting Module 0 installation process..."
    echo ""
    print_status $BLUE "Installation Plan:"
    [[ "$INSTALL_VERILATOR" == true ]] && echo "  ✓ Verilator (mode: $VERILATOR_MODE)"
    [[ "$INSTALL_COCOTB" == true ]] && echo "  ✓ cocotb (mode: $COCOTB_MODE)"
    [[ "$INSTALL_PYUVM" == true ]] && echo "  ✓ pyuvm (mode: $PYUVM_MODE)"
    [[ "$USE_VENV" == true ]] && echo "  ✓ Virtual environment: $VENV_DIR"
    
    # Parse arguments
    parse_args "$@"
    
    # Check prerequisites
    if [[ "$SKIP_CHECKS" == false ]] && [[ "$VERIFY_ONLY" == false ]]; then
        check_prerequisites
    fi
    
    # Verify only mode
    if [[ "$VERIFY_ONLY" == true ]]; then
        verify_installations
        exit $?
    fi
    
    # Install tools
    local install_errors=0
    
    if [[ "$INSTALL_VERILATOR" == true ]]; then
        if ! install_verilator; then
            print_status $RED "Verilator installation failed"
            install_errors=$((install_errors + 1))
        fi
    fi
    
    if [[ "$INSTALL_COCOTB" == true ]]; then
        if ! install_cocotb; then
            print_status $RED "cocotb installation failed"
            install_errors=$((install_errors + 1))
        fi
    fi
    
    if [[ "$INSTALL_PYUVM" == true ]]; then
        if ! install_pyuvm; then
            print_status $RED "pyuvm installation failed"
            install_errors=$((install_errors + 1))
        fi
    fi
    
    # Verify installations
    echo ""
    if ! verify_installations; then
        install_errors=$((install_errors + 1))
    fi
    
    # Summary
    print_header "Installation Summary"
    
    if [[ $install_errors -eq 0 ]]; then
        print_status $GREEN "✓ All tools installed successfully!"
        echo ""
        print_status $BLUE "Next steps:"
        if [[ "$USE_VENV" == true ]]; then
            echo "  1. Activate virtual environment: source $VENV_DIR/bin/activate"
        fi
        echo "  2. Proceed to Module 1: Python and Verification Basics"
        echo "  3. Create your first testbench"
        echo ""
        print_status $GREEN "Module 0 setup completed successfully!"
    else
        print_status $RED "✗ Installation completed with $install_errors error(s)"
        echo ""
        print_status $YELLOW "Please review the errors above and try again."
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

