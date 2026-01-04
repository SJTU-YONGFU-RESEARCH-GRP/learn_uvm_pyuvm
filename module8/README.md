# Module 8: UVM Miscellaneous Utilities

This directory contains all examples, exercises, and test cases for Module 8.

## Directory Structure

```
module8/
├── examples/              # pyuvm utility examples
│   ├── clp/              # Command Line Processor examples
│   ├── comparators/      # Comparator examples
│   ├── recorders/        # Recorder examples
│   ├── pools/            # Pool examples
│   ├── queues/           # Queue examples
│   ├── string_utils/     # String utility examples
│   ├── math_utils/       # Math utility examples
│   ├── random_utils/     # Random utility examples
│   └── integration/      # Utility integration examples
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module8.sh` script to run examples:

```bash
# Run all examples
./scripts/module8.sh

# Run specific examples
./scripts/module8.sh --clp
./scripts/module8.sh --comparators
./scripts/module8.sh --recorders
./scripts/module8.sh --pools
./scripts/module8.sh --queues
./scripts/module8.sh --string-utils
./scripts/module8.sh --math-utils
./scripts/module8.sh --random-utils
./scripts/module8.sh --integration
./scripts/module8.sh --pyuvm-tests
```

## Topics Covered

1. **Command Line Processor** - Parse and use command-line arguments
2. **Comparators** - Compare transactions in scoreboards
3. **Recorders** - Record transactions for analysis
4. **Pools** - Object pooling for performance
5. **Queues** - Queue data structures
6. **String Utilities** - String manipulation utilities
7. **Math Utilities** - Mathematical operations
8. **Random Utilities** - Random number generation
9. **Utility Integration** - Using multiple utilities together

