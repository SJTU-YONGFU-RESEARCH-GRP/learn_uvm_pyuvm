# Module 4: UVM Components

This directory contains all examples, exercises, and test cases for Module 4.

## Directory Structure

```
module4/
├── examples/              # pyuvm examples for each topic
│   ├── drivers/          # Driver implementation examples
│   ├── monitors/         # Monitor implementation examples
│   ├── sequencers/       # Sequencer and sequence examples
│   ├── tlm/              # TLM communication examples
│   ├── scoreboards/      # Scoreboard examples
│   ├── transactions/     # Transaction modeling examples
│   └── agents/           # Complete agent examples
├── dut/                   # Verilog Design Under Test modules
│   └── interfaces/       # Interface modules for testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module4.sh` script to run examples:

```bash
# Run all examples
./scripts/module4.sh

# Run specific examples
./scripts/module4.sh --drivers
./scripts/module4.sh --monitors
./scripts/module4.sh --sequencers
./scripts/module4.sh --tlm
./scripts/module4.sh --scoreboards
./scripts/module4.sh --transactions
./scripts/module4.sh --agents
./scripts/module4.sh --pyuvm-tests
```

## Topics Covered

1. **UVM Agent Architecture** - Active vs passive agents
2. **Driver Implementation** - Driving transactions to DUT
3. **Monitor Implementation** - Sampling DUT signals
4. **Sequencer and Sequences** - Sequence generation and execution
5. **TLM Communication** - Transaction-level modeling interfaces
6. **Scoreboard Implementation** - Result checking and comparison
7. **Transaction Modeling** - Transaction design and operations
8. **Complete Agent** - Full agent with all components
9. **Sequence Libraries** - Reusable sequence patterns
10. **Agent Integration** - Integrating agents into environments

