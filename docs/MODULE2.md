# Module 2: cocotb Fundamentals

**Goal**: Master cocotb for hardware verification

## Overview

This module provides comprehensive coverage of cocotb, the coroutine-based testbench framework that enables Python testbenches for hardware designs. You'll learn how to interact with simulators, drive signals, sample values, and create robust testbenches.

> **📖 Fundamental Concept**: Before diving into the details, make sure you understand [How Python and Verilog Interact](PYTHON_VERILOG_INTERACTION.md). This foundational document explains the two-layer architecture, signal flow, time synchronization, and how Cocotb bridges Python testbenches with Verilog hardware designs.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module2/` directory:

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
└── README.md             # Module 2 documentation
```

### Quick Start

**Run all tests using the orchestrator script:**
```bash
# Run all cocotb tests
./scripts/module2.sh --cocotb-tests

# Run specific examples (note: examples are cocotb test files)
./scripts/module2.sh --signal-access
./scripts/module2.sh --clock-generation
./scripts/module2.sh --triggers
./scripts/module2.sh --reset-patterns
./scripts/module2.sh --common-patterns
```

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run cocotb tests
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
make SIM=verilator TEST=test_shift_register

# Run examples (they are cocotb test files)
cd module2/examples/signal_access
# Create a Makefile or run with cocotb directly
```

## Topics Covered

### 1. cocotb Architecture and Concepts

- **What is cocotb?**
  - Coroutine-based testbench framework
  - Python testbenches for Verilog/VHDL
  - Simulator abstraction
  - History and motivation

- **cocotb Architecture**
  - Python testbench layer
  - Simulator interface layer
  - DUT interaction
  - Event scheduling

- **Key Concepts**
  - Coroutines for simulation
  - Triggers for synchronization
  - Handles for signal access
  - Simulation time management

### 2. Simulator Integration

- **Supported Simulators**
  - Verilator (recommended)
  - Icarus Verilog
  - ModelSim/QuestaSim
  - GHDL (VHDL)
  - VCS, Xcelium (commercial)

- **Simulator Selection**
  - Environment variables
  - Makefile configuration
  - Simulator-specific features

- **Compilation Process**
  - Verilog compilation
  - cocotb library compilation
  - Linking process
  - Makefile structure

### 3. Clock Generation and Management

- **Clock Generation**
  - `Clock` class usage
  - Clock parameters (period, units)
  - Starting clocks
  - Multiple clocks

- **Clock Patterns**
  - Regular clocks
  - Gated clocks
  - Clock division
  - Clock stopping

- **Clock Domain Management**
  - Multiple clock domains
  - Clock domain crossing
  - Synchronization between domains

### 4. Signal Access and Driving

- **Signal Handles**
  - Accessing DUT signals
  - `dut.signal_name` syntax
  - Signal value types
  - Signal properties

- **Reading Signal Values**
  - `.value` property
  - Integer conversion
  - Binary representation
  - Signal state checking

- **Driving Signals**
  - Assigning values
  - Integer assignment
  - Binary string assignment
  - High-impedance (Z) and unknown (X)

- **Signal Types**
  - Single-bit signals
  - Multi-bit signals (vectors)
  - Buses and arrays
  - Bidirectional signals

### 5. Triggers and Coroutines

- **Trigger Types**
  - `RisingEdge(signal)`
  - `FallingEdge(signal)`
  - `Edge(signal)` (any edge)
  - `Timer(time, units)`
  - `ReadOnly()` (end of time step)
  - `ReadWrite()` (during time step)
  - `Combine(*triggers)` (multiple triggers)
  - `First(*triggers)` (first to occur)

- **Coroutine Execution**
  - Defining coroutines
  - Starting coroutines
  - `cocotb.start_soon()` vs `await`
  - Parallel execution

- **Coroutine Synchronization**
  - Waiting for triggers
  - Coordinating multiple coroutines
  - Timeout handling
  - Exception propagation

### 6. Test Structure and Organization

- **Test Function Structure**
  - `@cocotb.test()` decorator
  - Test function signature
  - DUT parameter
  - Test organization

- **Test Phases**
  - Setup phase
  - Test execution
  - Cleanup phase
  - Error handling

- **Multiple Tests**
  - Test discovery
  - Test selection
  - Test parameters
  - Test fixtures

### 7. Reset and Initialization

- **Reset Strategies**
  - Synchronous reset
  - Asynchronous reset
  - Reset sequences
  - Reset verification

- **Initialization Patterns**
  - Signal initialization
  - State initialization
  - Configuration setup
  - Initial conditions

### 8. Common Verification Patterns

- **Stimulus Generation**
  - Sequential patterns
  - Random patterns
  - Constrained random
  - File-based stimulus

- **Response Checking**
  - Immediate checking
  - Deferred checking
  - Reference model comparison
  - Scoreboard patterns

- **Transaction-Level Modeling**
  - Transaction classes
  - Transaction generation
  - Transaction execution
  - Transaction checking

**See Example 2.6**: Common Verification Patterns (`module2/examples/common_patterns/common_patterns_example.py`) for detailed implementation.

### 9. Debugging with cocotb

- **Logging and Reporting**
  - cocotb logging
  - Log levels
  - Log formatting
  - Debug messages

- **Waveform Generation**
  - VCD file generation
  - FST file generation
  - Waveform viewing
  - Signal tracing

- **Interactive Debugging**
  - Python debugger (pdb)
  - Breakpoints
  - Variable inspection
  - Step-through debugging

- **Common Issues**
  - Signal access errors
  - Timing issues
  - Simulation hangs
  - Value conversion problems

### 10. Advanced cocotb Features

- **Memory Access**
  - Memory modeling
  - Memory initialization
  - Memory access patterns

- **Bus Functional Models (BFM)**
  - BFM concepts
  - BFM implementation
  - Reusable BFMs

- **Performance Optimization**
  - Coroutine efficiency
  - Trigger optimization
  - Simulation speed
  - Memory usage

### 11. Integration with pytest

- **pytest Integration**
  - Using pytest with cocotb
  - Test discovery
  - Fixtures
  - Parametrization

- **Test Organization**
  - Test directory structure
  - Test naming conventions
  - Test grouping
  - Test execution

## Learning Outcomes

By the end of this module, you should be able to:

- Understand cocotb architecture
- Integrate with simulators
- Generate and manage clocks
- Access and drive signals
- Use triggers effectively
- Structure tests properly
- Implement reset sequences
- Use common verification patterns
- Debug cocotb testbenches
- Optimize testbench performance

## Test Cases

### Test Case 2.1: Basic Signal Access
**Objective**: Access and read DUT signals

**Topics**:
- Signal handles
- Value reading
- Signal types

#### Example 2.1: Signal Access (`module2/examples/signal_access/signal_access_example.py`)

**What it demonstrates:**
- **Signal Handles**: Accessing DUT signals using `dut.signal_name`
- **Value Reading**: Reading signal values with `.value` property
- **Value Types**: Integer, binary, and hex representations
- **Signal Properties**: Signal width, name, path
- **Value Assignments**: Different ways to assign values (integer, BinaryValue)

**Execution:**
```bash
# Using orchestrator script (runs tests)
./scripts/module2.sh --signal-access

# Or manually with cocotb
cd module2/examples/signal_access
# Note: These are cocotb test files, need proper Makefile setup
# Or use in your own testbench
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_signal_access_basic (1/3)
Initial q value: 0
Initial q value (integer): 0
Initial q value (binary): 00000000
After reset q value: 0
After write q value: 0xAB
     0.00ns INFO     cocotb.regression                  test_signal_access_basic passed
```

**Key Concepts:**
- **`dut.signal_name`**: Access DUT signals
- **`.value`**: Get/set signal value
- **`.value.integer`**: Get integer representation
- **`.value.binstr`**: Get binary string representation
- **`BinaryValue`**: Create values from binary strings
- **Signal Width**: Use `len(dut.signal)` to get width

### Test Case 2.2: Clock Generation
**Objective**: Generate and manage clocks

**Topics**:
- Clock class
- Clock starting
- Multiple clocks

#### Example 2.2: Clock Generation (`module2/examples/clock_generation/clock_generation_example.py`)

**What it demonstrates:**
- **Clock Class**: Using `Clock(dut.clk, period, units)` to create clocks
- **Starting Clocks**: Using `cocotb.start_soon(clock.start())` to run clocks in background
- **Multiple Clocks**: Creating and managing multiple clock domains
- **Clock Gating**: Implementing clock enable/disable patterns
- **Clock Division**: Creating divided clock signals
- **Clock Stopping**: Stopping clock generation

**Execution:**
```bash
# Using orchestrator script
./scripts/module2.sh --clock-generation

# Or manually
cd module2/examples/clock_generation
# Run as cocotb test
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_clock_class (1/5)
Clock cycle 1
Clock cycle 2
Clock cycle 3
Clock cycle 4
Clock cycle 5
     0.00ns INFO     cocotb.regression                  test_clock_class passed
```

**Key Concepts:**
- **`Clock(signal, period, units)`**: Create clock object
- **`clock.start()`**: Start clock generation (returns coroutine)
- **`cocotb.start_soon()`**: Run coroutine in background
- **Multiple Clocks**: Each clock runs independently
- **Clock Gating**: Control clock with enable signals
- **Clock Division**: Divide clock frequency by counting edges

### Test Case 2.3: Signal Driving
**Objective**: Drive signals with values

**Topics**:
- Value assignment
- Timing control
- Signal updates

#### Example 2.3: Signal Driving

**What it demonstrates:**
Signal driving is demonstrated throughout the examples, particularly in:
- **Signal Access Example**: Shows reading and writing signals
- **Reset Patterns Example**: Demonstrates driving reset signals
- **Common Patterns Example**: Shows driving data signals with timing

**Key Concepts:**
- **Direct Assignment**: `dut.signal.value = value`
- **Integer Assignment**: `dut.signal.value = 0xAB`
- **Binary Assignment**: `dut.signal.value = BinaryValue("10101010")`
- **Hex Assignment**: `dut.signal.value = 0xAB` (same as integer)
- **Timing Control**: Use `await Timer()` or `await RisingEdge()` before reading driven values
- **ReadOnly Trigger**: Wait for `ReadOnly()` to ensure signal is stable after assignment
- **Signal Updates**: Signals update at the next simulation time step

**Example Code Pattern:**
```python
# Drive signal
dut.data.value = 0xAB

# Wait for signal to propagate
await RisingEdge(dut.clk)
await Timer(1, units="ns")  # Small delay for combinational logic

# Read back
assert dut.output.value.integer == expected_value
```

**See Also:**
- Signal driving in `module2/examples/signal_access/signal_access_example.py`
- Reset signal driving in `module2/examples/reset_patterns/reset_patterns_example.py`
- Data signal driving in `module2/examples/common_patterns/common_patterns_example.py`

### Test Case 2.4: Trigger Usage
**Objective**: Use various triggers

**Topics**:
- Edge triggers
- Timer triggers
- Combined triggers

#### Example 2.4: Triggers (`module2/examples/triggers/triggers_example.py`)

**What it demonstrates:**
- **Edge Triggers**: `RisingEdge()`, `FallingEdge()`, `Edge()`
- **Timer Triggers**: `Timer(time, units)` for time-based delays
- **ReadOnly Trigger**: `ReadOnly()` waits for end of time step
- **ReadWrite Trigger**: `ReadWrite()` for during time step
- **Combine Trigger**: `Combine(*triggers)` waits for all triggers
- **First Trigger**: `First(*triggers)` waits for first trigger
- **Timeout Handling**: Using triggers with timeout
- **Parallel Triggers**: Multiple coroutines with different triggers

**Execution:**
```bash
# Using orchestrator script
./scripts/module2.sh --triggers

# Or manually
cd module2/examples/triggers
# Run as cocotb test
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_edge_triggers (1/7)
Waiting for rising edge...
Rising edge detected
Waiting for falling edge...
Falling edge detected
Waiting for any edge...
Edge detected
     0.00ns INFO     cocotb.regression                  test_edge_triggers passed
```

**Key Concepts:**
- **`RisingEdge(signal)`**: Wait for 0→1 transition
- **`FallingEdge(signal)`**: Wait for 1→0 transition
- **`Edge(signal)`**: Wait for any edge
- **`Timer(time, units)`**: Wait for specified time
- **`ReadOnly()`**: Wait for end of time step (signals stable)
- **`Combine(*triggers)`**: Wait for all triggers to occur
- **`First(*triggers)`**: Wait for first trigger to occur
- **Parallel Execution**: Multiple coroutines can wait on different triggers

### Test Case 2.5: Reset Sequence
**Objective**: Implement reset sequence

**Topics**:
- Reset patterns
- Reset verification
- Initialization

#### Example 2.5: Reset Patterns (`module2/examples/reset_patterns/reset_patterns_example.py`)

**What it demonstrates:**
- **Async Reset**: Asynchronous reset sequence with timing
- **Sync Reset**: Synchronous reset synchronized to clock
- **Reset Verification**: Checking that reset works correctly
- **Reset Timing**: Proper reset assertion and deassertion timing
- **Initialization**: Setting up signals after reset
- **Reset During Operation**: Testing reset while DUT is operating

**Execution:**
```bash
# Using orchestrator script
./scripts/module2.sh --reset-patterns

# Or manually
cd module2/examples/reset_patterns
# Run as cocotb test
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_async_reset (1/4)
Asserting async reset...
Deasserting async reset...
Reset complete
✓ Async reset verified
     0.00ns INFO     cocotb.regression                  test_async_reset passed
```

**Key Concepts:**
- **Async Reset**: Assert reset, wait duration, deassert reset
- **Sync Reset**: Assert reset, wait for clock cycles, deassert on clock edge
- **Reset Verification**: Always check that reset puts DUT in known state
- **Reset Timing**: Proper timing ensures reset propagates through design
- **Initialization**: Set up control signals after reset completes
- **Reset Patterns**: Create reusable reset functions for different reset types

#### Example 2.6: Common Verification Patterns (`module2/examples/common_patterns/common_patterns_example.py`)

**What it demonstrates:**
- **Sequential Patterns**: Deterministic stimulus generation
- **Random Patterns**: Random stimulus with seed control
- **Scoreboard Pattern**: Expected vs actual comparison
- **Reference Model**: Golden reference for checking
- **Transaction-Level Modeling**: High-level transaction abstraction
- **Scoreboard Class**: Reusable scoreboard implementation

**Execution:**
```bash
# Using orchestrator script
./scripts/module2.sh --common-patterns

# Or manually
cd module2/examples/common_patterns
# Run as cocotb test
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_sequential_pattern (1/5)
Wrote 0x01, read 0x01
Wrote 0x02, read 0x02
Wrote 0x03, read 0x03
...
     0.00ns INFO     cocotb.regression                  test_sequential_pattern passed
```

**Key Concepts:**
- **Sequential Patterns**: Predictable, repeatable stimulus
- **Random Patterns**: Use `random.seed()` for reproducibility
- **Scoreboard**: Track expected vs actual for verification
- **Reference Model**: Software model of expected behavior
- **Transactions**: High-level abstraction for operations
- **Pattern Reusability**: Create reusable verification components

### Testbenches

#### Test: Simple Register (`module2/tests/cocotb_tests/test_simple_register.py`)

**What it tests:**
- Register reset functionality
- Register write operations
- Enable control behavior
- All 8-bit value boundaries

**Execution:**
```bash
# Using orchestrator script
./scripts/module2.sh --cocotb-tests

# Or manually
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
```

**Test Functions:**
- `test_register_reset`: Verifies reset puts register to 0
- `test_register_write`: Tests basic write operation
- `test_register_enable`: Tests enable control
- `test_register_all_values`: Tests boundary values (0x00, 0x01, 0x7F, 0x80, 0xFE, 0xFF)

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_register_reset (1/4)
     0.00ns INFO     cocotb.regression                  Running test_register_write (2/4)
     0.00ns INFO     cocotb.regression                  Running test_register_enable (3/4)
     0.00ns INFO     cocotb.regression                  Running test_register_all_values (4/4)
     0.00ns INFO     cocotb.regression                  test_simple_register passed
```

#### Test: Shift Register (`module2/tests/cocotb_tests/test_shift_register.py`)

**What it tests:**
- Shift register reset
- Serial shift operation
- Serial output behavior

**Execution:**
```bash
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_shift_register
```

**Test Functions:**
- `test_shift_register_reset`: Verifies reset clears register
- `test_shift_register_operation`: Tests serial shift in
- `test_shift_register_serial_out`: Tests serial shift out

### Design Under Test (DUT) Modules

#### Simple Register (`module2/dut/registers/simple_register.v`)
- **Purpose**: Basic 8-bit register with clock, reset, and enable
- **Used in**: Signal access, clock generation, reset pattern examples
- **Features**: Synchronous reset, enable control, 8-bit data path

#### Shift Register (`module2/dut/registers/shift_register.v`)
- **Purpose**: 8-bit serial-in, serial-out shift register
- **Used in**: Shift register testbench
- **Features**: Serial input/output, parallel output, shift enable

#### Simple FIFO (`module2/dut/fifos/simple_fifo.v`)
- **Purpose**: 16-entry FIFO with read/write pointers
- **Features**: Full/empty flags, 8-bit data width, synchronous operation
- **Note**: Available for future testbench development

#### Simple FSM (`module2/dut/state_machines/simple_fsm.v`)
- **Purpose**: 4-state finite state machine
- **Features**: IDLE, START, WORK, DONE states, start/done signals
- **Note**: Available for future testbench development

## Exercises

1. **Clock Management**
   - Create multiple clocks
   - Implement clock gating
   - Synchronize operations
   - **Location**: Extend `module2/examples/clock_generation/clock_generation_example.py`
   - **Hint**: Create two clocks with different periods and synchronize operations between them

2. **Signal Operations**
   - Read and write signals
   - Handle multi-bit signals
   - Work with buses
   - **Location**: Extend `module2/examples/signal_access/signal_access_example.py`
   - **Hint**: Test with different signal widths (1-bit, 8-bit, 16-bit, 32-bit)

3. **Trigger Patterns**
   - Use various triggers
   - Combine triggers
   - Handle timeouts
   - **Location**: Extend `module2/examples/triggers/triggers_example.py`
   - **Hint**: Create a timeout mechanism that cancels an operation if it takes too long

4. **Test Structure**
   - Organize tests
   - Implement fixtures
   - Handle errors
   - **Location**: Create new test in `module2/tests/cocotb_tests/`
   - **Hint**: Create a test fixture that sets up clock and reset for all tests

5. **Debugging**
   - Add logging
   - Generate waveforms
   - Use debugger
   - **Location**: Add to existing tests
   - **Hint**: Use `cocotb.log` for logging and enable VCD generation in Makefile

## Assessment

- [ ] Understands cocotb architecture
- [ ] Can integrate with simulators
- [ ] Can generate and manage clocks
- [ ] Can access and drive signals
- [ ] Can use triggers effectively
- [ ] Can structure tests properly
- [ ] Can implement reset sequences
- [ ] Can use common verification patterns
- [ ] Can debug cocotb testbenches
- [ ] Understands performance optimization

## Next Steps

After completing this module, proceed to [Module 3: UVM Basics](MODULE3.md) to learn the UVM methodology and class hierarchy.

## Additional Resources

- **cocotb Documentation**: https://docs.cocotb.org/
- **cocotb Examples**: https://github.com/cocotb/cocotb/tree/master/examples
- **cocotb Cookbook**: https://docs.cocotb.org/en/stable/cookbook.html
- **Verilator Documentation**: https://verilator.org/

## Troubleshooting

### Common Issues

**Issue: "cocotb not found" error**
```bash
# Solution: Install cocotb
./scripts/install_cocotb.sh --pip --venv .venv
# Or
./scripts/module0.sh
```

**Issue: "verilator not found" error**
```bash
# Solution: Install Verilator
./scripts/install_verilator.sh --from-submodule
# Or
./scripts/module0.sh
```

**Issue: Makefile errors when running tests**
```bash
# Solution: Check Makefile paths and cocotb installation
cd module2/tests/cocotb_tests
make SIM=verilator TEST=test_simple_register
# Ensure VERILOG_FILES path is correct
```

**Issue: Signal access errors**
```bash
# Solution: Check signal names match Verilog module
# Use: dut._discover_all() to see all available signals
# Or check: print(dut._name, dut._path)
```

**Issue: Simulation hangs**
```bash
# Solution: Check for infinite loops in coroutines
# Ensure all coroutines have exit conditions
# Use timeouts: await First(trigger, Timer(timeout))
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module2/README.md` for directory structure
- Run tests individually to isolate issues: `make SIM=verilator TEST=test_name`
- Check cocotb logs for detailed error messages
- Use `cocotb.log.set_level(cocotb.log.DEBUG)` for verbose logging
- Review all examples in `module2/examples/` for patterns
- Check testbenches in `module2/tests/cocotb_tests/` for complete examples

### Summary of Examples and Tests

**Examples (cocotb test files in `module2/examples/`):**
1. **Example 2.1: Signal Access** (`signal_access/`) - Signal reading/writing, value types
2. **Example 2.2: Clock Generation** (`clock_generation/`) - Clock patterns, gating, division
3. **Example 2.3: Signal Driving** - Demonstrated in signal access and reset examples
4. **Example 2.4: Triggers** (`triggers/`) - Edge triggers, timers, combined triggers
5. **Example 2.5: Reset Patterns** (`reset_patterns/`) - Async/sync reset sequences
6. **Example 2.6: Common Patterns** (`common_patterns/`) - Scoreboard, reference models, transactions

**Testbenches (runnable tests in `module2/tests/cocotb_tests/`):**
1. **Simple Register Test** (`test_simple_register.py`) - 4 test functions covering reset, write, enable, boundaries
2. **Shift Register Test** (`test_shift_register.py`) - 3 test functions covering reset, shift operation, serial output

**DUT Modules (in `module2/dut/`):**
1. **Simple Register** (`registers/simple_register.v`) - Used in examples and tests
2. **Shift Register** (`registers/shift_register.v`) - Used in shift register test
3. **Simple FIFO** (`fifos/simple_fifo.v`) - Available for future testbench development
4. **Simple FSM** (`state_machines/simple_fsm.v`) - Available for future testbench development

**Coverage:**
- ✅ Signal access and driving
- ✅ Clock generation and management
- ✅ Trigger usage
- ✅ Reset patterns
- ✅ Common verification patterns
- ✅ Test structure and organization
- ✅ Complete testbenches with assertions

