gst# Module 8: Advanced UVM Utilities

This directory contains all examples, exercises, and test cases for Module 8, focusing on advanced UVM utilities including command-line processing, comparators, recorders, pools, queues, and utility functions for strings, math, and random number generation.

## Directory Structure

```
module8/
├── examples/              # pyuvm examples for each topic
│   ├── clp/              # Command Line Processor examples
│   │   └── clp_example.py
│   ├── comparators/      # Comparator examples
│   │   └── comparator_example.py
│   ├── recorders/        # Recorder examples
│   │   └── recorder_example.py
│   ├── pools/            # Pool examples
│   │   └── pool_example.py
│   ├── queues/           # Queue examples
│   │   └── queue_example.py
│   ├── string_utils/     # String utility examples
│   │   └── string_utils_example.py
│   ├── math_utils/       # Math utility examples
│   │   └── math_utils_example.py
│   ├── random_utils/     # Random utility examples
│   │   └── random_utils_example.py
│   └── integration/      # Utility integration examples
│       └── integration_example.py
├── dut/                   # Verilog Design Under Test modules
│   └── dma/              # DMA controller
│       └── simple_dma.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
│       └── test_utilities.py
└── exercises/            # Exercise solutions (if any)
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

## Advanced UVM Utility Examples

### 1. Command Line Processor (CLP) (`examples/clp/clp_example.py`)

Demonstrates using command-line arguments for test configuration:

**Key Concepts:**
- Command-line argument parsing
- Test configuration via command line
- Parameter passing from command line
- Test mode selection
- Seed and debug level configuration

**CLP Components:**

1. **CLPEnv**
   - Environment demonstrating CLP usage
   - Parses command-line arguments using `get_clp_arg()`
   - Configures test based on command-line parameters
   - Supports test mode, debug level, transaction count, and seed

2. **get_clp_arg() Method**
   - Gets command-line argument values
   - Supports `+arg_name=value` format
   - Supports `+arg_name` boolean flags
   - Returns default value if argument not found
   - Simulates UVM CLP behavior in Python

**CLP Usage:**

**Command-Line Arguments:**
```bash
# Run with command-line arguments
make SIM=verilator TEST=clp_example EXTRA_ARGS="+test_mode=stress +debug_level=3 +num_transactions=100 +seed=42"
```

**Argument Format:**
- `+test_mode=normal` - Test mode parameter
- `+debug_level=2` - Debug level parameter
- `+num_transactions=50` - Number of transactions parameter
- `+seed=123` - Random seed parameter

**CLP Configuration:**
```python
# Get command-line arguments
self.test_mode = self.get_clp_arg("+test_mode", "normal")
self.debug_level = int(self.get_clp_arg("+debug_level", "0"))
self.num_transactions = int(self.get_clp_arg("+num_transactions", "10"))
self.seed = int(self.get_clp_arg("+seed", "0"))
```

**Running the example:**

```bash
# Via module script
./scripts/module8.sh --clp

# Or directly from example directory
cd module8/examples/clp
make SIM=verilator TEST=clp_example EXTRA_ARGS="+test_mode=stress +num_transactions=20"
```

**Expected Output:**
- Command-line argument parsing
- Test configuration from command line
- Parameter usage in test execution
- Test mode selection

### 2. Comparators (`examples/comparators/comparator_example.py`)

Demonstrates using comparators for transaction comparison in scoreboards:

**Key Concepts:**
- In-order transaction comparison
- Out-of-order transaction comparison
- Transaction matching algorithms
- Comparator statistics and reporting

**Comparator Components:**

1. **InOrderComparator**
   - Compares transactions in arrival order
   - Matches expected and actual transactions sequentially
   - Reports matches and mismatches
   - Tracks comparison statistics

2. **OutOfOrderComparator**
   - Compares transactions without requiring order
   - Uses matching algorithms (e.g., by address, by data)
   - Handles out-of-order transaction arrival
   - Reports matches and mismatches

3. **ComparatorTransaction**
   - Transaction for comparator example
   - Supports equality comparison via `__eq__()`
   - Supports hash for use in sets/dicts via `__hash__()`
   - Contains data, address, and timestamp fields

**Comparator Types:**

**In-Order Comparison:**
- Expected and actual must arrive in same order
- First expected matches first actual
- Simple FIFO matching algorithm

**Out-of-Order Comparison:**
- Expected and actual can arrive in any order
- Matching by key fields (e.g., address, data)
- More complex matching algorithm

**Comparator Usage:**
```python
# Create comparator
comparator = InOrderComparator.create("comparator", self)

# Connect expected and actual subscribers
monitor_expected.ap.connect(comparator.expected_subscriber.analysis_export)
monitor_actual.ap.connect(comparator.actual_subscriber.analysis_export)

# Comparator automatically compares transactions
```

**Running the example:**

```bash
./scripts/module8.sh --comparators
# or
cd module8/examples/comparators
make SIM=verilator TEST=comparator_example
```

**Expected Output:**
- Transaction comparison demonstration
- Match and mismatch detection
- Comparator statistics reporting
- In-order and out-of-order comparison

### 3. Recorders (`examples/recorders/recorder_example.py`)

Demonstrates transaction recording for analysis:

**Key Concepts:**
- Text file recording
- JSON file recording
- Transaction database storage
- Recording format and structure
- Post-simulation analysis

**Recorder Components:**

1. **TextRecorder**
   - Records transactions to text file
   - Human-readable format
   - Timestamp for each transaction
   - Simple file-based storage

2. **JSONRecorder**
   - Records transactions to JSON file
   - Machine-readable format
   - Structured data storage
   - Easy parsing and analysis

3. **TransactionDatabase**
   - In-memory transaction database
   - Stores transactions for querying
   - Supports filtering and searching
   - Post-simulation analysis

**Recording Formats:**

**Text Format:**
```
Transaction Recording Started: 2024-01-01 10:00:00
============================================================
[2024-01-01 10:00:01.123456] id=1, data=0xAA, addr=0x1000, ts=100
[2024-01-01 10:00:02.234567] id=2, data=0xBB, addr=0x2000, ts=200
============================================================
Transaction Recording Ended: 2024-01-01 10:00:05
Total transactions recorded: 2
```

**JSON Format:**
```json
{
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T10:00:05",
  "total_transactions": 2,
  "transactions": [
    {
      "transaction_id": 1,
      "data": "0xaa",
      "address": "0x1000",
      "timestamp": 100,
      "record_time": "2024-01-01T10:00:01.123456"
    }
  ]
}
```

**Running the example:**

```bash
./scripts/module8.sh --recorders
# or
cd module8/examples/recorders
make SIM=verilator TEST=recorder_example
```

**Expected Output:**
- Transaction recording to files
- Text and JSON format recording
- Database storage and querying
- Recording statistics

### 4. Pools (`examples/pools/pool_example.py`)

Demonstrates object pooling for performance optimization:

**Key Concepts:**
- Object reuse patterns
- Memory allocation optimization
- Pool size configuration
- Allocation and deallocation tracking
- Performance benefits

**Pool Components:**

1. **TransactionPool**
   - Object pool for transaction reuse
   - Pre-allocates pool of objects
   - Reduces memory allocation overhead
   - Tracks allocation and reuse statistics

2. **PoolTransaction**
   - Transaction with `reset()` method
   - Supports reuse after reset
   - Resets all fields to initial state

**Pool Operations:**

**Allocation:**
```python
# Get transaction from pool
txn = pool.get()  # Reuses existing or creates new
```

**Deallocation:**
```python
# Return transaction to pool
pool.put(txn)  # Resets and returns to pool
```

**Pool Benefits:**
- Reduces memory allocation overhead
- Improves performance by reusing objects
- Configurable pool size
- Tracks reuse statistics

**Running the example:**

```bash
./scripts/module8.sh --pools
# or
cd module8/examples/pools
make SIM=verilator TEST=pool_example
```

**Expected Output:**
- Object pool creation and management
- Allocation and deallocation demonstration
- Reuse statistics reporting
- Performance optimization benefits

### 5. Queues (`examples/queues/queue_example.py`)

Demonstrates queue data structures for transaction management:

**Key Concepts:**
- FIFO queue operations
- Priority queue support
- Queue size management
- Overflow handling
- Queue statistics

**Queue Components:**

1. **TransactionQueue**
   - FIFO queue for transactions
   - Uses Python's `deque` for efficiency
   - Supports maximum size configuration
   - Tracks queue statistics

2. **QueueTransaction**
   - Transaction with priority field
   - Supports priority-based ordering
   - Contains data, address, and priority

**Queue Operations:**

**Push:**
```python
# Add item to queue
queue.push(item)  # Returns True if added, False if overflow
```

**Pop:**
```python
# Remove and return item from queue
item = queue.pop()  # Returns None if empty
```

**Queue Types:**

**FIFO Queue:**
- First In, First Out
- Standard queue behavior
- Sequential processing

**Priority Queue:**
- Items ordered by priority
- Higher priority processed first
- More complex ordering

**Running the example:**

```bash
./scripts/module8.sh --queues
# or
cd module8/examples/queues
make SIM=verilator TEST=queue_example
```

**Expected Output:**
- Queue creation and management
- Push and pop operations
- Queue size tracking
- Overflow handling demonstration

### 6. String Utilities (`examples/string_utils/string_utils_example.py`)

Demonstrates string manipulation utilities for UVM:

**Key Concepts:**
- String formatting and conversion
- Hex and binary conversion
- Path manipulation
- String comparison
- Transaction string representation

**String Utilities:**

1. **String Formatting:**
   - Hex formatting: `f"0x{data:04X}"`
   - Binary formatting: `bin(data)`
   - Custom format strings

2. **String Conversion:**
   - `hex()` - Convert to hex string
   - `bin()` - Convert to binary string
   - `str()` - Convert to string

3. **Path Manipulation:**
   - `split('/')` - Split path components
   - `join()` - Join path components
   - Basename and dirname extraction

4. **String Comparison:**
   - Case-sensitive comparison
   - Case-insensitive comparison
   - Pattern matching

**String Utility Usage:**
```python
# Formatting
formatted = f"data=0x{data:04X}, addr=0x{addr:04X}"

# Conversion
hex_str = hex(data)
bin_str = bin(data)

# Path manipulation
basename = path.split('/')[-1]
dirname = '/'.join(path.split('/')[:-1])

# Transaction string representation
txn_str = ", ".join([f"{k}=0x{v:04X}" if isinstance(v, int) else f"{k}={v}" 
                     for k, v in txn_data.items()])
```

**Running the example:**

```bash
./scripts/module8.sh --string-utils
# or
cd module8/examples/string_utils
make SIM=verilator TEST=string_utils_example
```

**Expected Output:**
- String formatting and conversion
- Path manipulation demonstration
- String comparison examples
- Transaction string representation

### 7. Math Utilities (`examples/math_utils/math_utils_example.py`)

Demonstrates mathematical utilities for UVM:

**Key Concepts:**
- Random number generation
- Statistical functions
- Mathematical operations
- Bit manipulation
- Range operations

**Math Utilities:**

1. **Random Number Generation:**
   - `random.randint()` - Random integer
   - `random.random()` - Random float
   - Seed configuration

2. **Statistical Functions:**
   - `statistics.mean()` - Mean value
   - `statistics.median()` - Median value
   - `statistics.stdev()` - Standard deviation

3. **Bit Manipulation:**
   - Bit extraction: `(value >> bit) & 1`
   - Bit setting: `value | (1 << bit)`
   - Bit clearing: `value & ~(1 << bit)`

4. **Range Operations:**
   - `min()` - Minimum value
   - `max()` - Maximum value
   - Range calculation

**Math Utility Usage:**
```python
# Random number generation
random.seed(42)
rand_int = random.randint(0, 100)
rand_float = random.random()

# Statistical functions
mean_val = statistics.mean(data)
median_val = statistics.median(data)
stdev_val = statistics.stdev(data)

# Bit manipulation
bit_value = (value >> 8) & 1
set_bit = value | (1 << 4)
clear_bit = value & ~(1 << 4)
```

**Running the example:**

```bash
./scripts/module8.sh --math-utils
# or
cd module8/examples/math_utils
make SIM=verilator TEST=math_utils_example
```

**Expected Output:**
- Random number generation demonstration
- Statistical function usage
- Bit manipulation examples
- Range operation demonstration

### 8. Random Utilities (`examples/random_utils/random_utils_example.py`)

Demonstrates random number generation and constrained randomization:

**Key Concepts:**
- Transaction randomization
- Constrained randomization
- Seed management
- Random sequence generation
- Reproducible randomness

**Random Utilities:**

1. **RandomTransaction**
   - Transaction with random fields
   - `randomize()` method for randomization
   - `randomize_constrained()` for constrained randomization
   - Supports seed configuration

2. **RandomSequence**
   - Sequence generating random transactions
   - Configurable seed
   - Generates multiple random transactions

3. **ConstrainedRandomSequence**
   - Sequence with constrained randomization
   - Configurable constraints (min/max values)
   - Controlled randomness

**Randomization Methods:**

**Basic Randomization:**
```python
txn = RandomTransaction()
txn.randomize()  # Randomize all fields
```

**Constrained Randomization:**
```python
txn = RandomTransaction()
txn.randomize_constrained(
    data_min=0x00, data_max=0xFF,
    addr_min=0x0000, addr_max=0xFFFF,
    length_min=1, length_max=256
)
```

**Seed Configuration:**
```python
# Set seed for reproducibility
random.seed(42)

# Or pass seed to randomize
txn.randomize(seed=42)
```

**Running the example:**

```bash
./scripts/module8.sh --random-utils
# or
cd module8/examples/random_utils
make SIM=verilator TEST=random_utils_example
```

**Expected Output:**
- Transaction randomization demonstration
- Constrained randomization examples
- Seed management and reproducibility
- Random sequence generation

### 9. Utility Integration (`examples/integration/integration_example.py`)

Demonstrates integrating multiple utilities in a testbench:

**Key Concepts:**
- Combining multiple utilities
- Utility interaction patterns
- Integrated testbench design
- Utility coordination

**Integration Components:**

1. **Combined Utilities:**
   - CLP for configuration
   - Pools for object reuse
   - Queues for transaction management
   - Comparators for verification
   - Recorders for analysis

2. **Integration Patterns:**
   - Utility initialization
   - Utility coordination
   - Data flow between utilities
   - Utility reporting

**Integration Example:**
```python
# Initialize utilities
pool = TransactionPool.create("pool", self, pool_size=10)
queue = TransactionQueue.create("queue", self, max_size=100)
comparator = InOrderComparator.create("comparator", self)
recorder = TextRecorder.create("recorder", self, filename="transactions.txt")

# Use utilities together
txn = pool.get()  # Get from pool
queue.push(txn)   # Add to queue
txn_processed = queue.pop()  # Process from queue
recorder.write(txn_processed)  # Record transaction
```

**Running the example:**

```bash
./scripts/module8.sh --integration
# or
cd module8/examples/integration
make SIM=verilator TEST=integration_example
```

**Expected Output:**
- Multiple utility integration
- Utility interaction demonstration
- Coordinated utility usage
- Integrated testbench operation

## Design Under Test (DUT)

### Simple DMA Controller (`dut/dma/simple_dma.v`)

A simple DMA controller for verification utilities examples. This is the same DUT used in Module 7.

**Module Interface:**
```verilog
module simple_dma (
    input  wire        clk,            // Clock signal
    input  wire        rst_n,          // Active-low reset
    input  wire        dma_start,      // Start DMA transfer
    output reg         dma_done,       // DMA transfer complete
    input  wire [31:0] dma_src_addr,   // Source address (32-bit)
    input  wire [31:0] dma_dst_addr,   // Destination address (32-bit)
    input  wire [15:0] dma_length,     // Transfer length (16-bit)
    input  wire [2:0]  dma_channel     // DMA channel select (3-bit)
);
```

**Functionality:**
- Configurable source and destination addresses
- Variable transfer length
- Multiple channel support
- Transfer start and completion indication
- Transfer counter for progress tracking

**Note:** This DUT is primarily used for utility demonstration purposes. The utilities can be applied to any DUT or testbench.

## Testbenches

### pyuvm Tests (`tests/pyuvm_tests/`)

#### Utilities Test (`test_utilities.py`)

Complete UVM testbench demonstrating utility usage:

**UVM Components:**

1. **Transaction (`UtilitiesTransaction`)**
   - Contains `data` and `address` fields
   - Used for utility demonstration

2. **Sequence (`UtilitiesSequence`)**
   - Generates test transactions
   - Creates comprehensive test vectors

3. **Driver (`UtilitiesDriver`)**
   - Receives transactions from sequencer
   - Drives DUT inputs

4. **Monitor (`UtilitiesMonitor`)**
   - Samples DUT outputs
   - Creates transactions from sampled data
   - Broadcasts via analysis port

5. **Scoreboard (`UtilitiesScoreboard`)**
   - Extends `uvm_subscriber`
   - Receives transactions from monitor
   - Tracks received transactions

6. **Agent (`UtilitiesAgent`)**
   - Contains driver, monitor, and sequencer
   - Connects components

7. **Environment (`UtilitiesEnv`)**
   - Contains agent and scoreboard
   - Connects monitor to scoreboard

8. **Test (`UtilitiesTest`)**
   - Top-level test class
   - Creates environment and runs test
   - Starts sequence and checks results

**Test Flow:**
1. `build_phase()` - Create all components
2. `connect_phase()` - Connect components
3. `run_phase()` - Start sequence, generate transactions
4. `check_phase()` - Verify results
5. `report_phase()` - Generate test report

**Running the test:**

```bash
# Via module script
./scripts/module8.sh --pyuvm-tests

# Directly from test directory
cd module8/tests/pyuvm_tests
make SIM=verilator TEST=test_utilities
```

**Expected Results:**
- 1 test case passing
- All components created and connected
- Sequence execution demonstrated
- Scoreboard tracking demonstrated
- Utility concepts integrated

## Running Examples and Tests

### Using the Module Script

The `module8.sh` script provides a convenient way to run all examples and tests:

```bash
# Run everything (all examples + all tests)
./scripts/module8.sh

# Run only examples
./scripts/module8.sh --all-examples

# Run only tests
./scripts/module8.sh --pyuvm-tests

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

# Combine options
./scripts/module8.sh --clp --comparators --pyuvm-tests
```

### Running Individual Examples

#### Direct Execution from Example Directory

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to example directory
cd module8/examples/clp

# Run example
make SIM=verilator TEST=clp_example

# Clean build artifacts
make clean
```

#### Running All Examples Sequentially

```bash
cd module8/examples

# CLP
cd clp && make SIM=verilator TEST=clp_example && cd ..

# Comparators
cd comparators && make SIM=verilator TEST=comparator_example && cd ..

# Recorders
cd recorders && make SIM=verilator TEST=recorder_example && cd ..

# Pools
cd pools && make SIM=verilator TEST=pool_example && cd ..

# Queues
cd queues && make SIM=verilator TEST=queue_example && cd ..

# String utils
cd string_utils && make SIM=verilator TEST=string_utils_example && cd ..

# Math utils
cd math_utils && make SIM=verilator TEST=math_utils_example && cd ..

# Random utils
cd random_utils && make SIM=verilator TEST=random_utils_example && cd ..

# Integration
cd integration && make SIM=verilator TEST=integration_example && cd ..
```

### Running pyuvm Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module8/tests/pyuvm_tests

# Run test
make SIM=verilator TEST=test_utilities

# Clean build artifacts
make clean
```

## Test Results

When tests complete successfully, you should see output similar to:

### Example Test Output

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** clp_example.test_clp                           PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Expected Test Counts

- **CLP example**: 1 test
- **Comparators example**: 1 test
- **Recorders example**: 1 test
- **Pools example**: 1 test
- **Queues example**: 1 test
- **String utils example**: 1 test
- **Math utils example**: 1 test
- **Random utils example**: 1 test
- **Integration example**: 1 test
- **Utilities test**: 1 test
- **Total**: 10 tests across all examples and testbenches

## Troubleshooting

### Common Issues

#### 1. Verilator Version Error

**Error:** `cocotb requires Verilator 5.036 or later, but using 5.020`

**Solution:** Upgrade Verilator to 5.036 or later:

```bash
./scripts/install_verilator.sh --from-submodule --force
```

#### 2. Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'pyuvm'` or `ModuleNotFoundError: No module named 'cocotb'`

**Solution:** Activate the virtual environment:

```bash
source .venv/bin/activate
```

#### 3. CLP Argument Parsing Issues

**Error:** Command-line arguments not recognized

**Solution:**
- Verify argument format: `+arg_name=value` or `+arg_name`
- Check argument names match exactly
- Ensure `EXTRA_ARGS` is passed to Makefile
- Verify `get_clp_arg()` implementation

#### 4. Comparator Mismatch Issues

**Error:** Comparators report unexpected mismatches

**Solution:**
- Verify transaction `__eq__()` method implementation
- Check comparison logic in comparator
- Ensure expected and actual transactions have same type
- Verify transaction field matching criteria

#### 5. Recorder File Issues

**Error:** Recorded files not created or corrupted

**Solution:**
- Verify file path permissions
- Check file open/close operations
- Ensure proper JSON formatting
- Verify transaction `to_dict()` method

#### 6. Pool Allocation Issues

**Error:** Pool allocation fails or leaks

**Solution:**
- Verify pool size is sufficient
- Check `get()` and `put()` are paired correctly
- Ensure `reset()` method clears all fields
- Monitor pool allocation statistics

#### 7. Queue Overflow Issues

**Error:** Queue overflow warnings

**Solution:**
- Increase queue maximum size
- Verify items are popped from queue
- Check queue processing rate
- Monitor queue statistics

### Debugging Tips

1. **Check CLP Arguments:**
   ```python
   # Verify argument parsing
   self.logger.info(f"CLP args: test_mode={self.test_mode}, num_txns={self.num_transactions}")
   ```

2. **Monitor Comparator Operations:**
   ```python
   # Add logging in comparator
   self.logger.info(f"Comparing: expected={exp_txn}, actual={act_txn}")
   ```

3. **Check Recorder Status:**
   ```python
   # Verify recording
   self.logger.info(f"Recorded {self.recorded_count} transactions")
   ```

4. **Inspect Pool Statistics:**
   ```python
   # Check pool usage
   self.logger.info(f"Pool: allocated={self.allocated_count}, reused={self.reused_count}")
   ```

5. **Monitor Queue Status:**
   ```python
   # Check queue size
   self.logger.info(f"Queue: size={queue.size()}, added={queue.added_count}, removed={queue.removed_count}")
   ```

## Topics Covered

1. **Command Line Processor** - CLP argument parsing, test configuration
2. **Comparators** - In-order and out-of-order transaction comparison
3. **Recorders** - Text, JSON, and database transaction recording
4. **Pools** - Object pooling for performance optimization
5. **Queues** - FIFO and priority queue data structures
6. **String Utilities** - String formatting, conversion, and manipulation
7. **Math Utilities** - Random numbers, statistics, bit manipulation
8. **Random Utilities** - Constrained randomization, seed management
9. **Utility Integration** - Combining multiple utilities in testbenches
10. **Performance Optimization** - Utility-based testbench optimization

## Next Steps

After completing Module 8, you have completed the full UVM/PyUVM learning path!

**Recommended Next Steps:**
- Review all modules and consolidate learning
- Build a complete verification project using all concepts
- Explore advanced topics in pyuvm documentation
- Contribute to open-source UVM/PyUVM projects

## Additional Resources

- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [UVM User's Guide](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [Python Documentation](https://docs.python.org/3/)
- [cocotb Documentation](https://docs.cocotb.org/)
- [Verilator Documentation](https://verilator.org/)

## File Descriptions

### Examples

| File | Description | Tests |
|------|-------------|-------|
| `clp_example.py` | Command-line processor demonstration | 1 test function |
| `comparator_example.py` | Transaction comparator demonstration | 1 test function |
| `recorder_example.py` | Transaction recorder demonstration | 1 test function |
| `pool_example.py` | Object pool demonstration | 1 test function |
| `queue_example.py` | Queue data structure demonstration | 1 test function |
| `string_utils_example.py` | String utility demonstration | 1 test function |
| `math_utils_example.py` | Math utility demonstration | 1 test function |
| `random_utils_example.py` | Random utility demonstration | 1 test function |
| `integration_example.py` | Utility integration demonstration | 1 test function |

### DUT Modules

| File | Description | Ports |
|------|-------------|-------|
| `simple_dma.v` | Simple DMA controller | `clk`, `rst_n`, `dma_start`, `dma_done`, `dma_src_addr[31:0]`, `dma_dst_addr[31:0]`, `dma_length[15:0]`, `dma_channel[2:0]` |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_utilities.py` | pyuvm | Utilities testbench | 1 UVM test |

---

For questions or issues, refer to the main project README or check the test logs for detailed error messages.
