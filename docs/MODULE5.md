# Module 5: Advanced UVM Concepts

**Goal**: Master sequences, coverage, configuration, and virtual sequences

## Overview

This module covers advanced UVM concepts including virtual sequences, coverage models, complex configuration, callbacks, and advanced register model usage. These concepts are essential for building sophisticated verification environments.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module5/` directory:

```
module5/
├── examples/              # pyuvm examples for each topic
│   ├── virtual_sequences/ # Virtual sequence examples
│   ├── coverage/         # Coverage model examples
│   ├── configuration/    # Configuration object examples
│   ├── callbacks/        # Callback examples
│   └── register_model/   # Register model examples
├── dut/                   # Verilog Design Under Test modules
│   └── advanced/          # Advanced modules for testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── README.md             # Module 5 documentation
```

### Quick Start

**Run all examples using the orchestrator script:**
```bash
# Run all examples
./scripts/module5.sh

# Run specific examples
./scripts/module5.sh --virtual-sequences
./scripts/module5.sh --coverage
./scripts/module5.sh --configuration
./scripts/module5.sh --callbacks
./scripts/module5.sh --register-model
./scripts/module5.sh --pyuvm-tests
```

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run pyuvm tests
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm

# Examples are pyuvm structural examples
# They can be imported and used in your testbenches
```

## Topics Covered

### 1. Advanced Sequences

- **Virtual Sequences**
  - What are virtual sequences?
  - Virtual sequence purpose
  - Multiple sequencer coordination
  - Virtual sequence implementation

- **Sequence Libraries**
  - Base sequence classes
  - Derived sequences
  - Sequence reuse patterns
  - Sequence organization

- **Sequence Arbitration**
  - Sequencer arbitration
  - Priority mechanisms
  - Lock and grab
  - Sequence coordination

- **Layered Sequences**
  - High-level sequences
  - Low-level sequences
  - Sequence composition
  - Protocol layering

### 2. UVM Coverage Models

- **Coverage Overview**
  - What is coverage?
  - Coverage types
  - Coverage goals
  - Coverage metrics

- **Functional Coverage**
  - Coverage models
  - Coverage groups
  - Coverpoints
  - Coverage bins

- **Coverage Implementation**
  - Coverage class structure
  - Coverage sampling
  - Coverage analysis
  - Coverage reporting

- **Coverage Patterns**
  - Transaction coverage
  - Protocol coverage
  - State coverage
  - Cross coverage

### 3. Complex Configuration Objects

- **Configuration Objects**
  - Configuration class design
  - Configuration fields
  - Configuration methods
  - Configuration validation

- **Configuration Hierarchy**
  - Hierarchical configuration
  - Configuration inheritance
  - Configuration override
  - Configuration patterns

- **Resource Database**
  - Resource database usage
  - Resource types
  - Resource lookup
  - Resource management

- **Configuration Callbacks**
  - Configuration callbacks
  - Pre/post callbacks
  - Callback registration
  - Callback execution

### 4. UVM Callbacks

- **Callback Overview**
  - What are callbacks?
  - Callback purpose
  - Callback types
  - Callback benefits

- **Callback Implementation**
  - Callback class definition
  - Callback registration
  - Callback execution
  - Callback patterns

- **Pre/Post Callbacks**
  - Pre-callbacks
  - Post-callbacks
  - Callback ordering
  - Callback control

- **Callback Use Cases**
  - Driver callbacks
  - Monitor callbacks
  - Scoreboard callbacks
  - Test callbacks

### 5. UVM Register Model (Advanced)

- **Register Model Overview**
  - Register model purpose
  - Register model structure
  - Register model benefits
  - Register model components

- **Register Model Components**
  - `uvm_reg_block` - Register blocks
  - `uvm_reg` - Registers
  - `uvm_reg_field` - Register fields
  - `uvm_reg_map` - Address maps

- **Register Operations**
  - Register read
  - Register write
  - Register peek/poke
  - Register update

- **Register Sequences**
  - Register access sequences
  - Register test sequences
  - Register model integration
  - Register predictor

- **Backdoor Access**
  - Backdoor read/write
  - Backdoor vs frontdoor
  - Backdoor use cases
  - Backdoor implementation

### 6. Virtual Sequences and Virtual Sequencers

- **Virtual Sequencer**
  - Virtual sequencer purpose
  - Virtual sequencer structure
  - Multiple sequencer references
  - Virtual sequencer implementation

- **Virtual Sequence Coordination**
  - Coordinating multiple sequencers
  - Parallel sequence execution
  - Sequence synchronization
  - Sequence coordination patterns

- **Virtual Sequence Patterns**
  - Master-slave coordination
  - Multi-channel coordination
  - Protocol coordination
  - Test coordination

### 7. Coverage Analysis and Closure

- **Coverage Analysis**
  - Coverage collection
  - Coverage reporting
  - Coverage gaps
  - Coverage analysis tools

- **Coverage Closure**
  - Coverage goals
  - Coverage strategies
  - Coverage improvement
  - Coverage metrics

- **Coverage Patterns**
  - Functional coverage
  - Code coverage
  - Assertion coverage
  - Coverage correlation

### 8. Advanced Configuration Patterns

- **Configuration Strategies**
  - Top-down configuration
  - Bottom-up configuration
  - Mixed configuration
  - Configuration best practices

- **Dynamic Configuration**
  - Runtime configuration
  - Configuration updates
  - Configuration validation
  - Configuration debugging

### 9. Performance Optimization

- **Testbench Performance**
  - Performance bottlenecks
  - Optimization strategies
  - Memory optimization
  - Simulation speed

- **Sequence Optimization**
  - Efficient sequence design
  - Sequence reuse
  - Sequence caching
  - Sequence performance

### 10. Advanced Debugging Techniques

- **UVM Debugging**
  - UVM debugging tools
  - Phase debugging
  - Component debugging
  - Transaction debugging

- **Coverage Debugging**
  - Coverage gaps
  - Coverage analysis
  - Coverage improvement
  - Coverage tools

## Learning Outcomes

By the end of this module, you should be able to:

- Create and use virtual sequences
- Implement coverage models
- Design complex configuration objects
- Use UVM callbacks effectively
- Use advanced register model features
- Coordinate multiple sequencers
- Analyze and close coverage
- Optimize testbench performance
- Debug advanced testbenches
- Apply advanced patterns

## Test Cases

### Test Case 5.1: Virtual Sequences
**Objective**: Create virtual sequence coordinating multiple sequencers

**Topics**:
- Virtual sequencer
- Virtual sequence
- Multiple sequencer coordination

#### Example 5.1: Virtual Sequences (`module5/examples/virtual_sequences/virtual_sequence_example.py`)

**What it demonstrates:**
- **Virtual Sequencer**: Container for multiple sequencer references
- **Virtual Sequence**: Sequence that coordinates multiple sequencers
- **Parallel Execution**: Starting sequences on different sequencers concurrently
- **Sequential Execution**: Running sequences in order
- **Multi-Channel Coordination**: Coordinating master and slave channels
- **Sequence Synchronization**: Synchronizing multiple sequence executions

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --virtual-sequences

# Or directly (syntax check)
cd module5/examples/virtual_sequences
python3 -c "import pyuvm; exec(open('virtual_sequence_example.py').read())"
```

**Expected Output:**
```
============================================================
Virtual Sequence Example Test
============================================================
Building VirtualEnv
Building MasterAgent
Building SlaveAgent
[virtual_seqr] Building virtual sequencer
[virtual_seqr] Connecting virtual sequencer
[VirtualSequence] Starting virtual sequence
[VirtualSequence] Starting parallel sequences
[master_seq] Starting channel 0 sequence
[slave_seq] Starting channel 1 sequence
...
[VirtualSequence] Parallel sequences completed
```

**Key Concepts:**
- **Virtual Sequencer**: Contains references to multiple sequencers
- **Virtual Sequence**: Coordinates sequences across multiple sequencers
- **Parallel Execution**: Use `cocotb.start_soon()` for concurrent sequences
- **Sequential Execution**: Use `await` for ordered sequence execution
- **Multi-Agent Coordination**: Coordinate sequences across multiple agents
- **Sequence Layering**: Virtual sequences can call other sequences

### Test Case 5.2: Coverage Model
**Objective**: Implement functional coverage

**Topics**:
- Coverage class
- Coverpoints and bins
- Coverage sampling

#### Example 5.2: Coverage Models (`module5/examples/coverage/coverage_example.py`)

**What it demonstrates:**
- **Coverage Class**: Inheriting from `uvm_subscriber` for coverage
- **Coverage Sampling**: Sampling transactions via analysis port
- **Coverpoints**: Tracking data, address ranges, commands
- **Coverage Bins**: Organizing coverage into bins (low, mid, high address ranges)
- **Cross Coverage**: Tracking combinations of coverage items
- **Coverage Reporting**: Generating coverage reports in report_phase

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --coverage

# Or directly
cd module5/examples/coverage
python3 -c "import pyuvm; exec(open('coverage_example.py').read())"
```

**Expected Output:**
```
============================================================
Coverage Example Test
============================================================
[coverage] Building coverage model
[monitor] Starting coverage monitor
[coverage] Sampling coverage for: data=0x00, addr=0x1000, cmd=0x01
...
============================================================
[coverage] Coverage Report
============================================================
Data Coverage: 5 unique values
Address Coverage:
  Low (0x0000-0x3FFF):  2 samples
  Mid (0x4000-0x7FFF):  1 samples
  High (0x8000-0xFFFF): 2 samples
Command Coverage: 3 unique commands
Cross Coverage: 5 unique combinations
Data Coverage: 2.0%
Command Coverage: 1.2%
```

**Key Concepts:**
- **`uvm_subscriber`**: Base class for coverage models
- **Analysis Port Connection**: Connect monitor to coverage via analysis port
- **Coverage Sampling**: Sample transactions in `write()` method
- **Coverage Bins**: Organize coverage into meaningful bins
- **Cross Coverage**: Track combinations of coverage items
- **Coverage Reporting**: Report coverage statistics in report_phase

### Test Case 5.3: Configuration Objects
**Objective**: Create complex configuration

**Topics**:
- Configuration class
- Configuration hierarchy
- Configuration usage

#### Example 5.3: Configuration Objects (`module5/examples/configuration/configuration_example.py`)

**What it demonstrates:**
- **Configuration Class Design**: Creating configuration objects inheriting from `uvm_object`
- **Configuration Fields**: Defining configuration parameters
- **Configuration Validation**: Validating configuration values
- **Hierarchical Configuration**: Environment and agent-level configuration
- **Configuration Composition**: Composing complex configurations from simpler ones
- **ConfigDB Usage**: Setting and getting configuration via ConfigDB

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --configuration

# Or directly
cd module5/examples/configuration
python3 -c "import pyuvm; exec(open('configuration_example.py').read())"
```

**Expected Output:**
```
============================================================
Configuration Example Test
============================================================
Building ConfigurableEnv
Set environment configuration: num_agents=2, master_config=...
[master_agent] Building configurable agent
[master_agent] Got config: active=True, has_coverage=True, ...
[master_agent] Agent is ACTIVE
[slave_agent] Building configurable agent
[slave_agent] Got config: active=False, has_coverage=False, ...
[slave_agent] Agent is PASSIVE
Configuration Hierarchy:
  Master agent config: active=True, has_coverage=True, ...
  Slave agent config: active=False, has_coverage=False, ...
```

**Key Concepts:**
- **`uvm_object`**: Base class for configuration objects
- **Configuration Design**: Design configuration classes with validation
- **Hierarchical Configuration**: Set configuration at different hierarchy levels
- **Configuration Validation**: Validate configuration in `validate()` method
- **ConfigDB**: Use ConfigDB for configuration storage and retrieval
- **Configuration Composition**: Build complex configurations from simpler ones

### Test Case 5.4: Callbacks
**Objective**: Implement callback mechanism

**Topics**:
- Callback class
- Callback registration
- Callback execution

#### Example 5.4: UVM Callbacks (`module5/examples/callbacks/callback_example.py`)

**What it demonstrates:**
- **Callback Class**: Creating callback classes inheriting from `uvm_callback`
- **Callback Methods**: Implementing pre/post callback methods
- **Callback Registration**: Registering callbacks with components
- **Callback Execution**: Executing callbacks at appropriate points
- **Driver Callbacks**: Pre-drive and post-drive callbacks
- **Monitor Callbacks**: Pre-sample and post-sample callbacks

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --callbacks

# Or directly
cd module5/examples/callbacks
python3 -c "import pyuvm; exec(open('callback_example.py').read())"
```

**Expected Output:**
```
============================================================
Callback Example Test
============================================================
Building CallbackEnv
Building CallbackAgent
[driver] Building driver with callbacks
[monitor] Building monitor with callbacks
Registering callbacks
Registered driver callback
Registered monitor callback
[driver] Starting driver
[driver] Executing pre-drive callbacks
[driver_callback] Pre-drive callback: data=0x00
[driver] Driving: data=0x00
[driver] Executing post-drive callbacks
[driver_callback] Post-drive callback: data=0x00
```

**Key Concepts:**
- **`uvm_callback`**: Base class for all callbacks
- **Callback Methods**: Implement callback methods (pre/post)
- **Callback Registration**: Register callbacks in `end_of_elaboration_phase()`
- **Callback Execution**: Execute callbacks using `get_callbacks()`
- **Pre/Post Callbacks**: Pre-callbacks before action, post-callbacks after
- **Callback Use Cases**: Modify transactions, add logging, add checks

### Test Case 5.5: Advanced Register Model
**Objective**: Use advanced register features

**Topics**:
- Register model
- Register sequences
- Backdoor access

#### Example 5.5: Register Model (`module5/examples/register_model/register_model_example.py`)

**What it demonstrates:**
- **Register Model Structure**: Creating register model classes
- **Register Operations**: Read, write, peek, poke operations
- **Register Sequences**: Sequences for register access
- **Frontdoor Access**: Normal register access through bus
- **Backdoor Access**: Direct register access (peek/poke)
- **Register Update**: Updating registers from model to hardware

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --register-model

# Or directly
cd module5/examples/register_model
python3 -c "import pyuvm; exec(open('register_model_example.py').read())"
```

**Expected Output:**
```
============================================================
Register Model Example Test
============================================================
Building RegisterEnv
Building RegisterAgent
[reg_model] Writing register 0x0000 (CONTROL): 0x01
[reg_model] Reading register 0x0000 (CONTROL): 0x01
Read back value: 0x01
[reg_model] Poking register 0x0004: 0x80
[reg_model] Peeking register 0x0004: 0x80
Peeked value: 0x80
[seq] Starting register sequence
[seq] Register operation: WRITE: addr=0x0000, data=0x01
```

**Key Concepts:**
- **Register Model**: Software model of hardware registers
- **Frontdoor Access**: Normal bus-based register access
- **Backdoor Access**: Direct register access (peek/poke)
- **Register Operations**: read(), write(), peek(), poke(), update()
- **Register Sequences**: Sequences for register testing
- **Note**: Full UVM register model support may vary in pyuvm

#### Test: Advanced UVM Test (`module5/tests/pyuvm_tests/test_advanced_uvm.py`)

**What it demonstrates:**
- Complete testbench with advanced UVM features
- Coverage integration
- Advanced component usage
- Full test flow

**Execution:**
```bash
# Using orchestrator script
./scripts/module5.sh --pyuvm-tests

# Or manually
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm
```

**Test Structure:**
- `AdvancedTransaction`: Transaction for advanced test
- `AdvancedSequence`: Generates test vectors
- `AdvancedDriver`: Drives transactions
- `AdvancedMonitor`: Monitors DUT
- `AdvancedCoverage`: Coverage model
- `AdvancedAgent`: Contains driver, monitor, sequencer
- `AdvancedEnv`: Contains agent and coverage
- `AdvancedUVMTest`: Top-level test class

### Design Under Test (DUT) Modules

#### Multi-Channel Interface (`module5/dut/advanced/multi_channel.v`)
- **Purpose**: Multi-channel interface with master and slave channels
- **Used in**: Advanced UVM test
- **Features**: Clocked operation, reset, valid/ready handshaking, separate channels

## Exercises

1. **Virtual Sequences**
   - Create virtual sequencer
   - Create virtual sequence
   - Coordinate multiple agents
   - **Location**: Extend `module5/examples/virtual_sequences/virtual_sequence_example.py`
   - **Hint**: Add more channels and coordinate them in virtual sequence

2. **Coverage Implementation**
   - Design coverage model
   - Implement coverage
   - Analyze coverage
   - **Location**: Extend `module5/examples/coverage/coverage_example.py`
   - **Hint**: Add more coverpoints and cross coverage bins

3. **Configuration Design**
   - Create configuration classes
   - Implement hierarchy
   - Use configuration
   - **Location**: Extend `module5/examples/configuration/configuration_example.py`
   - **Hint**: Create configuration for multiple agents with different settings

4. **Callback Implementation**
   - Create callbacks
   - Register callbacks
   - Use callbacks
   - **Location**: Extend `module5/examples/callbacks/callback_example.py`
   - **Hint**: Add callbacks for scoreboard and add transaction modification

5. **Register Model**
   - Create register model
   - Implement sequences
   - Use backdoor access
   - **Location**: Extend `module5/examples/register_model/register_model_example.py`
   - **Hint**: Add more registers and implement register field access

## Assessment

- [ ] Can create virtual sequences
- [ ] Can implement coverage models
- [ ] Can design configuration objects
- [ ] Can use callbacks effectively
- [ ] Can use advanced register model
- [ ] Can coordinate multiple sequencers
- [ ] Can analyze coverage
- [ ] Can optimize performance
- [ ] Can debug advanced testbenches
- [ ] Understands advanced patterns

## Next Steps

After completing this module, proceed to [Module 6: Complex Testbenches](MODULE6.md) to learn how to build complex multi-agent testbenches.

## Additional Resources

- **pyuvm Documentation**: https://pyuvm.readthedocs.io/
- **UVM 1.2 User's Guide**: Accellera Systems Initiative
- **Advanced UVM**: Ray Salemi
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

**Issue: Virtual sequence not coordinating sequencers**
```bash
# Solution: Ensure virtual sequencer has references to actual sequencers
# Set in connect_phase: virtual_seqr.master_seqr = master_agent.seqr
# Pass to virtual sequence: virtual_seq.master_seqr = env.virtual_seqr.master_seqr
```

**Issue: Coverage not sampling**
```bash
# Solution: Check analysis port connection
# Ensure: monitor.ap.connect(coverage.ap)
# Verify coverage implements write() method
```

**Issue: Callbacks not executing**
```bash
# Solution: Register callbacks in end_of_elaboration_phase()
# Ensure: component.add_callback(callback)
# Verify callback methods are implemented correctly
```

**Issue: Configuration not found**
```bash
# Solution: Set configuration before component build_phase
# Use ConfigDB().set() in test build_phase
# Check configuration path matches component hierarchy
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module5/README.md` for directory structure
- Run examples individually to understand each advanced concept
- Study virtual sequence coordination in `virtual_sequence_example.py`
- Review coverage implementation in `coverage_example.py`
- Check pyuvm documentation for advanced features

### Summary of Examples and Tests

**Examples (pyuvm structural examples in `module5/examples/`):**
1. **Example 5.1: Virtual Sequences** (`virtual_sequences/`) - Virtual sequencer and sequence coordination
2. **Example 5.2: Coverage Models** (`coverage/`) - Functional coverage implementation
3. **Example 5.3: Configuration Objects** (`configuration/`) - Complex configuration design
4. **Example 5.4: UVM Callbacks** (`callbacks/`) - Callback implementation and usage
5. **Example 5.5: Register Model** (`register_model/`) - Register model operations

**Testbenches (runnable tests in `module5/tests/pyuvm_tests/`):**
1. **Advanced UVM Test** (`test_advanced_uvm.py`) - Complete testbench with advanced features

**DUT Modules (in `module5/dut/`):**
1. **Multi-Channel Interface** (`advanced/multi_channel.v`) - Multi-channel interface for advanced testing

**Coverage:**
- ✅ Virtual sequences and virtual sequencers
- ✅ Functional coverage models
- ✅ Complex configuration objects
- ✅ UVM callback mechanism
- ✅ Register model operations
- ✅ Advanced testbench integration

