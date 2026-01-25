# Module 4: UVM Components

**Goal**: Build complete UVM agents with driver, monitor, and sequencer

## Overview

This module covers the core UVM components used to build verification environments. You'll learn how to create agents, drivers, monitors, sequencers, and sequences to build complete verification environments.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module4/` directory:

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
└── README.md             # Module 4 documentation
```

### Quick Start

**Run all examples using the orchestrator script:**
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

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run pyuvm tests
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent

# Examples are pyuvm structural examples
# They can be imported and used in your testbenches
```

## Topics Covered

### 1. UVM Agent Architecture

- **Agent Overview**
  - What is an agent?
  - Agent components
  - Agent purpose
  - Agent types

- **Active vs Passive Agents**
  - Active agents (driver + sequencer + monitor)
  - Passive agents (monitor only)
  - When to use each
  - Agent configuration

- **Agent Structure**
  - Driver component
  - Monitor component
  - Sequencer component
  - Agent container

### 2. UVM Driver Implementation

- **Driver Overview**
  - Driver purpose
  - Driver responsibilities
  - Driver interface
  - Driver lifecycle

- **Driver Implementation**
  - Inheriting from `uvm_driver`
  - `run_phase()` implementation
  - Transaction reception
  - Signal driving

- **Driver-Sequencer Communication**
  - `seq_item_port` interface
  - `get_next_item()`
  - `item_done()`
  - Transaction flow

- **Signal-Level Driving**
  - DUT signal access
  - Signal value assignment
  - Timing control
  - Protocol implementation

### 3. UVM Monitor Implementation

- **Monitor Overview**
  - Monitor purpose
  - Monitor responsibilities
  - Monitor types
  - Monitor lifecycle

- **Monitor Implementation**
  - Inheriting from `uvm_monitor`
  - `run_phase()` implementation
  - Signal sampling
  - Transaction creation

- **Analysis Ports**
  - Analysis port purpose
  - Creating analysis ports
  - Writing to analysis ports
  - Analysis port connections

- **Transaction Creation**
  - Sampling signals
  - Creating transaction objects
  - Populating transaction fields
  - Broadcasting transactions

### 4. UVM Sequencer and Sequences

- **Sequencer Overview**
  - Sequencer purpose
  - Sequencer responsibilities
  - Sequencer types
  - Sequencer lifecycle

- **Sequencer Implementation**
  - Inheriting from `uvm_sequencer`
  - Default sequencer usage
  - Custom sequencer features
  - Sequencer configuration

- **Sequence Items**
  - `uvm_sequence_item` base class
  - Transaction definition
  - Transaction fields
  - Transaction methods

- **Sequence Basics**
  - `uvm_sequence` base class
  - `body()` method
  - Sequence execution
  - Sequence lifecycle

- **Sequence Operations**
  - `start_item()`
  - `finish_item()`
  - `wait_for_grant()`
  - Transaction creation

### 5. TLM (Transaction-Level Modeling) - Complete Coverage

- **TLM Overview**
  - What is TLM?
  - TLM benefits
  - TLM abstraction levels
  - TLM communication patterns

- **TLM Interface Types**
  - `put` interface - Unidirectional blocking put
  - `get` interface - Unidirectional blocking get
  - `peek` interface - Unidirectional non-blocking peek
  - `transport` interface - Bidirectional blocking transport
  - Interface characteristics and use cases

- **TLM Port Types**
  - `uvm_put_port` - Put port
  - `uvm_get_port` - Get port
  - `uvm_peek_port` - Peek port
  - `uvm_transport_port` - Transport port
  - Port vs export vs implementation

- **TLM Export Types**
  - `uvm_put_export` - Put export
  - `uvm_get_export` - Get export
  - `uvm_peek_export` - Peek export
  - `uvm_transport_export` - Transport export
  - Export usage patterns

- **TLM Implementation Types**
  - `uvm_put_imp` - Put implementation
  - `uvm_get_imp` - Get implementation
  - `uvm_peek_imp` - Peek implementation
  - `uvm_transport_imp` - Transport implementation
  - Implementation requirements

- **Analysis Ports and Exports (Special TLM Type)**
  - Analysis port concept
  - Publisher-subscriber pattern
  - Broadcast communication
  - One-to-many connections
  - `uvm_analysis_port` - Analysis port
  - `uvm_analysis_export` - Analysis export
  - `uvm_analysis_imp` - Analysis implementation
  - Connection patterns

- **TLM FIFOs**
  - `uvm_tlm_fifo` - TLM FIFO
  - FIFO purpose and usage
  - FIFO capacity and blocking behavior
  - FIFO connection patterns
  - When to use FIFOs

- **TLM Connection Patterns**
  - Direct connections (port to export)
  - FIFO connections (port to FIFO to export)
  - Multi-port connections
  - Hierarchical connections
  - Connection best practices

- **TLM Usage Patterns**
  - Producer-consumer pattern
  - Request-response pattern
  - Broadcast pattern
  - Pipeline pattern
  - TLM vs analysis ports

- **TLM Implementation Examples**
  - Using put/get interfaces
  - Using transport interface
  - Using TLM FIFOs
  - Combining TLM types
  - TLM debugging

### 6. Scoreboard Implementation

- **Scoreboard Overview**
  - Scoreboard purpose
  - Scoreboard types
  - Scoreboard responsibilities
  - Scoreboard lifecycle

- **Scoreboard Implementation**
  - Inheriting from `uvm_component`
  - Analysis port connections
  - Transaction storage
  - Comparison logic

- **Scoreboard Patterns**
  - Reference model comparison
  - Expected vs actual
  - Transaction matching
  - Error reporting

- **Advanced Scoreboards**
  - Multi-channel scoreboards
  - Time-based matching
  - Complex comparison logic
  - Performance optimization

### 7. Transaction-Level Modeling

- **Transaction Concepts**
  - What are transactions?
  - Transaction abstraction
  - Transaction fields
  - Transaction methods

- **Transaction Design**
  - Transaction class structure
  - Field definition
  - Constraint definition
  - Method implementation

- **Transaction Operations**
  - Transaction creation
  - Transaction copying
  - Transaction comparison
  - Transaction conversion

### 8. Complete Agent Example

- **Agent Structure**
  - Agent class definition
  - Component instantiation
  - Component connections
  - Agent configuration

- **Agent Build Phase**
  - Component creation
  - Configuration application
  - Active/passive selection

- **Agent Connect Phase**
  - Driver-sequencer connection
  - Monitor analysis port
  - External connections

### 9. Sequence Libraries

- **Sequence Organization**
  - Base sequences
  - Derived sequences
  - Sequence libraries
  - Sequence reuse

- **Common Sequences**
  - Simple sequences
  - Random sequences
  - Constrained sequences
  - Layered sequences

### 10. Agent Integration

- **Environment Integration**
  - Adding agents to environment
  - Agent configuration
  - Agent connections
  - Agent coordination

- **Test Integration**
  - Agent instantiation
  - Sequence execution
  - Test coordination
  - Result checking

## Learning Outcomes

By the end of this module, you should be able to:

- Understand agent architecture
- Implement UVM drivers
- Implement UVM monitors
- Implement sequencers and sequences
- Use analysis ports effectively
- Implement scoreboards
- Design transaction models
- Build complete agents
- Integrate agents into environments
- Execute sequences in tests

## Test Cases

### Test Case 4.1: Simple Driver
**Objective**: Implement basic driver

**Topics**:
- Driver class
- Transaction reception
- Signal driving

#### Example 4.1: Driver Implementation (`module4/examples/drivers/driver_example.py`)

**What it demonstrates:**
- **Driver Class Structure**: Inheriting from `uvm_driver`
- **Sequencer Port**: Creating `seq_item_port` for transaction reception
- **Transaction Reception**: Using `get_next_item()` to receive transactions
- **Signal Driving**: Driving DUT signals based on transaction fields
- **Protocol Implementation**: Demonstrating protocol-specific signal driving
- **Driver-Sequencer Communication**: `item_done()` to signal completion

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --drivers

# Or directly (syntax check)
cd module4/examples/drivers
python3 -c "import pyuvm; exec(open('driver_example.py').read())"
```

**Expected Output:**
```
============================================================
Driver Example Test
============================================================
[driver] Building driver
[driver] Connecting driver
[driver] Starting driver run_phase
[driver] Received transaction: data=0x00, addr=0x0000
[driver] Driving transaction: data=0x00, addr=0x0000
[driver] Signals driven: data=0x00, addr=0x0000
[driver] Transaction completed
```

**Key Concepts:**
- **`uvm_driver`**: Base class for all drivers
- **`seq_item_port`**: Port for receiving transactions from sequencer
- **`get_next_item()`**: Get next transaction from sequencer
- **`item_done()`**: Signal transaction completion to sequencer
- **`run_phase()`**: Main driver loop
- **Protocol Implementation**: Drive signals according to protocol timing

### Test Case 4.2: Simple Monitor
**Objective**: Implement basic monitor

**Topics**:
- Monitor class
- Signal sampling
- Analysis ports

#### Example 4.2: Monitor Implementation (`module4/examples/monitors/monitor_example.py`)

**What it demonstrates:**
- **Monitor Class Structure**: Inheriting from `uvm_monitor`
- **Analysis Port**: Creating `uvm_analysis_port` for broadcasting transactions
- **Signal Sampling**: Sampling DUT signals and creating transactions
- **Transaction Creation**: Creating transaction objects from sampled signals
- **Analysis Port Broadcasting**: Using `write()` to broadcast transactions
- **Protocol-Aware Sampling**: Protocol-specific signal sampling patterns

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --monitors

# Or directly
cd module4/examples/monitors
python3 -c "import pyuvm; exec(open('monitor_example.py').read())"
```

**Expected Output:**
```
============================================================
Monitor Example Test
============================================================
[monitor] Building monitor
[monitor] Starting monitor run_phase
[monitor] Sampled transaction: data=0xAB, addr=0x1000, time=0ns
[monitor] Broadcasted transaction via analysis port
```

**Key Concepts:**
- **`uvm_monitor`**: Base class for all monitors
- **`uvm_analysis_port`**: Port for broadcasting transactions
- **`write()`**: Method to broadcast transactions via analysis port
- **Signal Sampling**: Wait for valid data, sample signals, create transactions
- **Transaction Broadcasting**: One-to-many communication pattern
- **Protocol Monitoring**: Monitor protocol-specific events

### Test Case 4.3: Simple Sequencer and Sequence
**Objective**: Implement sequencer and sequence

**Topics**:
- Sequencer class
- Sequence items
- Sequence execution

#### Example 4.3: Sequencer and Sequences (`module4/examples/sequencers/sequencer_example.py`)

**What it demonstrates:**
- **Sequence Class**: Inheriting from `uvm_sequence`
- **Sequence Body**: Implementing `body()` method for sequence execution
- **Transaction Creation**: Creating sequence items within sequences
- **Sequence Operations**: `start_item()` and `finish_item()` for transaction flow
- **Random Sequences**: Generating random transactions
- **Layered Sequences**: Calling other sequences from within a sequence
- **Sequence Execution**: Starting sequences on sequencers

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --sequencers

# Or directly
cd module4/examples/sequencers
python3 -c "import pyuvm; exec(open('sequencer_example.py').read())"
```

**Expected Output:**
```
============================================================
Sequencer Example Test
============================================================
Starting SimpleSequence
[seq1] Starting sequence body
[seq1] Creating transaction 0: data=0x00, addr=0x0000
[seq1] Started item: data=0x00, addr=0x0000
[seq1] Finished item: data=0x00, addr=0x0000
...
[seq1] Sequence body completed
```

**Key Concepts:**
- **`uvm_sequence`**: Base class for all sequences
- **`body()`**: Main sequence execution method
- **`start_item()`**: Request transaction from sequencer
- **`finish_item()`**: Send transaction to driver
- **`uvm_sequencer`**: Manages sequence execution
- **Sequence Layering**: Sequences can call other sequences
- **Random Generation**: Generate random transactions with constraints

### Test Case 4.4: Complete Agent
**Objective**: Build complete agent

**Topics**:
- Agent structure
- Component integration
- Connections

#### Example 4.4: Complete Agent (`module4/examples/agents/agent_example.py`)

**What it demonstrates:**
- **Agent Structure**: Complete agent with driver, monitor, sequencer
- **Active vs Passive**: Agent configuration for active/passive modes
- **Component Integration**: Building agent from components
- **Component Connections**: Connecting driver to sequencer
- **Agent Configuration**: Using ConfigDB for agent configuration
- **Environment Integration**: Integrating agent into environment

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --agents

# Or directly
cd module4/examples/agents
python3 -c "import pyuvm; exec(open('agent_example.py').read())"
```

**Expected Output:**
```
============================================================
Complete Agent Example Test
============================================================
[agent] Building complete agent
[agent] Agent mode: ACTIVE
[agent] Created driver and sequencer
[driver] Building driver
[monitor] Building monitor
[agent] Connecting agent
[agent] Connected driver to sequencer
```

**Key Concepts:**
- **`uvm_agent`**: Container for driver, monitor, sequencer
- **Active Agent**: Contains driver, sequencer, and monitor
- **Passive Agent**: Contains only monitor
- **Component Integration**: Agent builds and connects all components
- **ConfigDB**: Configure agent mode (active/passive)
- **Environment Integration**: Agent connects to environment components

### Test Case 4.5: Scoreboard
**Objective**: Implement scoreboard

**Topics**:
- Scoreboard class
- Analysis connections
- Comparison logic

#### Example 4.5: Scoreboard Implementation (`module4/examples/scoreboards/scoreboard_example.py`)

**What it demonstrates:**
- **Scoreboard Class**: Inheriting from `uvm_scoreboard`
- **Analysis Export**: Creating `uvm_analysis_export` and `uvm_analysis_imp`
- **Transaction Reception**: Implementing `write()` method to receive transactions
- **Comparison Logic**: Comparing expected vs actual transactions
- **Reference Model**: Using reference model for expected value calculation
- **Error Reporting**: Reporting mismatches and statistics

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --scoreboards

# Or directly
cd module4/examples/scoreboards
python3 -c "import pyuvm; exec(open('scoreboard_example.py').read())"
```

**Expected Output:**
```
============================================================
Scoreboard Example Test
============================================================
[scoreboard] Building scoreboard
[scoreboard] Received transaction: data=0x00, expected=0x00, actual=0x00
[scoreboard] Match: expected=0x00, actual=0x00
[scoreboard] Mismatch: expected=0x20, actual=0xFF
============================================================
[scoreboard] Scoreboard Check
  Total expected: 0
  Total actual: 5
  Mismatches: 1
```

**Key Concepts:**
- **`uvm_scoreboard`**: Base class for scoreboards
- **`uvm_analysis_export`**: Export for receiving transactions
- **`uvm_analysis_imp`**: Implementation of analysis interface
- **`write()`**: Method called when transaction is received
- **Comparison Logic**: Compare expected vs actual values
- **Reference Model**: Calculate expected values using reference model
- **Error Reporting**: Report mismatches in check_phase

#### Example 4.6: TLM Communication (`module4/examples/tlm/tlm_example.py`)

**What it demonstrates:**
- **TLM Put Interface**: Producer-consumer pattern with put port/export
- **TLM Get Interface**: Producer-consumer pattern with get port/export
- **TLM Transport Interface**: Request-response pattern
- **TLM FIFO**: Using `uvm_tlm_fifo` for buffering
- **TLM Connections**: Connecting ports, exports, and implementations
- **TLM Patterns**: Different TLM communication patterns

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --tlm

# Or directly
cd module4/examples/tlm
python3 -c "import pyuvm; exec(open('tlm_example.py').read())"
```

**Key Concepts:**
- **`uvm_put_port`**: Port for sending transactions
- **`uvm_put_export`**: Export for receiving transactions
- **`uvm_put_imp`**: Implementation of put interface
- **`uvm_get_port`**: Port for receiving transactions
- **`uvm_transport_port`**: Port for request-response
- **`uvm_tlm_fifo`**: FIFO for buffering transactions
- **TLM Patterns**: Producer-consumer, request-response, broadcast

#### Example 4.7: Transaction Modeling (`module4/examples/transactions/transaction_example.py`)

**What it demonstrates:**
- **Transaction Design**: Base and extended transaction classes
- **Transaction Methods**: `copy()`, `__eq__()`, `__str__()`
- **Constrained Transactions**: Randomization with constraints
- **Transaction Packing**: Pack/unpack for serialization
- **Transaction Comparison**: Equality and comparison methods

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --transactions

# Or directly
cd module4/examples/transactions
python3 -c "import pyuvm; exec(open('transaction_example.py').read())"
```

**Key Concepts:**
- **`uvm_sequence_item`**: Base class for all transactions
- **Transaction Fields**: Define transaction data fields
- **Transaction Methods**: Implement useful methods (copy, compare, convert)
- **Constraints**: Define randomization constraints
- **Serialization**: Pack/unpack for communication

#### Test: Complete Agent Test (`module4/tests/pyuvm_tests/test_complete_agent.py`)

**What it demonstrates:**
- Complete UVM testbench with all components
- Driver, monitor, sequencer, scoreboard integration
- Sequence execution
- Analysis port connections
- Full test flow

**Execution:**
```bash
# Using orchestrator script
./scripts/module4.sh --pyuvm-tests

# Or manually
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent
```

**Test Structure:**
- `InterfaceTransaction`: Transaction for interface test
- `InterfaceSequence`: Generates test vectors
- `InterfaceDriver`: Drives transactions to DUT
- `InterfaceMonitor`: Monitors DUT outputs
- `InterfaceScoreboard`: Checks results
- `InterfaceAgent`: Contains driver, monitor, sequencer
- `InterfaceEnv`: Contains agent and scoreboard
- `CompleteAgentTest`: Top-level test class

### Design Under Test (DUT) Modules

#### Simple Interface (`module4/dut/interfaces/simple_interface.v`)
- **Purpose**: Simple interface with valid/ready handshaking
- **Used in**: Complete agent test
- **Features**: Clocked operation, reset, data/address buses, result output

## Exercises

1. **Driver Implementation**
   - Create driver class
   - Implement signal driving
   - Handle transactions
   - **Location**: Extend `module4/examples/drivers/driver_example.py`
   - **Hint**: Add protocol-specific signal driving with timing

2. **Monitor Implementation**
   - Create monitor class
   - Sample signals
   - Broadcast transactions
   - **Location**: Extend `module4/examples/monitors/monitor_example.py`
   - **Hint**: Add protocol-aware signal sampling

3. **Sequence Creation**
   - Create sequence items
   - Create sequences
   - Execute sequences
   - **Location**: Extend `module4/examples/sequencers/sequencer_example.py`
   - **Hint**: Create constrained random sequences

4. **Agent Building**
   - Build complete agent
   - Integrate components
   - Test agent
   - **Location**: Extend `module4/examples/agents/agent_example.py`
   - **Hint**: Add configuration for active/passive modes

5. **Scoreboard Implementation**
   - Create scoreboard
   - Connect analysis ports
   - Implement checking
   - **Location**: Extend `module4/examples/scoreboards/scoreboard_example.py`
   - **Hint**: Add reference model for expected value calculation

## Assessment

- [ ] Understands agent architecture
- [ ] Can implement drivers
- [ ] Can implement monitors
- [ ] Can implement sequencers
- [ ] Can create sequences
- [ ] Can use analysis ports
- [ ] Can implement scoreboards
- [ ] Can build complete agents
- [ ] Can integrate agents
- [ ] Can execute sequences

## Next Steps

After completing this module, proceed to [Module 5: Advanced UVM Concepts](MODULE5.md) to learn advanced UVM features.

## Additional Resources

- **pyuvm Documentation**: https://pyuvm.readthedocs.io/
- **UVM 1.2 User's Guide**: Accellera Systems Initiative
- **The UVM Primer**: Ray Salemi
- **pyuvm Examples**: https://github.com/pyuvm/pyuvm/tree/main/examples

## Troubleshooting

### Common Issues

**Issue: "pyuvm not found" error**
```bash
# Solution: Install pyuvm
./scripts/install_pyuvm.sh --pip --venv .venv
# Or
./scripts/module0.sh
```

**Issue: Driver not receiving transactions**
```bash
# Solution: Check driver-sequencer connection
# Ensure: driver.seq_item_port.connect(sequencer.seq_item_export)
# Check sequence is started on correct sequencer
```

**Issue: Monitor not broadcasting transactions**
```bash
# Solution: Check analysis port connection
# Ensure: monitor.ap.connect(scoreboard.ap)
# Verify write() method is implemented in scoreboard
```

**Issue: Sequence not executing**
```bash
# Solution: Check sequence is started on sequencer
# Ensure: await seq.start(sequencer)
# Verify sequencer is connected to driver
```

**Issue: Scoreboard not receiving transactions**
```bash
# Solution: Check analysis port connections
# Ensure: monitor.ap.connect(scoreboard.ap)
# Verify scoreboard has uvm_analysis_imp with write() method
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module4/README.md` for directory structure
- Run examples individually to understand each component
- Study driver-sequencer communication in `driver_example.py`
- Review analysis port usage in `monitor_example.py` and `scoreboard_example.py`
- Check pyuvm documentation for TLM interface details

### Summary of Examples and Tests

**Examples (pyuvm structural examples in `module4/examples/`):**
1. **Example 4.1: Driver Implementation** (`drivers/`) - Driver class and signal driving
2. **Example 4.2: Monitor Implementation** (`monitors/`) - Monitor class and analysis ports
3. **Example 4.3: Sequencer and Sequences** (`sequencers/`) - Sequence execution
4. **Example 4.4: Complete Agent** (`agents/`) - Full agent with all components
5. **Example 4.5: Scoreboard Implementation** (`scoreboards/`) - Scoreboard and comparison
6. **Example 4.6: TLM Communication** (`tlm/`) - TLM interfaces and patterns
7. **Example 4.7: Transaction Modeling** (`transactions/`) - Transaction design

**Testbenches (runnable tests in `module4/tests/pyuvm_tests/`):**
1. **Complete Agent Test** (`test_complete_agent.py`) - Full testbench with all components

**DUT Modules (in `module4/dut/`):**
1. **Simple Interface** (`interfaces/simple_interface.v`) - Interface for agent testing

**Coverage:**
- ✅ Driver implementation and signal driving
- ✅ Monitor implementation and analysis ports
- ✅ Sequencer and sequence execution
- ✅ Complete agent structure
- ✅ Scoreboard implementation
- ✅ TLM communication patterns
- ✅ Transaction modeling
- ✅ Full testbench integration

