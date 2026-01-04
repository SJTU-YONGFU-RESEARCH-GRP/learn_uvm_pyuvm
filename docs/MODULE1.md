# Module 1: Python and Verification Basics

**Duration**: 2 weeks  
**Complexity**: Beginner  
**Goal**: Understand Python for verification and verification fundamentals

## Overview

This module establishes the foundation for verification work. You'll learn essential Python concepts used in verification and understand the fundamental principles of hardware verification.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module1/` directory:

```
module1/
├── examples/              # Python examples for each topic
│   ├── python_basics/     # Classes, inheritance, OOP
│   ├── decorators/        # Decorators and context managers
│   ├── async_await/       # Async/await patterns
│   ├── data_structures/   # Data structures for verification
│   └── error_handling/   # Exception handling and logging
├── dut/                   # Verilog Design Under Test modules
│   └── simple_gates/      # Basic gates (AND gate, Counter)
├── tests/                 # Testbenches
│   ├── cocotb_tests/     # cocotb testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── README.md             # Module 1 documentation
```

### Quick Start

**Run all examples using the orchestrator script:**
```bash
# Run all Python examples
./scripts/module1.sh

# Run specific examples
./scripts/module1.sh --python-basics
./scripts/module1.sh --decorators
./scripts/module1.sh --async-await
./scripts/module1.sh --data-structures
./scripts/module1.sh --error-handling

# Run tests
./scripts/module1.sh --cocotb-tests
./scripts/module1.sh --pyuvm-tests

# Run everything
./scripts/module1.sh --all-python --all-tests
```

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run Python examples directly
python3 module1/examples/python_basics/transaction.py
python3 module1/examples/decorators/decorators_example.py
python3 module1/examples/async_await/async_example.py
python3 module1/examples/data_structures/data_structures_example.py
python3 module1/examples/error_handling/error_handling_example.py

# Run cocotb tests
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
make SIM=verilator TEST=test_counter
```

## Topics Covered

### 1. Python Classes and Inheritance for Verification

- **Object-Oriented Programming Basics**
  - Classes and objects
  - Instance variables and methods
  - Class variables and methods
  - Encapsulation concepts

- **Inheritance in Python**
  - Single inheritance
  - Multiple inheritance (MRO)
  - Method overriding
  - `super()` function usage

- **Special Methods (Dunder Methods)**
  - `__init__()` for initialization
  - `__str__()` and `__repr__()` for string representation
  - `__eq__()` for equality comparison
  - `__hash__()` for hashable objects

- **Class Design Patterns for Verification**
  - Factory pattern basics
  - Singleton pattern
  - Builder pattern
  - Strategy pattern

#### Example 1.1: Transaction Classes (`module1/examples/python_basics/transaction.py`)

**What it demonstrates:**
- Base `Transaction` class with class variables (`_id_counter`)
- Instance variables (`id`, `data`, `timestamp`)
- Special methods: `__init__()`, `__str__()`, `__repr__()`, `__eq__()`, `__hash__()`
- Inheritance: `ReadTransaction` and `WriteTransaction` inherit from `Transaction`
- Method overriding: Child classes override `__str__()` method
- Using `super()` to call parent class methods

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --python-basics

# Or directly
python3 module1/examples/python_basics/transaction.py
```

**Expected Output:**
```
============================================================
Module 1 Example 1.1: Python Class Basics
============================================================

1. Creating base transaction:
   Transaction(id=1, data=4660, timestamp=0)
   Transaction ID: 1

2. Creating read transaction (inheritance):
   ReadTransaction(id=2, address=0x1000, data=0xDEAD)
   Address: 0x1000

3. Creating write transaction (inheritance):
   WriteTransaction(id=3, address=0x2000, data=0xBEEF)
   Address: 0x2000

4. Testing equality:
   txn1 == txn2: True
   txn1 == read_txn: False

5. Using transactions in a set (requires __hash__):
   Set size: 3
   - Transaction(id=1, data=4660, timestamp=0)
   - ReadTransaction(id=2, address=0x1000, data=0xDEAD)
   - WriteTransaction(id=3, address=0x2000, data=0xBEEF)

============================================================
Example completed successfully!
============================================================
```

**Key Concepts:**
- **Class Variables**: `_id_counter` is shared across all instances
- **Instance Variables**: Each transaction has its own `id`, `data`, `timestamp`
- **Special Methods**: Enable Pythonic behavior (string representation, equality, hashing)
- **Inheritance**: `ReadTransaction` and `WriteTransaction` extend base functionality
- **Method Overriding**: Child classes customize string representation

### 2. Decorators and Context Managers

- **Python Decorators**
  - Function decorators
  - Class decorators
  - Decorator syntax and usage
  - Common decorators (`@property`, `@staticmethod`, `@classmethod`)

- **Context Managers**
  - `with` statement
  - `__enter__()` and `__exit__()` methods
  - Context manager protocol
  - `contextlib` utilities

- **Verification-Specific Decorators**
  - cocotb decorators (`@cocotb.test()`, `@cocotb.coroutine`)
  - Custom decorators for verification
  - Timing decorators

#### Example 1.2: Decorators and Context Managers (`module1/examples/decorators/decorators_example.py`)

**What it demonstrates:**
- **Function Decorators**: `@timing_decorator` and `@log_calls_decorator` wrap functions
- **Decorator Stacking**: Multiple decorators can be applied to the same function
- **Context Manager Class**: `VerificationContext` implements `__enter__()` and `__exit__()`
- **Function-based Context Manager**: `simulation_phase()` using `@contextmanager`
- **Nested Context Managers**: Using multiple context managers together
- **Logging Integration**: Decorators and context managers use Python's logging module

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --decorators

# Or directly
python3 module1/examples/decorators/decorators_example.py
```

**Expected Output:**
```
============================================================
Module 1 Example 1.2: Decorators and Context Managers
============================================================

1. Using function decorators:
2024-01-04 10:00:00 - __main__ - INFO - Calling setup with args=(), kwargs={}
2024-01-04 10:00:00 - __main__ - INFO - Setting up test environment
2024-01-04 10:00:00 - __main__ - INFO - setup returned: None
2024-01-04 10:00:00 - __main__ - INFO - setup took 0.1000 seconds
...

2. Using context manager (class-based):
2024-01-04 10:00:01 - __main__ - INFO - Entering verification context: test_context
   Elapsed time: 0.1000s
2024-01-04 10:00:01 - __main__ - INFO - Exiting verification context: test_context (success, 0.1000s)

3. Using context manager (function-based):
2024-01-04 10:00:02 - __main__ - INFO - Starting simulation phase: reset_phase
2024-01-04 10:00:02 - __main__ - INFO -    Performing reset operations
2024-01-04 10:00:02 - __main__ - INFO - Completed simulation phase: reset_phase (0.0500s)
...

============================================================
Example completed successfully!
============================================================
```

**Key Concepts:**
- **Decorators**: Functions that modify other functions without changing their code
- **`functools.wraps`**: Preserves function metadata when decorating
- **Context Managers**: Ensure proper resource cleanup using `with` statements
- **Exception Handling**: Context managers can handle exceptions in `__exit__()`
- **Logging**: Integration with Python's logging module for verification workflows

### 3. Async/Await for Simulation

- **Asynchronous Programming Concepts**
  - Coroutines vs functions
  - Event loop basics
  - Concurrency vs parallelism

- **Python `async` and `await`**
  - Defining async functions
  - Awaiting coroutines
  - Async context managers
  - Async iterators

- **cocotb Coroutines**
  - cocotb coroutine concept
  - `await` for simulation time
  - Trigger objects
  - Coroutine scheduling

- **Common Patterns**
  - Parallel coroutines
  - Sequential execution
  - Timeout handling
  - Exception handling in async code

#### Example 1.3: Async/Await Patterns (`module1/examples/async_await/async_example.py`)

**What it demonstrates:**
- **Async Functions**: Defining coroutines with `async def`
- **Awaiting Operations**: Using `await` to wait for async operations
- **Clock Generation**: Simulating clock signals with async functions
- **Parallel Execution**: Running multiple coroutines concurrently with `asyncio.gather()`
- **Sequential Execution**: Running coroutines one after another
- **Timeout Handling**: Using `asyncio.wait_for()` with timeout
- **Exception Handling**: Catching exceptions in async code
- **Queues**: Using `asyncio.Queue` for communication between coroutines

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --async-await

# Or directly
python3 module1/examples/async_await/async_example.py
```

**Expected Output:**
```
============================================================
Module 1 Example 1.3: Async/Await for Simulation
============================================================

1. Sequential execution:
Running sequential execution example...
Final result: Step 1 complete, Step 2 complete, Step 3 complete

2. Parallel tasks:
Running parallel tasks example...
Results collected: [0, 2, 4, 6, 8]

3. Timeout handling:
Running timeout example...
Operation timed out!

4. Exception handling:
Running exception handling example...
Caught exception: Simulated error

============================================================
Example completed successfully!
============================================================
```

**Key Concepts:**
- **Coroutines**: Functions defined with `async def` that can be paused and resumed
- **Event Loop**: `asyncio.run()` creates and manages the event loop
- **Concurrency**: Multiple coroutines can run concurrently (not in parallel)
- **`asyncio.gather()`**: Runs multiple coroutines concurrently and waits for all
- **`asyncio.wait_for()`**: Adds timeout to coroutine execution
- **Async Queues**: `asyncio.Queue` for safe communication between coroutines
- **Simulation Time**: In cocotb, `await Timer()` advances simulation time

### 4. Verification Fundamentals

- **What is Verification?**
  - Design vs verification
  - Verification goals
  - Verification metrics
  - Verification lifecycle

- **Testbench Architecture**
  - Testbench components
  - Stimulus generation
  - Response checking
  - Coverage collection

- **Verification Levels**
  - Unit level verification
  - Block level verification
  - System level verification
  - SoC level verification

### 5. Testbench Architecture Basics

- **Testbench Structure**
  - Design Under Test (DUT)
  - Testbench components
  - Interface definition
  - Clock and reset generation

- **Stimulus Generation**
  - Deterministic stimulus
  - Random stimulus
  - Constrained random
  - Directed tests

- **Response Checking**
  - Self-checking testbenches
  - Reference models
  - Scoreboards
  - Assertions

### 6. Simulation Flow

- **Simulation Phases**
  - Initialization
  - Reset phase
  - Test execution
  - Cleanup phase

- **Time Management**
  - Simulation time vs real time
  - Time units (ns, ps, etc.)
  - Clock cycles
  - Timing relationships

- **Event-Driven Simulation**
  - Event scheduling
  - Delta cycles
  - Signal updates
  - Trigger conditions

### 7. Assertions Introduction

- **What are Assertions?**
  - Immediate assertions
  - Concurrent assertions
  - Assertion types

- **Basic Assertions**
  - Simple property checks
  - Signal value assertions
  - Timing assertions

- **Assertion Best Practices**
  - When to use assertions
  - Assertion placement
  - Assertion messages
  - Assertion coverage

### 8. Python Testing Frameworks (Overview)

- **pytest Basics**
  - Test discovery
  - Fixtures
  - Parametrization
  - Markers

- **Unit Testing Concepts**
  - Test organization
  - Test isolation
  - Mocking and stubbing
  - Test coverage

- **Integration with Verification**
  - Using pytest with cocotb
  - Test organization patterns
  - Reporting and logging

### 9. Data Structures for Verification

- **Lists and Dictionaries**
  - Common operations
  - List comprehensions
  - Dictionary comprehensions
  - Nested structures

- **Collections Module**
  - `deque` for queues
  - `defaultdict` for default values
  - `Counter` for counting
  - `namedtuple` for structured data

- **Verification-Specific Structures**
  - Transaction queues
  - Scoreboard data structures
  - Coverage data structures

#### Example 1.4: Data Structures (`module1/examples/data_structures/data_structures_example.py`)

**What it demonstrates:**
- **`deque`**: Double-ended queue for FIFO/LIFO operations in `TransactionQueue`
- **`defaultdict`**: Dictionary with default values for scoreboard
- **`Counter`**: Counting occurrences for statistics
- **`namedtuple`**: Structured data for transactions
- **List Comprehensions**: Creating lists from iterables
- **Dictionary Comprehensions**: Creating dictionaries from iterables
- **Scoreboard Pattern**: Comparing expected vs actual results
- **Coverage Collection**: Tracking coverage bins and hit counts

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --data-structures

# Or directly
python3 module1/examples/data_structures/data_structures_example.py
```

**Expected Output:**
```
============================================================
Module 1: Data Structures for Verification
============================================================

1. Transaction Queue (deque):
   Queue size: 5
   Popped: id=1, addr=0x1000, data=0x0
   Popped: id=2, addr=0x1001, data=0x2
   ...

2. Scoreboard (defaultdict, Counter):
   Matches: 5
   Mismatches: 0
   Unexpected: 2
   Mismatch details: []

3. Coverage Collector (set, Counter):
   address: 80.0% coverage
      Unique values: 8
      Total hits: 8
   data: 70.0% coverage
      Unique values: 7
      Total hits: 7
   ...

4. List Comprehensions:
   Created 10 transactions
   First transaction: Transaction(id=0, addr=4096, data=0, timestamp=0)

5. Dictionary Comprehensions:
   Created address map with 10 entries
   Sample: {4096: 0, 4097: 2, 4098: 4}

============================================================
Example completed successfully!
============================================================
```

**Key Concepts:**
- **`deque`**: Efficient FIFO/LIFO operations, thread-safe for async code
- **`defaultdict`**: Automatically creates default values for missing keys
- **`Counter`**: Specialized dictionary for counting occurrences
- **`namedtuple`**: Lightweight alternative to classes for simple data structures
- **Comprehensions**: Pythonic way to create lists/dicts from iterables
- **Scoreboard**: Common verification pattern for checking results
- **Coverage**: Tracking which values/conditions have been tested

### 10. Error Handling and Logging

- **Exception Handling**
  - Try/except blocks
  - Exception types
  - Custom exceptions
  - Exception chaining

- **Logging in Python**
  - `logging` module basics
  - Log levels
  - Log formatting
  - Log handlers

- **Verification Logging**
  - UVM reporting (preview)
  - Testbench logging patterns
  - Debug logging
  - Log analysis

#### Example 1.5: Error Handling and Logging (`module1/examples/error_handling/error_handling_example.py`)

**What it demonstrates:**
- **Custom Exceptions**: `VerificationError`, `MismatchError`, `TimeoutError`
- **Exception Handling**: Try/except blocks with specific exception types
- **Exception Chaining**: Using `raise ... from ...` to chain exceptions
- **Retry Logic**: Implementing retry mechanisms with error handling
- **Logging Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Handlers**: File and console handlers
- **Log Formatting**: Custom log message formats
- **Verification Statistics**: Tracking pass/fail/error counts

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --error-handling

# Or directly
python3 module1/examples/error_handling/error_handling_example.py
```

**Expected Output:**
```
============================================================
Module 1: Error Handling and Logging
============================================================

1. Basic Error Handling:
   ✓ Successful check passed
   ✓ Caught expected error: Mismatch at address 0x2000: expected 0x5678, got 0x9ABC
   Statistics: {'total': 2, 'pass': 1, 'fail': 1, 'error': 0, 'errors': 1}

2. Exception Chaining:
2024-01-04 10:00:00 - __main__ - ERROR - Caught chained exception: Verification failed
2024-01-04 10:00:00 - __main__ - ERROR - Original exception: Original error
   ✓ Exception chaining demonstrated

3. Retry Logic:
2024-01-04 10:00:01 - __main__ - WARNING - RetryChecker: Attempt 1 failed: ...
2024-01-04 10:00:01 - __main__ - WARNING - RetryChecker: Attempt 2 failed: ...
2024-01-04 10:00:01 - __main__ - INFO - RetryChecker: Operation succeeded on attempt 3
   ✓ Operation succeeded after 3 attempts

4. Logging Levels:
2024-01-04 10:00:02 - __main__ - DEBUG - This is a DEBUG message...
2024-01-04 10:00:02 - __main__ - INFO - This is an INFO message...
2024-01-04 10:00:02 - __main__ - WARNING - This is a WARNING message...
2024-01-04 10:00:02 - __main__ - ERROR - This is an ERROR message...
2024-01-04 10:00:02 - __main__ - CRITICAL - This is a CRITICAL message...
   ✓ Logging levels demonstrated (check verification.log)

============================================================
Example completed successfully!
============================================================
Check 'verification.log' for detailed logs
```

**Key Concepts:**
- **Custom Exceptions**: Create domain-specific exceptions for better error handling
- **Exception Chaining**: Preserve original exception context with `raise ... from ...`
- **Retry Logic**: Implement robust error recovery mechanisms
- **Logging Levels**: Use appropriate levels (DEBUG < INFO < WARNING < ERROR < CRITICAL)
- **Log Handlers**: Multiple handlers (file, console) for different outputs
- **Log Formatting**: Customize log message format with timestamps, levels, etc.
- **Verification Statistics**: Track test results and errors for reporting

## Learning Outcomes

By the end of this module, you should be able to:

- Write Python classes with inheritance
- Use decorators and context managers effectively
- Understand and use async/await for simulation
- Explain verification fundamentals
- Understand testbench architecture
- Comprehend simulation flow
- Write basic assertions
- Use Python testing frameworks
- Handle errors and implement logging

## Test Cases

### Test Case 1.1: Python Class Basics
**Objective**: Create a simple transaction class with inheritance

**Topics**:
- Class definition
- Instance variables
- Methods
- Inheritance

### Test Case 1.2: Decorators and Async
**Objective**: Use decorators and async functions

**Topics**:
- Function decorators
- Async function definition
- Await usage

### Test Case 1.3: Simple Verification Test
**Objective**: Create a basic verification testbench

**Topics**:
- Testbench structure
- Clock generation
- Signal driving
- Basic checking

#### cocotb Test: AND Gate (`module1/tests/cocotb_tests/test_and_gate.py`)

**What it demonstrates:**
- **Test Structure**: Using `@cocotb.test()` decorator
- **Signal Access**: Reading and writing DUT signals (`dut.a`, `dut.b`, `dut.y`)
- **Timing Control**: Using `await Timer()` for simulation time
- **Assertions**: Python assertions for checking results
- **Test Cases**: Multiple test functions for different scenarios
- **Truth Table Testing**: Systematic testing of all input combinations

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --cocotb-tests

# Or manually
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_and_gate_basic (1/3)
     0.00ns INFO     cocotb.regression                  Running test_and_gate_truth_table (2/3)
     0.00ns INFO     cocotb.regression                  Running test_and_gate_timing (3/3)
     0.00ns INFO     cocotb.regression                  test_and_gate passed
```

**Key Concepts:**
- **`@cocotb.test()`**: Decorator marks function as a test
- **DUT Access**: `dut.signal_name.value` to read/write signals
- **`Timer()`**: Advances simulation time
- **Assertions**: Python `assert` statements for checking
- **Test Organization**: Multiple test functions in one file

#### cocotb Test: Counter (`module1/tests/cocotb_tests/test_counter.py`)

**What it demonstrates:**
- **Clock Generation**: Creating clock signal with `generate_clock()` coroutine
- **Reset Sequence**: Implementing reset with proper timing
- **Sequential Logic Testing**: Testing clocked (sequential) circuits
- **Enable Control**: Testing enable/disable functionality
- **Edge Detection**: Using `RisingEdge()` trigger
- **Multiple Test Scenarios**: Reset, increment, enable, overflow tests

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --cocotb-tests

# Or manually
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_counter
```

**Expected Output:**
```
     0.00ns INFO     cocotb.regression                  Running test_counter_reset (1/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_increment (2/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_enable (3/4)
     0.00ns INFO     cocotb.regression                  Running test_counter_overflow (4/4)
     0.00ns INFO     cocotb.regression                  test_counter passed
```

**Key Concepts:**
- **Clock Generation**: Background coroutine for clock signal
- **`cocotb.start_soon()`**: Start background coroutines
- **`RisingEdge()`**: Wait for clock edge
- **Reset Timing**: Proper reset sequence with timing
- **Sequential Testing**: Testing state machines and counters

#### pyuvm Test: AND Gate (`module1/tests/pyuvm_tests/test_and_gate_uvm.py`)

**What it demonstrates:**
- **UVM Test Structure**: `@uvm_test()` decorator
- **UVM Phases**: `build_phase()`, `run_phase()`, `check_phase()`
- **UVM Components**: `uvm_test`, `uvm_env`, `uvm_agent`, `uvm_driver`, `uvm_monitor`
- **UVM Sequences**: `uvm_sequence` and `uvm_sequence_item`
- **UVM Reporting**: Using `self.logger` for messages
- **Objections**: Using `raise_objection()` and `drop_objection()` for test control

**Execution:**
```bash
# Using orchestrator script
./scripts/module1.sh --pyuvm-tests

# Or manually
cd module1/tests/pyuvm_tests
make SIM=verilator TEST=test_and_gate_uvm
```

**Note**: This is a structural example showing UVM patterns. Full integration with cocotb requires additional setup.

**Key Concepts:**
- **UVM Phases**: Build, connect, run, check phases
- **Component Hierarchy**: Test → Environment → Agent → Driver/Monitor
- **Sequences**: Generate and send transactions
- **Objections**: Control test execution duration
- **Factory Pattern**: UVM uses factory for component creation

## Exercises

1. **Class Design**
   - Create a base transaction class
   - Derive specific transaction types
   - Implement comparison methods
   - **Location**: Extend `module1/examples/python_basics/transaction.py`
   - **Hint**: Add a `WriteReadTransaction` class that combines both operations

2. **Async Patterns**
   - Create multiple parallel coroutines
   - Implement timeout handling
   - Handle exceptions in async code
   - **Location**: Extend `module1/examples/async_await/async_example.py`
   - **Hint**: Create a monitor that times out if no data arrives

3. **Testbench Structure**
   - Design a simple testbench
   - Implement clock and reset
   - Create basic stimulus
   - **Location**: Create new test in `module1/tests/cocotb_tests/`
   - **Hint**: Test the counter with different enable patterns

4. **Assertions**
   - Add assertions to testbench
   - Test assertion behavior
   - Understand assertion messages
   - **Location**: Add to existing tests in `module1/tests/cocotb_tests/`
   - **Hint**: Add assertions for timing constraints

5. **Logging**
   - Implement logging in testbench
   - Use different log levels
   - Format log messages
   - **Location**: Extend `module1/examples/error_handling/error_handling_example.py`
   - **Hint**: Create a custom log formatter for verification messages

## Assessment

- [ ] Can write Python classes with inheritance
- [ ] Understands decorators and context managers
- [ ] Can use async/await effectively
- [ ] Understands verification fundamentals
- [ ] Can explain testbench architecture
- [ ] Understands simulation flow
- [ ] Can write basic assertions
- [ ] Can use Python testing frameworks
- [ ] Can handle errors and implement logging

## Next Steps

After completing this module, proceed to [Module 2: cocotb Fundamentals](MODULE2.md) to learn how to use cocotb for hardware verification.

## Additional Resources

- **Python Official Tutorial**: https://docs.python.org/3/tutorial/
- **Real Python Async Guide**: https://realpython.com/async-io-python/
- **pytest Documentation**: https://docs.pytest.org/
- **Python Logging Guide**: https://docs.python.org/3/howto/logging.html

## Troubleshooting

### Common Issues

**Issue: Virtual environment not found**
```bash
# Solution: Create virtual environment first
python3 -m venv .venv
source .venv/bin/activate
./scripts/module0.sh  # Install dependencies
```

**Issue: cocotb tests fail with "simulator not found"**
```bash
# Solution: Verify Verilator is installed
verilator --version
# If not installed, run:
./scripts/install_verilator.sh --from-submodule
```

**Issue: Import errors in Python examples**
```bash
# Solution: Ensure you're using the correct Python environment
source .venv/bin/activate  # If using venv
python3 --version  # Should be 3.8+
```

**Issue: Makefile errors when running tests**
```bash
# Solution: Ensure cocotb is properly installed
python3 -c "import cocotb; print(cocotb.__version__)"
# Check Makefile paths are correct
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module1/README.md` for directory structure
- Run examples individually to isolate issues
- Check log files (e.g., `verification.log` for error handling example)

