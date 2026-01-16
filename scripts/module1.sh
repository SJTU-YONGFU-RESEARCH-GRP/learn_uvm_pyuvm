#!/bin/bash

# Module 1: Python and Verification Basics Orchestrator
# This script runs examples and tests for Module 1
# Usage: ./module1.sh [OPTIONS]

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
MODULE1_DIR="$PROJECT_ROOT/module1"
VENV_DIR="$PROJECT_ROOT/.venv"

# Options
RUN_PYTHON_BASICS=true
RUN_DECORATORS=true
RUN_ASYNC_AWAIT=true
RUN_DATA_STRUCTURES=true
RUN_ERROR_HANDLING=true
RUN_COCOTB_TESTS=true
RUN_PYUVM_TESTS=true
USE_VENV=true
SIMULATOR="verilator"

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

Module 1: Python and Verification Basics
This script runs examples and tests for Module 1.

OPTIONS:
    Python Examples:
        --python-basics        Run Python class basics examples
        --decorators           Run decorators and context managers examples
        --async-await          Run async/await examples
        --data-structures      Run data structures examples
        --error-handling       Run error handling and logging examples
        --all-python           Run all Python examples (default)
        --skip-python          Skip all Python examples
    
    Tests:
        --cocotb-tests         Run cocotb tests
        --pyuvm-tests          Run pyuvm tests
        --all-tests            Run all tests
    
    Environment:
        --venv DIR             Virtual environment directory (default: .venv)
        --no-venv              Don't use virtual environment
        --sim SIMULATOR        Simulator to use (default: verilator)
    
    Other:
        --help, -h             Show this help message

EXAMPLES:
    # Run all Python examples
    $0
    
    # Run only Python basics
    $0 --python-basics
    
    # Run cocotb tests
    $0 --cocotb-tests
    
    # Run everything
    $0 --all-python --all-tests

EOF
}

# Function to check prerequisites
check_prerequisites() {
    print_status $BLUE "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_status $RED "Error: python3 not found"
        exit 1
    fi
    
    # Check if virtual environment exists (if using venv)
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
        print_status $GREEN "Using virtual environment: $VENV_DIR"
    elif [[ "$USE_VENV" == true ]]; then
        print_status $YELLOW "Warning: Virtual environment not found, using system Python"
        USE_VENV=false
    fi
    
    # Check cocotb (if running tests)
    if [[ "$RUN_COCOTB_TESTS" == true ]] || [[ "$RUN_PYUVM_TESTS" == true ]]; then
        if ! python3 -c "import cocotb" 2>/dev/null; then
            print_status $RED "Error: cocotb not found. Please install it first."
            exit 1
        fi
        
        if [[ "$RUN_PYUVM_TESTS" == true ]]; then
            if ! python3 -c "import pyuvm" 2>/dev/null; then
                print_status $RED "Error: pyuvm not found. Please install it first."
                exit 1
            fi
        fi
        
        # Check simulator
        if [[ "$SIMULATOR" == "verilator" ]]; then
            if ! command -v verilator &> /dev/null; then
                print_status $RED "Error: verilator not found. Please install it first."
                exit 1
            fi
        fi
    fi
    
    print_status $GREEN "Prerequisites check passed"
}

# Function to run Python example
run_python_example() {
    local example_file=$1
    local example_name=$2
    
    print_header "Running: $example_name"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    if python3 "$example_file"; then
        print_status $GREEN "✓ $example_name completed successfully"
        return 0
    else
        print_status $RED "✗ $example_name failed"
        return 1
    fi
}

# Function to run cocotb tests
run_cocotb_tests() {
    print_header "Running cocotb Tests"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    cd "$MODULE1_DIR/tests/cocotb_tests" || {
        print_status $RED "Error: Failed to change to cocotb tests directory"
        return 1
    }
    
    local failed=0
    
    # Run AND gate tests
    print_status $BLUE "Running AND gate tests..."
    # Clean previous build to ensure correct TOPLEVEL
    make clean >/dev/null 2>&1 || true
    set +e  # Temporarily disable exit on error to capture exit code
    make SIM="$SIMULATOR" TEST=test_and_gate 2>&1 | tee /tmp/cocotb_and_gate.log
    local exit_code=${PIPESTATUS[0]}
    set -e  # Re-enable exit on error
    if [[ $exit_code -eq 0 ]]; then
        print_status $GREEN "✓ AND gate tests passed"
    else
        print_status $RED "✗ AND gate tests failed (exit code: $exit_code)"
        print_status $YELLOW "Check /tmp/cocotb_and_gate.log for details"
        failed=$((failed + 1))
    fi
    
    # Run counter tests
    print_status $BLUE "Running counter tests..."
    # Clean previous build to ensure correct TOPLEVEL
    make clean >/dev/null 2>&1 || true
    set +e  # Temporarily disable exit on error to capture exit code
    make SIM="$SIMULATOR" TEST=test_counter 2>&1 | tee /tmp/cocotb_counter.log
    local exit_code=${PIPESTATUS[0]}
    set -e  # Re-enable exit on error
    if [[ $exit_code -eq 0 ]]; then
        print_status $GREEN "✓ Counter tests passed"
    else
        print_status $RED "✗ Counter tests failed (exit code: $exit_code)"
        print_status $YELLOW "Check /tmp/cocotb_counter.log for details"
        failed=$((failed + 1))
    fi
    
    cd "$PROJECT_ROOT"
    
    if [[ $failed -eq 0 ]]; then
        print_status $GREEN "All cocotb tests passed"
        return 0
    else
        print_status $RED "$failed cocotb test(s) failed"
        return 1
    fi
}

# Function to run pyuvm tests
run_pyuvm_tests() {
    print_header "Running pyuvm Tests"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    cd "$MODULE1_DIR/tests/pyuvm_tests" || {
        print_status $RED "Error: Failed to change to pyuvm tests directory"
        return 1
    }
    
    print_status $BLUE "Running pyuvm AND gate test..."
    set +e  # Temporarily disable exit on error to capture exit code
    make SIM="$SIMULATOR" TEST=test_and_gate_uvm 2>&1 | tee /tmp/pyuvm_and_gate.log
    local exit_code=${PIPESTATUS[0]}
    set -e  # Re-enable exit on error
    if [[ $exit_code -eq 0 ]]; then
        print_status $GREEN "✓ pyuvm AND gate test passed"
        cd "$PROJECT_ROOT"
        return 0
    else
        print_status $RED "✗ pyuvm AND gate test failed (exit code: $exit_code)"
        print_status $YELLOW "Check /tmp/pyuvm_and_gate.log for details"
        cd "$PROJECT_ROOT"
        return 1
    fi
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --python-basics)
                RUN_PYTHON_BASICS=true
                shift
                ;;
            --decorators)
                RUN_DECORATORS=true
                shift
                ;;
            --async-await)
                RUN_ASYNC_AWAIT=true
                shift
                ;;
            --data-structures)
                RUN_DATA_STRUCTURES=true
                shift
                ;;
            --error-handling)
                RUN_ERROR_HANDLING=true
                shift
                ;;
            --all-python)
                RUN_PYTHON_BASICS=true
                RUN_DECORATORS=true
                RUN_ASYNC_AWAIT=true
                RUN_DATA_STRUCTURES=true
                RUN_ERROR_HANDLING=true
                shift
                ;;
            --skip-python)
                RUN_PYTHON_BASICS=false
                RUN_DECORATORS=false
                RUN_ASYNC_AWAIT=false
                RUN_DATA_STRUCTURES=false
                RUN_ERROR_HANDLING=false
                shift
                ;;
            --cocotb-tests)
                RUN_COCOTB_TESTS=true
                shift
                ;;
            --pyuvm-tests)
                RUN_PYUVM_TESTS=true
                shift
                ;;
            --all-tests)
                RUN_COCOTB_TESTS=true
                RUN_PYUVM_TESTS=true
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
            --sim)
                SIMULATOR="$2"
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
    print_header "Module 1: Python and Verification Basics"
    
    # Parse arguments
    parse_args "$@"
    
    # Check prerequisites
    check_prerequisites
    
    local errors=0
    
    # Run Python examples
    if [[ "$RUN_PYTHON_BASICS" == true ]] || [[ "$RUN_DECORATORS" == true ]] || \
       [[ "$RUN_ASYNC_AWAIT" == true ]] || [[ "$RUN_DATA_STRUCTURES" == true ]] || \
       [[ "$RUN_ERROR_HANDLING" == true ]]; then
        
        print_header "Running Python Examples"
        
        if [[ "$RUN_PYTHON_BASICS" == true ]]; then
            if ! run_python_example "$MODULE1_DIR/examples/python_basics/transaction.py" "Python Basics"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_DECORATORS" == true ]]; then
            if ! run_python_example "$MODULE1_DIR/examples/decorators/decorators_example.py" "Decorators"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_ASYNC_AWAIT" == true ]]; then
            if ! run_python_example "$MODULE1_DIR/examples/async_await/async_example.py" "Async/Await"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_DATA_STRUCTURES" == true ]]; then
            if ! run_python_example "$MODULE1_DIR/examples/data_structures/data_structures_example.py" "Data Structures"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_ERROR_HANDLING" == true ]]; then
            if ! run_python_example "$MODULE1_DIR/examples/error_handling/error_handling_example.py" "Error Handling"; then
                errors=$((errors + 1))
            fi
        fi
    fi
    
    # Run tests
    if [[ "$RUN_COCOTB_TESTS" == true ]]; then
        if ! run_cocotb_tests; then
            errors=$((errors + 1))
        fi
    fi
    
    if [[ "$RUN_PYUVM_TESTS" == true ]]; then
        if ! run_pyuvm_tests; then
            errors=$((errors + 1))
        fi
    fi
    
    # Summary
    print_header "Summary"
    
    if [[ $errors -eq 0 ]]; then
        print_status $GREEN "✓ All examples and tests completed successfully!"
        echo ""
        print_status $BLUE "Next steps:"
        echo "  1. Review the examples in module1/examples/"
        echo "  2. Try modifying the examples"
        echo "  3. Proceed to Module 2: cocotb Fundamentals"
    else
        print_status $RED "✗ Completed with $errors error(s)"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

