#!/bin/bash

# Module 3: UVM Basics Orchestrator
# This script runs examples and tests for Module 3
# Usage: ./module3.sh [OPTIONS]

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
MODULE3_DIR="$PROJECT_ROOT/module3"
VENV_DIR="$PROJECT_ROOT/.venv"

# Options
RUN_CLASS_HIERARCHY=false
RUN_PHASES=false
RUN_REPORTING=false
RUN_CONFIGDB=false
RUN_FACTORY=false
RUN_OBJECTIONS=false
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

Module 3: UVM Basics
This script runs examples and tests for Module 3.

OPTIONS:
    Examples:
        --class-hierarchy    Run UVM class hierarchy examples
        --phases             Run UVM phases examples
        --reporting          Run UVM reporting examples
        --configdb           Run ConfigDB examples
        --factory            Run factory pattern examples
        --objections         Run objection mechanism examples
        --all-examples       Run all examples (default)
        --skip-examples      Skip all examples
    
    Tests:
        --pyuvm-tests        Run pyuvm tests
    
    Environment:
        --venv DIR           Virtual environment directory (default: .venv)
        --no-venv            Don't use virtual environment
        --sim SIMULATOR      Simulator to use (default: verilator)
    
    Other:
        --help, -h           Show this help message

EXAMPLES:
    # Run all examples
    $0
    
    # Run specific examples
    $0 --class-hierarchy
    $0 --phases
    $0 --reporting
    
    # Run tests
    $0 --pyuvm-tests
    
    # Run everything
    $0 --all-examples --pyuvm-tests

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
    
    # Check pyuvm
    if ! python3 -c "import pyuvm" 2>/dev/null; then
        print_status $RED "Error: pyuvm not found. Please install it first."
        print_status $YELLOW "Run: ./scripts/module0.sh or ./scripts/install_pyuvm.sh"
        exit 1
    fi
    
    # Check cocotb (needed for running tests)
    if [[ "$RUN_PYUVM_TESTS" == true ]]; then
        if ! python3 -c "import cocotb" 2>/dev/null; then
            print_status $RED "Error: cocotb not found. Please install it first."
            print_status $YELLOW "Run: ./scripts/module0.sh or ./scripts/install_cocotb.sh"
            exit 1
        fi
        
        # Check simulator
        if [[ "$SIMULATOR" == "verilator" ]]; then
            if ! command -v verilator &> /dev/null; then
                print_status $RED "Error: verilator not found. Please install it first."
                print_status $YELLOW "Run: ./scripts/module0.sh or ./scripts/install_verilator.sh"
                exit 1
            fi
        fi
    fi
    
    print_status $GREEN "Prerequisites check passed"
}

# Function to run Python example (run with cocotb)
run_python_example() {
    local example_dir=$1
    local example_name=$2
    
    print_header "Running: $example_name"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    # Check if Makefile exists
    if [[ ! -f "$MODULE3_DIR/examples/$example_dir/Makefile" ]]; then
        print_status $RED "✗ Makefile not found for $example_name"
        return 1
    fi
    
    # Run with cocotb using make
    cd "$MODULE3_DIR/examples/$example_dir"
    
    print_status $BLUE "Running pyuvm test for $example_name..."
    if make SIM="$SIMULATOR" 2>&1 | tee "/tmp/pyuvm_${example_dir}.log"; then
        print_status $GREEN "✓ $example_name completed successfully"
        cd "$PROJECT_ROOT"
        return 0
    else
        print_status $RED "✗ $example_name failed"
        cd "$PROJECT_ROOT"
        return 1
    fi
}

# Function to run pyuvm tests
run_pyuvm_tests() {
    print_header "Running pyuvm Tests"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    cd "$MODULE3_DIR/tests/pyuvm_tests"
    
    print_status $BLUE "Running simple UVM test..."
    if make SIM="$SIMULATOR" TEST=test_simple_uvm 2>&1 | tee /tmp/pyuvm_test.log; then
        print_status $GREEN "✓ pyuvm test passed"
        cd "$PROJECT_ROOT"
        return 0
    else
        print_status $RED "✗ pyuvm test failed"
        cd "$PROJECT_ROOT"
        return 1
    fi
}

# Function to parse command line arguments
parse_args() {
    # Default: run all examples if no specific option given
    local has_specific_option=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --class-hierarchy)
                RUN_CLASS_HIERARCHY=true
                has_specific_option=true
                shift
                ;;
            --phases)
                RUN_PHASES=true
                has_specific_option=true
                shift
                ;;
            --reporting)
                RUN_REPORTING=true
                has_specific_option=true
                shift
                ;;
            --configdb)
                RUN_CONFIGDB=true
                has_specific_option=true
                shift
                ;;
            --factory)
                RUN_FACTORY=true
                has_specific_option=true
                shift
                ;;
            --objections)
                RUN_OBJECTIONS=true
                has_specific_option=true
                shift
                ;;
            --all-examples)
                RUN_CLASS_HIERARCHY=true
                RUN_PHASES=true
                RUN_REPORTING=true
                RUN_CONFIGDB=true
                RUN_FACTORY=true
                RUN_OBJECTIONS=true
                has_specific_option=true
                shift
                ;;
            --skip-examples)
                RUN_CLASS_HIERARCHY=false
                RUN_PHASES=false
                RUN_REPORTING=false
                RUN_CONFIGDB=false
                RUN_FACTORY=false
                RUN_OBJECTIONS=false
                shift
                ;;
            --pyuvm-tests)
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
    
    # If no specific option, run all examples
    if [[ "$has_specific_option" == false ]]; then
        RUN_CLASS_HIERARCHY=true
        RUN_PHASES=true
        RUN_REPORTING=true
        RUN_CONFIGDB=true
        RUN_FACTORY=true
        RUN_OBJECTIONS=true
    fi
}

# Main function
main() {
    print_header "Module 3: UVM Basics"
    
    # Parse arguments
    parse_args "$@"
    
    # Check prerequisites
    check_prerequisites
    
    local errors=0
    
    # Run examples
    if [[ "$RUN_CLASS_HIERARCHY" == true ]] || [[ "$RUN_PHASES" == true ]] || \
       [[ "$RUN_REPORTING" == true ]] || [[ "$RUN_CONFIGDB" == true ]] || \
       [[ "$RUN_FACTORY" == true ]] || [[ "$RUN_OBJECTIONS" == true ]]; then
        
        print_header "Running UVM Examples"
        
        if [[ "$RUN_CLASS_HIERARCHY" == true ]]; then
            if ! run_python_example "class_hierarchy" "Class Hierarchy"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_PHASES" == true ]]; then
            if ! run_python_example "phases" "UVM Phases"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_REPORTING" == true ]]; then
            if ! run_python_example "reporting" "UVM Reporting"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_CONFIGDB" == true ]]; then
            if ! run_python_example "configdb" "ConfigDB"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_FACTORY" == true ]]; then
            if ! run_python_example "factory" "Factory Pattern"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_OBJECTIONS" == true ]]; then
            if ! run_python_example "objections" "Objections"; then
                errors=$((errors + 1))
            fi
        fi
    fi
    
    # Run tests
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
        echo "  1. Review the examples in module3/examples/"
        echo "  2. Study the UVM class hierarchy and phases"
        echo "  3. Try modifying the examples"
        echo "  4. Proceed to Module 4: UVM Components"
    else
        print_status $RED "✗ Completed with $errors error(s)"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

