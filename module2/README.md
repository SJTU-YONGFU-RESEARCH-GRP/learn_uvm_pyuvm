# Module 2: cocotb Fundamentals

This directory contains all examples, exercises, and test cases for Module 2.

## Directory Structure

```
module2/
├── examples/              # cocotb examples for each topic
│   ├── signal_access/     # Signal reading and writing
│   ├── clock_generation/  # Clock generation patterns
│   ├── triggers/         # Trigger usage examples
│   ├── reset_patterns/   # Reset sequences
│   └── common_patterns/  # Common verification patterns
├── dut/                   # Verilog Design Under Test modules
│   ├── registers/         # Register modules
│   ├── fifos/            # FIFO modules
│   └── state_machines/   # State machine modules
├── tests/                 # Testbenches
│   └── cocotb_tests/     # cocotb testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module2.sh` script to run examples:

```bash
# Run all examples
./scripts/module2.sh

# Run specific examples
./scripts/module2.sh --signal-access
./scripts/module2.sh --clock-generation
./scripts/module2.sh --triggers
./scripts/module2.sh --reset-patterns
./scripts/module2.sh --common-patterns
./scripts/module2.sh --cocotb-tests
```

## Topics Covered

1. **cocotb Architecture** - Understanding cocotb structure
2. **Simulator Integration** - Working with Verilator and other simulators
3. **Clock Generation** - Creating and managing clocks
4. **Signal Access** - Reading and writing DUT signals
5. **Triggers** - Using triggers for synchronization
6. **Test Structure** - Organizing cocotb tests
7. **Reset Patterns** - Implementing reset sequences
8. **Common Patterns** - Verification patterns and best practices
9. **Debugging** - Debugging cocotb testbenches
10. **Advanced Features** - Memory access, BFMs, optimization

