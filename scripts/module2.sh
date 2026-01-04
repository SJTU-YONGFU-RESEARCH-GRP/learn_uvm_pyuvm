#!/bin/bash

# Module 2: cocotb Fundamentals Orchestrator
# This script runs examples and tests for Module 2
# Usage: ./module2.sh [OPTIONS]

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
MODULE2_DIR="$PROJECT_ROOT/module2"
VENV_DIR="$PROJECT_ROOT/.venv"

# Options
RUN_SIGNAL_ACCESS=true
RUN_CLOCK_GENERATION=true
RUN_TRIGGERS=true
RUN_RESET_PATTERNS=true
RUN_COMMON_PATTERNS=true
RUN_COCOTB_TESTS=false
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

Module 2: cocotb Fundamentals
This script runs examples and tests for Module 2.

OPTIONS:
    Examples:
        --signal-access       Run signal access examples
        --clock-generation    Run clock generation examples
        --triggers            Run trigger usage examples
        --reset-patterns      Run reset pattern examples
        --common-patterns     Run common verification pattern examples
        --all-examples        Run all examples (default)
        --skip-examples       Skip all examples
    
    Tests:
        --cocotb-tests        Run cocotb tests
    
    Environment:
        --venv DIR            Virtual environment directory (default: .venv)
        --no-venv             Don't use virtual environment
        --sim SIMULATOR       Simulator to use (default: verilator)
    
    Other:
        --help, -h            Show this help message

EXAMPLES:
    # Run all examples
    $0
    
    # Run specific examples
    $0 --signal-access
    $0 --clock-generation
    $0 --triggers
    
    # Run tests
    $0 --cocotb-tests
    
    # Run everything
    $0 --all-examples --cocotb-tests

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
    
    # Check cocotb
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
    
    print_status $GREEN "Prerequisites check passed"
}

# Function to run cocotb example
run_cocotb_example() {
    local example_dir=$1
    local example_name=$2

    print_header "Running: $example_name"

    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi

    # Check if Makefile exists
    if [[ ! -f "$MODULE2_DIR/examples/$example_dir/Makefile" ]]; then
        print_status $RED "✗ Makefile not found for $example_name"
        return 1
    fi

    # Set library path for cocotb VPI libraries
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(cocotb-config --lib-dir)"

    # Run with cocotb using make
    cd "$MODULE2_DIR/examples/$example_dir"

    # Clean previous build to avoid path issues
    make clean > /dev/null 2>&1 || true

    print_status $BLUE "Running cocotb test for $example_name..."
    if make SIM="$SIMULATOR" 2>&1 | tee "/tmp/cocotb_${example_dir}.log"; then
        print_status $GREEN "✓ $example_name completed successfully"
        cd "$PROJECT_ROOT"
        return 0
    else
        print_status $RED "✗ $example_name failed"
        cd "$PROJECT_ROOT"
        return 1
    fi
}

# Function to run cocotb tests
run_cocotb_tests() {
    print_header "Running cocotb Tests"

    if [[ "$USE_VENV" == true ]] && [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    fi

    # Set library path for cocotb VPI libraries
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(cocotb-config --lib-dir)"

    cd "$MODULE2_DIR/tests/cocotb_tests"

    # Clean previous build to avoid path issues
    make clean > /dev/null 2>&1 || true

    local failed=0

    # Run simple register tests
    print_status $BLUE "Running simple register tests..."
    if make SIM="$SIMULATOR" TEST=test_simple_register 2>&1 | tee /tmp/cocotb_register.log; then
        print_status $GREEN "✓ Simple register tests passed"
    else
        print_status $RED "✗ Simple register tests failed"
        failed=$((failed + 1))
    fi

    # Run shift register tests
    print_status $BLUE "Running shift register tests..."
    if make SIM="$SIMULATOR" TEST=test_shift_register 2>&1 | tee /tmp/cocotb_shift_register.log; then
        print_status $GREEN "✓ Shift register tests passed"
    else
        print_status $RED "✗ Shift register tests failed"
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

# Function to parse command line arguments
parse_args() {
    # Default: run all examples if no specific option given
    local has_specific_option=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --signal-access)
                RUN_SIGNAL_ACCESS=true
                has_specific_option=true
                shift
                ;;
            --clock-generation)
                RUN_CLOCK_GENERATION=true
                has_specific_option=true
                shift
                ;;
            --triggers)
                RUN_TRIGGERS=true
                has_specific_option=true
                shift
                ;;
            --reset-patterns)
                RUN_RESET_PATTERNS=true
                has_specific_option=true
                shift
                ;;
            --common-patterns)
                RUN_COMMON_PATTERNS=true
                has_specific_option=true
                shift
                ;;
            --all-examples)
                RUN_SIGNAL_ACCESS=true
                RUN_CLOCK_GENERATION=true
                RUN_TRIGGERS=true
                RUN_RESET_PATTERNS=true
                RUN_COMMON_PATTERNS=true
                has_specific_option=true
                shift
                ;;
            --skip-examples)
                RUN_SIGNAL_ACCESS=false
                RUN_CLOCK_GENERATION=false
                RUN_TRIGGERS=false
                RUN_RESET_PATTERNS=false
                RUN_COMMON_PATTERNS=false
                shift
                ;;
            --cocotb-tests)
                RUN_COCOTB_TESTS=true
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
        RUN_SIGNAL_ACCESS=true
        RUN_CLOCK_GENERATION=true
        RUN_TRIGGERS=true
        RUN_RESET_PATTERNS=true
        RUN_COMMON_PATTERNS=true
    fi
}

# Main function
main() {
    print_header "Module 2: cocotb Fundamentals"
    
    # Parse arguments
    parse_args "$@"
    
    # Check prerequisites
    check_prerequisites
    
    local errors=0
    
    # Run examples (these are cocotb test files, run with make)
    if [[ "$RUN_SIGNAL_ACCESS" == true ]] || [[ "$RUN_CLOCK_GENERATION" == true ]] || \
       [[ "$RUN_TRIGGERS" == true ]] || [[ "$RUN_RESET_PATTERNS" == true ]] || \
       [[ "$RUN_COMMON_PATTERNS" == true ]]; then
        
        print_header "Running cocotb Examples"
        
        if [[ "$RUN_SIGNAL_ACCESS" == true ]]; then
            if ! run_cocotb_example "signal_access" "Signal Access"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_CLOCK_GENERATION" == true ]]; then
            if ! run_cocotb_example "clock_generation" "Clock Generation"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_TRIGGERS" == true ]]; then
            if ! run_cocotb_example "triggers" "Triggers"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_RESET_PATTERNS" == true ]]; then
            if ! run_cocotb_example "reset_patterns" "Reset Patterns"; then
                errors=$((errors + 1))
            fi
        fi
        
        if [[ "$RUN_COMMON_PATTERNS" == true ]]; then
            if ! run_cocotb_example "common_patterns" "Common Patterns"; then
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
    
    # Summary
    print_header "Summary"
    
    if [[ $errors -eq 0 ]]; then
        print_status $GREEN "✓ All examples and tests completed successfully!"
        echo ""
        print_status $BLUE "Next steps:"
        echo "  1. Review the examples in module2/examples/"
        echo "  2. Try modifying the examples"
        echo "  3. Proceed to Module 3: UVM Basics"
    else
        print_status $RED "✗ Completed with $errors error(s)"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

