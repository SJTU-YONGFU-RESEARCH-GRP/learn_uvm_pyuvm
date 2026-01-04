#!/bin/bash

# Module 8: UVM Miscellaneous Utilities Orchestrator
# This script runs examples and tests for Module 8
# Usage: ./module8.sh [OPTIONS]

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
MODULE8_DIR="$PROJECT_ROOT/module8"
VENV_DIR="$PROJECT_ROOT/.venv"

# Options
RUN_CLP=false
RUN_COMPARATORS=false
RUN_RECORDERS=false
RUN_POOLS=false
RUN_QUEUES=false
RUN_STRING_UTILS=false
RUN_MATH_UTILS=false
RUN_RANDOM_UTILS=false
RUN_INTEGRATION=false
RUN_PYUVM_TESTS=false
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

Module 8: UVM Miscellaneous Utilities
This script runs examples and tests for Module 8.

OPTIONS:
    Examples:
        --clp              Run Command Line Processor examples
        --comparators      Run Comparator examples
        --recorders        Run Recorder examples
        --pools            Run Pool examples
        --queues           Run Queue examples
        --string-utils     Run String utility examples
        --math-utils       Run Math utility examples
        --random-utils     Run Random utility examples
        --integration      Run Utility integration examples
        --all-examples     Run all examples (default)
        --skip-examples    Skip all examples
    
    Tests:
        --pyuvm-tests      Run pyuvm tests
    
    Environment:
        --venv DIR         Virtual environment directory (default: .venv)
        --no-venv          Don't use virtual environment
        --sim SIMULATOR    Simulator to use (default: verilator)
    
    Other:
        --help, -h         Show this help message

EXAMPLES:
    # Run all examples
    $0
    
    # Run specific examples
    $0 --clp
    $0 --comparators
    $0 --recorders
    $0 --pools
    $0 --queues
    $0 --string-utils
    $0 --math-utils
    $0 --random-utils
    $0 --integration
    
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

# Function to run Python example (syntax check)
run_python_example() {
    local example_file=$1
    local example_name=$2
    
    print_header "Running: $example_name"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    # Check syntax only (don't execute, as these are structural examples)
    if python3 -m py_compile "$example_file" 2>&1; then
        print_status $GREEN "✓ $example_name syntax check passed"
        print_status $YELLOW "Note: This is a structural example. Run with cocotb for full simulation."
        return 0
    else
        print_status $RED "✗ $example_name syntax check failed"
        return 1
    fi
}

# Function to run pyuvm tests
run_pyuvm_tests() {
    print_header "Running pyuvm Tests"
    
    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    cd "$MODULE8_DIR/tests/pyuvm_tests"
    
    print_status $BLUE "Running utilities test..."
    if make SIM="$SIMULATOR" TEST=test_utilities 2>&1 | tee /tmp/pyuvm_test.log; then
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
            --clp)
                RUN_CLP=true
                has_specific_option=true
                shift
                ;;
            --comparators)
                RUN_COMPARATORS=true
                has_specific_option=true
                shift
                ;;
            --recorders)
                RUN_RECORDERS=true
                has_specific_option=true
                shift
                ;;
            --pools)
                RUN_POOLS=true
                has_specific_option=true
                shift
                ;;
            --queues)
                RUN_QUEUES=true
                has_specific_option=true
                shift
                ;;
            --string-utils)
                RUN_STRING_UTILS=true
                has_specific_option=true
                shift
                ;;
            --math-utils)
                RUN_MATH_UTILS=true
                has_specific_option=true
                shift
                ;;
            --random-utils)
                RUN_RANDOM_UTILS=true
                has_specific_option=true
                shift
                ;;
            --integration)
                RUN_INTEGRATION=true
                has_specific_option=true
                shift
                ;;
            --all-examples)
                RUN_CLP=true
                RUN_COMPARATORS=true
                RUN_RECORDERS=true
                RUN_POOLS=true
                RUN_QUEUES=true
                RUN_STRING_UTILS=true
                RUN_MATH_UTILS=true
                RUN_RANDOM_UTILS=true
                RUN_INTEGRATION=true
                has_specific_option=true
                shift
                ;;
            --skip-examples)
                RUN_CLP=false
                RUN_COMPARATORS=false
                RUN_RECORDERS=false
                RUN_POOLS=false
                RUN_QUEUES=false
                RUN_STRING_UTILS=false
                RUN_MATH_UTILS=false
                RUN_RANDOM_UTILS=false
                RUN_INTEGRATION=false
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
        RUN_CLP=true
        RUN_COMPARATORS=true
        RUN_RECORDERS=true
        RUN_POOLS=true
        RUN_QUEUES=true
        RUN_STRING_UTILS=true
        RUN_MATH_UTILS=true
        RUN_RANDOM_UTILS=true
        RUN_INTEGRATION=true
    fi
}

# Main function
main() {
    print_header "Module 8: UVM Miscellaneous Utilities"
    
    # Parse arguments
    parse_args "$@"
    
    # Check prerequisites
    check_prerequisites
    
    local errors=0
    
    # Run examples
    if [[ "$RUN_CLP" == true ]] || [[ "$RUN_COMPARATORS" == true ]] || \
       [[ "$RUN_RECORDERS" == true ]] || [[ "$RUN_POOLS" == true ]] || \
       [[ "$RUN_QUEUES" == true ]] || [[ "$RUN_STRING_UTILS" == true ]] || \
       [[ "$RUN_MATH_UTILS" == true ]] || [[ "$RUN_RANDOM_UTILS" == true ]] || \
       [[ "$RUN_INTEGRATION" == true ]]; then
        
        print_header "UVM Utilities Examples"
        print_status $YELLOW "Note: Examples are pyuvm structural examples."
        print_status $YELLOW "They demonstrate UVM utility usage patterns."
        
        if [[ "$RUN_CLP" == true ]]; then
            cd "$MODULE8_DIR/examples/clp"
            if ! run_python_example "clp_example.py" "Command Line Processor"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_COMPARATORS" == true ]]; then
            cd "$MODULE8_DIR/examples/comparators"
            if ! run_python_example "comparator_example.py" "Comparators"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_RECORDERS" == true ]]; then
            cd "$MODULE8_DIR/examples/recorders"
            if ! run_python_example "recorder_example.py" "Recorders"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_POOLS" == true ]]; then
            cd "$MODULE8_DIR/examples/pools"
            if ! run_python_example "pool_example.py" "Pools"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_QUEUES" == true ]]; then
            cd "$MODULE8_DIR/examples/queues"
            if ! run_python_example "queue_example.py" "Queues"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_STRING_UTILS" == true ]]; then
            cd "$MODULE8_DIR/examples/string_utils"
            if ! run_python_example "string_utils_example.py" "String Utilities"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_MATH_UTILS" == true ]]; then
            cd "$MODULE8_DIR/examples/math_utils"
            if ! run_python_example "math_utils_example.py" "Math Utilities"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_RANDOM_UTILS" == true ]]; then
            cd "$MODULE8_DIR/examples/random_utils"
            if ! run_python_example "random_utils_example.py" "Random Utilities"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
        fi
        
        if [[ "$RUN_INTEGRATION" == true ]]; then
            cd "$MODULE8_DIR/examples/integration"
            if ! run_python_example "integration_example.py" "Utility Integration"; then
                errors=$((errors + 1))
            fi
            cd "$PROJECT_ROOT"
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
        print_status $BLUE "Congratulations! You have completed Module 8: UVM Miscellaneous Utilities"
        echo ""
        print_status $BLUE "You now have:"
        echo "  - Understanding of UVM utility classes"
        echo "  - Ability to use Command Line Processor"
        echo "  - Knowledge of comparators, recorders, pools, and queues"
        echo "  - Skills to use string, math, and random utilities"
        echo "  - Ability to integrate utilities in testbenches"
        echo ""
        print_status $BLUE "Next steps:"
        echo "  1. Review all examples in module8/examples/"
        echo "  2. Practice using utilities in your testbenches"
        echo "  3. Integrate utilities for better testbench performance"
        echo "  4. Continue learning and applying UVM concepts"
    else
        print_status $RED "✗ Completed with $errors error(s)"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

