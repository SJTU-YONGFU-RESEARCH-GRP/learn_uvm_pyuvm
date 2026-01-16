# Module 1: Python and Verification Basics

This directory contains all examples, exercises, and test cases for Module 1, focusing on Python fundamentals for hardware verification and basic testbench concepts.

## Directory Structure

```
module1/
├── examples/              # Python examples for each topic
│   ├── python_basics/     # Classes, inheritance, OOP
│   │   └── transaction.py
│   ├── decorators/        # Decorators and context managers
│   │   └── decorators_example.py
│   ├── async_await/       # Async/await patterns
│   │   └── async_example.py
│   ├── data_structures/   # Data structures for verification
│   │   └── data_structures_example.py
│   └── error_handling/    # Exception handling and logging
│       └── error_handling_example.py
├── dut/                   # Verilog Design Under Test modules
│   └── simple_gates/
│       ├── and_gate.v     # 2-input AND gate
│       └── counter.v      # 8-bit up counter with reset
├── tests/                 # Testbenches
│   ├── cocotb_tests/      # cocotb testbenches
│   │   ├── test_and_gate.py
│   │   └── test_counter.py
│   └── pyuvm_tests/       # pyuvm testbenches
│       └── test_and_gate_uvm.py
└── exercises/             # Exercise solutions (if any)
```

## Prerequisites

Before running the experiments, ensure you have:

- **Python 3.8+** - Required for cocotb and pyuvm
- **Verilator 5.036+** - Required for simulation (5.044 recommended)
- **cocotb 2.0+** - Installed in virtual environment
- **pyuvm 4.0+** - Installed in virtual environment
- **Make** - For building and running tests

To verify your environment:

```bash
python3 --version        # Should be 3.8+
verilator --version      # Should be 5.036+
python3 -c "import cocotb; print(cocotb.__version__)"
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

## Python Examples

### 1. Python Basics (`examples/python_basics/transaction.py`)

Demonstrates object-oriented programming concepts essential for verification:

- **Transaction Class**: Base class for verification data structures
  - `__init__`, `__repr__`, `__eq__`, `__hash__` methods
  - Class attributes and instance variables
- **Inheritance**: Creating derived transaction classes
  - `ReadTransaction` - Extends base with address field
  - `WriteTransaction` - Extends base with address and data fields
- **Hashability**: Making objects hashable for use in sets and dictionaries

**Running the example:**

```bash
# Run via module script
./scripts/module1.sh --python-basics

# Or directly
python3 module1/examples/python_basics/transaction.py
```

**Expected Output:**
- Base transaction creation and manipulation
- Derived transaction examples showing inheritance
- Equality testing between transactions
- Using transactions in sets (requires `__hash__`)

### 2. Decorators (`examples/decorators/decorators_example.py`)

Shows Python decorators and context managers for testbench patterns:

- **Function Decorators**: Wrapping functions with timing/logging
  - Automatic setup/teardown
  - Execution timing measurement
- **Context Managers**: Resource management patterns
  - Class-based context managers
  - Function-based context managers using `@contextmanager`
  - Nested context managers for hierarchical phases

**Key Concepts:**
- `@timing_decorator` - Measures function execution time
- `VerificationContext` - Class-based context manager
- `simulation_phase()` - Function-based context manager
- Automatic resource cleanup via `__exit__`

**Running the example:**

```bash
./scripts/module1.sh --decorators
# or
python3 module1/examples/decorators/decorators_example.py
```

### 3. Async/Await (`examples/async_await/async_example.py`)

Demonstrates asynchronous programming for simulation:

- **Sequential Execution**: Sequential async operations
- **Parallel Execution**: Concurrent async tasks with `asyncio.gather()`
- **Timeout Handling**: Using `asyncio.wait_for()` for timeouts
- **Exception Handling**: Proper error handling in async contexts

**Key Patterns:**
- Sequential async operations
- Parallel task execution
- Timeout management
- Exception propagation in async code

**Running the example:**

```bash
./scripts/module1.sh --async-await
# or
python3 module1/examples/async_await/async_example.py
```

### 4. Data Structures (`examples/data_structures/data_structures_example.py`)

Shows data structures commonly used in verification:

- **Transaction Queues**: Using `collections.deque` for FIFO queues
- **Scoreboards**: Using `collections.defaultdict` and `Counter` for checking
- **Coverage Collectors**: Using `set` and `Counter` for coverage tracking
- **List/Dict Comprehensions**: Pythonic data transformations

**Key Data Structures:**
- `deque` - Fast FIFO/LIFO queue operations
- `defaultdict` - Automatic dictionary initialization
- `Counter` - Counting occurrences
- `set` - Unique value tracking
- Comprehensions for data generation

**Running the example:**

```bash
./scripts/module1.sh --data-structures
# or
python3 module1/examples/data_structures/data_structures_example.py
```

### 5. Error Handling (`examples/error_handling/error_handling_example.py`)

Demonstrates exception handling and logging:

- **Basic Error Handling**: Try/except blocks for error recovery
- **Exception Chaining**: Preserving exception context with `raise ... from`
- **Retry Logic**: Implementing retry mechanisms with exponential backoff
- **Logging Levels**: Using Python `logging` module with different levels

**Key Features:**
- Custom exception classes
- Exception chaining for debugging
- Retry mechanisms with configurable attempts
- Structured logging to file and console

**Running the example:**

```bash
./scripts/module1.sh --error-handling
# or
python3 module1/examples/error_handling/error_handling_example.py
```

**Output Files:**
- `verification.log` - Detailed log file with all log levels

## Design Under Test (DUT)

### AND Gate (`dut/simple_gates/and_gate.v`)

A simple 2-input AND gate for basic verification examples.

**Module Interface:**
```verilog
module and_gate (
    input  wire a,    // Input signal A
    input  wire b,    // Input signal B
    output reg  y     // Output signal Y = A & B
);
```

**Truth Table:**
| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Characteristics:**
- Combinational logic
- No clock required
- Immediate output propagation

### Counter (`dut/simple_gates/counter.v`)

An 8-bit up counter with active-low reset and enable.

**Module Interface:**
```verilog
module counter (
    input  wire       clk,     // Clock signal
    input  wire       rst_n,   // Active-low reset
    input  wire       enable,  // Counter enable
    output reg [7:0]  count    // 8-bit counter output
);
```

**Functionality:**
- Resets to 0 when `rst_n` is low
- Increments on positive clock edge when `enable` is high
- Holds value when `enable` is low
- Wraps around at 0xFF → 0x00

**Characteristics:**
- Sequential logic
- Requires clock signal
- Synchronous reset

## Testbenches

### cocotb Tests (`tests/cocotb_tests/`)

#### AND Gate Test (`test_and_gate.py`)

Comprehensive testbench for the AND gate using cocotb:

**Test Cases:**
1. `test_and_gate_basic` - Basic truth table test
   - Tests all 4 input combinations
   - Verifies correct output for each combination
   - Uses `Timer` for signal propagation delays

2. `test_and_gate_truth_table` - Systematic truth table verification
   - Uses loop to iterate through all combinations
   - Checks output using `dut.y.value` access
   - Demonstrates test vector generation

3. `test_and_gate_timing` - Timing verification
   - Tests signal propagation timing
   - Verifies output stability
   - Checks response to input changes

**Running the test:**

```bash
# Via module script (runs all cocotb tests)
./scripts/module1.sh --cocotb-tests

# Directly from test directory
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
```

**Expected Results:**
- 3 test cases, all passing
- Total simulation time: ~105ns
- All input combinations verified

#### Counter Test (`test_counter.py`)

Testbench for the counter module:

**Test Cases:**
1. `test_counter_reset` - Reset functionality
   - Verifies counter resets to 0
   - Tests active-low reset behavior

2. `test_counter_increment` - Increment functionality
   - Verifies counter increments correctly
   - Tests 10 consecutive clock cycles
   - Validates enable control

3. `test_counter_enable` - Enable control
   - Tests counter hold when disabled
   - Verifies increment when enabled

4. `test_counter_overflow` - Overflow behavior
   - Tests wrap-around at 0xFF → 0x00
   - Verifies 256 count cycles

**Key Features:**
- Clock generation using `cocotb.start_soon()`
- Reset sequence helper function
- Rising edge detection using `RisingEdge` trigger

**Running the test:**

```bash
# Via module script
./scripts/module1.sh --cocotb-tests

# Directly from test directory
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_counter
```

**Expected Results:**
- 4 test cases, all passing
- Total simulation time: ~2773ns (includes overflow test)
- All counter functionality verified

### pyuvm Tests (`tests/pyuvm_tests/`)

#### AND Gate UVM Test (`test_and_gate_uvm.py`)

UVM-style testbench demonstrating pyuvm architecture:

**UVM Components:**

1. **Transaction (`AndGateTransaction`)**
   - Extends `uvm_sequence_item`
   - Contains test data (a, b, expected_y)

2. **Sequence (`AndGateSequence`)**
   - Extends `uvm_sequence`
   - Generates test vectors for the AND gate

3. **Driver (`AndGateDriver`)**
   - Extends `uvm_driver`
   - Drives transactions to DUT (pattern shown)
   - Uses `seq_item_port` for communication

4. **Monitor (`AndGateMonitor`)**
   - Extends `uvm_monitor`
   - Observes DUT outputs (pattern shown)
   - Uses `analysis_port` for data forwarding

5. **Agent (`AndGateAgent`)**
   - Extends `uvm_agent`
   - Contains driver, monitor, and sequencer
   - Connects components in `connect_phase`

6. **Environment (`AndGateEnv`)**
   - Extends `uvm_env`
   - Contains agent instances
   - Top-level verification environment

7. **Test (`AndGateTest`)**
   - Extends `uvm_test`
   - Top-level test class
   - Orchestrates test execution

**UVM Phases:**
- `build_phase()` - Component construction
- `connect_phase()` - Component connections
- `run_phase()` - Test execution
- `check_phase()` - Result verification

**Running the test:**

```bash
# Via module script
./scripts/module1.sh --pyuvm-tests

# Directly from test directory
cd module1/tests/pyuvm_tests
make SIM=verilator TEST=test_and_gate_uvm
```

**Expected Results:**
- 1 test case passing
- UVM phases executed successfully
- Transaction generation and processing demonstrated

**Note:** This test demonstrates the UVM architecture pattern. In a real implementation, the driver and monitor would interface with cocotb's DUT handles to drive and sample actual hardware signals.

## Running Examples and Tests

### Using the Module Script

The `module1.sh` script provides a convenient way to run all examples and tests:

```bash
# Run everything (Python examples + all tests)
./scripts/module1.sh

# Run only Python examples
./scripts/module1.sh --all-python

# Run only hardware tests
./scripts/module1.sh --skip-python

# Run specific Python examples
./scripts/module1.sh --python-basics
./scripts/module1.sh --decorators
./scripts/module1.sh --async-await
./scripts/module1.sh --data-structures
./scripts/module1.sh --error-handling

# Run specific test suites
./scripts/module1.sh --cocotb-tests
./scripts/module1.sh --pyuvm-tests
./scripts/module1.sh --all-tests

# Combine options
./scripts/module1.sh --python-basics --cocotb-tests
```

### Running Individual Tests

#### Direct Python Execution

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Python examples directly
python3 module1/examples/python_basics/transaction.py
python3 module1/examples/decorators/decorators_example.py
python3 module1/examples/async_await/async_example.py
python3 module1/examples/data_structures/data_structures_example.py
python3 module1/examples/error_handling/error_handling_example.py
```

#### Running cocotb Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module1/tests/cocotb_tests

# Run AND gate tests
make SIM=verilator TEST=test_and_gate

# Run counter tests
make SIM=verilator TEST=test_counter

# Run all tests
make test_all

# Clean build artifacts
make clean
```

#### Running pyuvm Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module1/tests/pyuvm_tests

# Run pyuvm AND gate test
make SIM=verilator TEST=test_and_gate_uvm

# Clean build artifacts
make clean
```

## Test Results

When tests complete successfully, you should see:

### cocotb Test Output

```
** TEST                                 STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** test_and_gate.test_and_gate_basic         PASS          50.00           0.00      89013.24  **
** test_and_gate.test_and_gate_truth_table   PASS          40.00           0.00     284842.38  **
** test_and_gate.test_and_gate_timing        PASS          15.00           0.00     110376.42  **
** TESTS=3 PASS=3 FAIL=0 SKIP=0                           105.00           0.00      51311.93  **
```

### Expected Test Counts

- **cocotb AND gate tests**: 3 tests
- **cocotb Counter tests**: 4 tests
- **pyuvm AND gate test**: 1 test
- **Total**: 8 hardware tests

## Troubleshooting

### Common Issues

#### 1. Verilator Version Error

**Error:** `cocotb requires Verilator 5.036 or later, but using 5.020`

**Solution:** Upgrade Verilator to 5.036 or later:

```bash
./scripts/install_verilator.sh --from-submodule --force
```

#### 2. Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'cocotb'`

**Solution:** Activate the virtual environment:

```bash
source .venv/bin/activate
```

#### 3. TOPLEVEL Mismatch

**Error:** `Can not find root handle 'and_gate'` or `Can not find root handle 'counter'`

**Solution:** Clean the build directory between tests with different TOPLEVELs:

```bash
cd module1/tests/cocotb_tests
make clean
make SIM=verilator TEST=test_and_gate
```

The module script automatically cleans between tests.

#### 4. Makefile Errors

**Error:** `target file 'clean' has both : and :: entries`

**Solution:** This should not occur as the Makefiles have been updated to remove duplicate clean targets.

#### 5. Build Failures

**Error:** Build errors in `sim_build/`

**Solution:** Clean and rebuild:

```bash
make clean
make SIM=verilator TEST=<test_name>
```

### Debugging Tips

1. **Check Verilator Version:**
   ```bash
   verilator --version
   ```

2. **Verify Virtual Environment:**
   ```bash
   which python3  # Should point to .venv/bin/python3
   python3 -c "import cocotb; import pyuvm"
   ```

3. **Check Build Directory:**
   ```bash
   ls -la module1/tests/cocotb_tests/sim_build/
   ```

4. **View Detailed Logs:**
   ```bash
   # Check log files created by module script
   tail -f /tmp/cocotb_and_gate.log
   tail -f /tmp/cocotb_counter.log
   tail -f /tmp/pyuvm_and_gate.log
   ```

5. **Run Tests with Verbose Output:**
   ```bash
   make SIM=verilator TEST=test_and_gate V=1
   ```

## Topics Covered

1. **Python Classes and Inheritance** - OOP fundamentals for verification data structures
2. **Decorators and Context Managers** - Python patterns for testbench automation
3. **Async/Await** - Asynchronous programming for simulation coroutines
4. **Verification Fundamentals** - Basic testbench concepts and structure
5. **Testbench Architecture** - DUT, stimulus generation, result checking
6. **Simulation Flow** - Time management and synchronization
7. **Assertions** - Property checking and validation
8. **Data Structures** - Collections optimized for verification (queues, scoreboards, coverage)
9. **Error Handling** - Exception management and structured logging
10. **cocotb Basics** - Writing cocotb testbenches
11. **pyuvm Basics** - UVM-style testbench architecture with pyuvm

## Next Steps

After completing Module 1, proceed to:

- **Module 2**: cocotb Fundamentals - Clock generation, reset patterns, signal access
- **Module 3**: UVM Concepts - Phases, factory, configuration database
- **Module 4**: UVM Components - Agents, sequencers, monitors, drivers

## Additional Resources

- [cocotb Documentation](https://docs.cocotb.org/)
- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [Verilator Documentation](https://verilator.org/)
- [Python Documentation](https://docs.python.org/3/)

## File Descriptions

### Examples

| File | Description |
|------|-------------|
| `transaction.py` | Base transaction class and inheritance examples |
| `decorators_example.py` | Decorators and context managers for verification |
| `async_example.py` | Async/await patterns for simulation |
| `data_structures_example.py` | Data structures for verification (queues, scoreboards, coverage) |
| `error_handling_example.py` | Exception handling and logging patterns |

### DUT Modules

| File | Description | Ports |
|------|-------------|-------|
| `and_gate.v` | 2-input AND gate | `a`, `b` (inputs), `y` (output) |
| `counter.v` | 8-bit up counter | `clk`, `rst_n`, `enable` (inputs), `count` (output) |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_and_gate.py` | cocotb | AND gate testbench | 3 test functions |
| `test_counter.py` | cocotb | Counter testbench | 4 test functions |
| `test_and_gate_uvm.py` | pyuvm | AND gate UVM testbench | 1 UVM test |

---

For questions or issues, refer to the main project README or check the test logs for detailed error messages.
