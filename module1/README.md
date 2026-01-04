# Module 1: Python and Verification Basics

This directory contains all examples, exercises, and test cases for Module 1.

## Directory Structure

```
module1/
├── examples/              # Python examples for each topic
│   ├── python_basics/     # Classes, inheritance, OOP
│   ├── decorators/        # Decorators and context managers
│   ├── async_await/       # Async/await patterns
│   ├── data_structures/   # Data structures for verification
│   └── error_handling/   # Exception handling and logging
├── dut/                   # Verilog Design Under Test modules
│   ├── simple_gates/      # Basic gates (AND, OR, etc.)
│   └── counters/         # Counter modules
├── tests/                 # Testbenches
│   ├── cocotb_tests/     # cocotb testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module1.sh` script to run examples:

```bash
# Run all examples
./scripts/module1.sh

# Run specific examples
./scripts/module1.sh --python-basics
./scripts/module1.sh --cocotb-tests
./scripts/module1.sh --pyuvm-tests
```

## Topics Covered

1. **Python Classes and Inheritance** - OOP for verification
2. **Decorators and Context Managers** - Python patterns
3. **Async/Await** - Simulation coroutines
4. **Verification Fundamentals** - Testbench concepts
5. **Testbench Architecture** - DUT, stimulus, checking
6. **Simulation Flow** - Time management
7. **Assertions** - Property checking
8. **Data Structures** - Collections for verification
9. **Error Handling** - Exceptions and logging

