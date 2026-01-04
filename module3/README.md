# Module 3: UVM Basics

This directory contains all examples, exercises, and test cases for Module 3.

## Directory Structure

```
module3/
├── examples/              # pyuvm examples for each topic
│   ├── class_hierarchy/   # UVM class hierarchy examples
│   ├── phases/           # UVM phases examples
│   ├── reporting/        # UVM reporting examples
│   ├── configdb/         # ConfigDB examples
│   ├── factory/          # Factory pattern examples
│   └── objections/       # Objection mechanism examples
├── dut/                   # Verilog Design Under Test modules
│   └── simple_blocks/     # Simple blocks for UVM testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module3.sh` script to run examples:

```bash
# Run all examples
./scripts/module3.sh

# Run specific examples
./scripts/module3.sh --class-hierarchy
./scripts/module3.sh --phases
./scripts/module3.sh --reporting
./scripts/module3.sh --configdb
./scripts/module3.sh --factory
./scripts/module3.sh --objections
./scripts/module3.sh --pyuvm-tests
```

## Topics Covered

1. **UVM Introduction** - Understanding UVM methodology
2. **Class Hierarchy** - UVM base classes and components
3. **UVM Phases** - Build, run, and cleanup phases
4. **Reporting System** - UVM messaging and verbosity
5. **ConfigDB** - Configuration database
6. **Factory Pattern** - Object creation and overrides
7. **Test Classes** - Creating UVM tests
8. **Environment Structure** - Building UVM environments
9. **Objection Mechanism** - Controlling test execution
10. **Test Execution** - Running UVM tests

