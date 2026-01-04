# Module 6: Complex Testbenches

This directory contains all examples, exercises, and test cases for Module 6.

## Directory Structure

```
module6/
├── examples/              # pyuvm examples for each topic
│   ├── multi_agent/      # Multi-agent environment examples
│   ├── protocol/         # Protocol verification examples
│   ├── protocol_checkers/# Protocol checker examples
│   ├── scoreboards/      # Multi-channel scoreboard examples
│   └── architecture/     # Testbench architecture examples
├── dut/                   # Verilog Design Under Test modules
│   └── protocols/        # Protocol modules for testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module6.sh` script to run examples:

```bash
# Run all examples
./scripts/module6.sh

# Run specific examples
./scripts/module6.sh --multi-agent
./scripts/module6.sh --protocol
./scripts/module6.sh --protocol-checkers
./scripts/module6.sh --scoreboards
./scripts/module6.sh --architecture
./scripts/module6.sh --pyuvm-tests
```

## Topics Covered

1. **Multi-Agent Environments** - Multiple agent coordination
2. **Protocol Verification** - AXI4-Lite and custom protocols
3. **Protocol Checkers** - Protocol compliance checking
4. **Multi-Channel Scoreboards** - Advanced scoreboarding
5. **Testbench Architecture** - Layered and reusable patterns
6. **Debugging and Analysis** - Advanced debugging techniques
7. **Multi-Channel Verification** - Channel coordination
8. **Performance Verification** - Performance monitoring
9. **Error Injection** - Error injection and recovery
10. **Testbench Integration** - Component and system integration

