# Module 5: Advanced UVM Concepts

This directory contains all examples, exercises, and test cases for Module 5, focusing on advanced UVM concepts including virtual sequences, coverage models, complex configuration, callbacks, and register models.

## Directory Structure

```
module5/
├── examples/              # pyuvm examples for each topic
│   ├── virtual_sequences/ # Virtual sequence examples
│   │   └── virtual_sequence_example.py
│   ├── coverage/          # Coverage model examples
│   │   └── coverage_example.py
│   ├── configuration/     # Configuration object examples
│   │   └── configuration_example.py
│   ├── callbacks/         # Callback examples
│   │   └── callback_example.py
│   └── register_model/    # Register model examples
│       └── register_model_example.py
├── dut/                   # Verilog Design Under Test modules
│   └── advanced/          # Advanced modules for testing
│       └── multi_channel.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
│       └── test_advanced_uvm.py
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

## Advanced UVM Examples

### 1. Virtual Sequences (`examples/virtual_sequences/virtual_sequence_example.py`)

Demonstrates virtual sequencer and virtual sequence coordination:

**Key Concepts:**
- Virtual sequencer containing references to multiple sequencers
- Virtual sequence coordinating sequences on different sequencers
- Parallel sequence execution using `cocotb.start_soon()`
- Sequential sequence execution
- Sequence synchronization

**Virtual Sequence Components:**

1. **VirtualSequencer**
   - Extends `uvm_sequencer`
   - Contains references to multiple sequencers (`master_seqr`, `slave_seqr`)
   - References set in `connect_phase()` from environment
   - No transactions of its own (coordinates other sequencers)

2. **VirtualSequence**
   - Extends `uvm_sequence`
   - Coordinates sequences on multiple sequencers
   - Parallel execution using `cocotb.start_soon()`
   - Sequential execution using `await seq.start()`
   - Demonstrates sequence synchronization

3. **ChannelSequence**
   - Regular sequence for a single channel
   - Generates transactions for a specific channel
   - Configurable channel number and item count

**Virtual Sequence Patterns:**

**Parallel Execution:**
```python
# Start sequences in parallel
master_task = cocotb.start_soon(master_seq.start(self.master_seqr))
slave_task = cocotb.start_soon(slave_seq.start(self.slave_seqr))

# Wait for both to complete
await master_task
await slave_task
```

**Sequential Execution:**
```python
# Start sequences sequentially
await seq1.start(self.master_seqr)
await seq2.start(self.slave_seqr)
```

**Running the example:**

```bash
# Via module script
./scripts/module5.sh --virtual-sequences

# Or directly from example directory
cd module5/examples/virtual_sequences
make SIM=verilator TEST=virtual_sequence_example
```

**Expected Output:**
- Virtual sequencer creation and connection
- Parallel sequence execution
- Sequential sequence execution
- Multi-sequencer coordination

### 2. Coverage (`examples/coverage/coverage_example.py`)

Demonstrates functional coverage implementation:

**Key Concepts:**
- Coverage model class extending `uvm_subscriber`
- Coverage sampling via `write()` method
- Coverpoints and bins (simplified Python implementation)
- Cross coverage between multiple fields
- Coverage analysis and reporting

**Coverage Classes:**

1. **CoverageModel**
   - Extends `uvm_subscriber`
   - Receives transactions via analysis port
   - Samples coverage in `write()` method
   - Tracks coverage data structures
   - Reports coverage in `report_phase()`

2. **CoverageMonitor**
   - Generates sample transactions
   - Broadcasts via analysis port
   - Connected to coverage model

**Coverage Types:**

1. **Data Coverage**
   - Tracks unique data values
   - Coverage: number of unique values / total possible values
   - Example: 5 unique values / 256 possible = 2.0% coverage

2. **Address Range Coverage**
   - Tracks address ranges (low, mid, high)
   - Coverage: samples in each range
   - Example: Low (0x0000-0x3FFF), Mid (0x4000-0x7FFF), High (0x8000-0xFFFF)

3. **Command Coverage**
   - Tracks unique command values
   - Coverage: number of unique commands / total possible
   - Example: 3 unique commands / 256 possible = 1.2% coverage

4. **Cross Coverage**
   - Tracks combinations of data and command
   - Coverage: number of unique combinations
   - Example: (data, command) pairs

**Coverage Sampling:**
```python
def write(self, txn):
    """Sample coverage for transaction."""
    # Data coverage
    self.data_coverage[txn.data] = self.data_coverage.get(txn.data, 0) + 1
    
    # Address range coverage
    if txn.address < 0x4000:
        self.address_ranges['low'] += 1
    elif txn.address < 0x8000:
        self.address_ranges['mid'] += 1
    else:
        self.address_ranges['high'] += 1
    
    # Cross coverage
    key = (txn.data, txn.command)
    self.cross_coverage[key] = self.cross_coverage.get(key, 0) + 1
```

**Running the example:**

```bash
./scripts/module5.sh --coverage
# or
cd module5/examples/coverage
make SIM=verilator TEST=coverage_example
```

**Expected Output:**
- Coverage sampling demonstration
- Coverage statistics reporting
- Coverage percentage calculations
- Cross coverage tracking

### 3. Configuration (`examples/configuration/configuration_example.py`)

Demonstrates complex configuration object design and hierarchy:

**Key Concepts:**
- Configuration objects extending `uvm_object`
- Hierarchical configuration structure
- Configuration validation
- Configuration composition
- Configuration inheritance

**Configuration Classes:**

1. **AgentConfig**
   - Configuration for agent components
   - Fields: `active`, `has_coverage`, `address_width`, `data_width`, `max_outstanding`
   - `validate()` method for configuration validation
   - Used by agents to configure behavior

2. **EnvConfig**
   - Environment-level configuration
   - Contains agent configurations (`master_config`, `slave_config`)
   - Fields: `num_agents`, `enable_scoreboard`, `enable_coverage`
   - Demonstrates configuration composition

**Configuration Patterns:**

**Configuration Validation:**
```python
def validate(self):
    """Validate configuration values."""
    if self.address_width not in [16, 32, 64]:
        return False
    if self.data_width not in [8, 16, 32, 64]:
        return False
    if self.max_outstanding < 1:
        return False
    return True
```

**Hierarchical Configuration:**
```python
# Set configuration at different hierarchy levels
ConfigDB().set(None, "", "env.config", env_config)
ConfigDB().set(None, "", "env.master_agent.config", master_config)
ConfigDB().set(None, "", "env.slave_agent.config", slave_config)
```

**Configuration Usage:**
```python
# Get configuration in build_phase
config = None
success = ConfigDB().get(None, "", f"{self.get_full_name()}.config", config)
if success and config is not None:
    self.config = config
    if not self.config.validate():
        self.logger.error("Configuration validation failed")
```

**Running the example:**

```bash
./scripts/module5.sh --configuration
# or
cd module5/examples/configuration
make SIM=verilator TEST=configuration_example
```

**Configuration Benefits:**
- Centralized configuration management
- Hierarchical configuration inheritance
- Configuration validation and error checking
- Easy test customization without code changes

### 4. Callbacks (`examples/callbacks/callback_example.py`)

Demonstrates callback implementation patterns:

**Key Concepts:**
- Callback class design (note: pyuvm may have limited callback support)
- Pre/post callbacks for drivers and monitors
- Callback registration (conceptual demonstration)
- Callback usage patterns

**Callback Classes:**

1. **DriverCallback**
   - Callback for driver operations
   - Methods: `pre_drive()`, `post_drive()`
   - Can modify transactions before/after driving
   - Demonstrates callback structure

2. **MonitorCallback**
   - Callback for monitor operations
   - Methods: `pre_sample()`, `post_sample()`
   - Can modify transactions before/after sampling
   - Demonstrates callback structure

**Note:** pyuvm may not have full callback support as in SystemVerilog UVM. This example demonstrates the callback pattern conceptually.

**Callback Patterns:**

**Pre-Drive Callback:**
```python
def pre_drive(self, driver, txn):
    """Called before driving transaction."""
    # Can modify transaction
    txn.data = modify_data(txn.data)
    return txn
```

**Post-Drive Callback:**
```python
def post_drive(self, driver, txn):
    """Called after driving transaction."""
    # Can perform actions after driving
    self.logger.info(f"Transaction driven: {txn}")
```

**Callback Registration (Conceptual):**
```python
# In end_of_elaboration_phase
callback = DriverCallback.create("callback")
# In full UVM: driver.add_callback(callback)
```

**Running the example:**

```bash
./scripts/module5.sh --callbacks
# or
cd module5/examples/callbacks
make SIM=verilator TEST=callback_example
```

**Callback Benefits:**
- Non-intrusive test enhancements
- Reusable callback implementations
- Flexible test customization
- Separation of concerns

### 5. Register Model (`examples/register_model/register_model_example.py`)

Demonstrates register model implementation:

**Key Concepts:**
- Register model class design (simplified example)
- Frontdoor register operations (read/write)
- Backdoor register operations (peek/poke)
- Register update operations
- Register sequence integration

**Note:** This is a simplified example. Full UVM register model support may require additional pyuvm features.

**Register Model Classes:**

1. **RegisterModel**
   - Simplified register model implementation
   - Stores register values (address -> value)
   - Provides frontdoor operations: `read()`, `write()`
   - Provides backdoor operations: `peek()`, `poke()`
   - Provides update operation: `update()`

2. **RegisterSequence**
   - Sequence for register access
   - Generates register read/write transactions
   - Integrates with register model

3. **RegisterDriver**
   - Driver for register operations
   - Executes register read/write operations
   - Uses register model for operations

**Register Operations:**

**Frontdoor Operations:**
```python
# Write register via frontdoor (through DUT interface)
reg_model.write(0x0000, 0x01)

# Read register via frontdoor
value = reg_model.read(0x0000)
```

**Backdoor Operations:**
```python
# Poke register via backdoor (direct access)
reg_model.poke(0x0004, 0x80)

# Peek register via backdoor
value = reg_model.peek(0x0004)
```

**Update Operation:**
```python
# Update all registers (write desired values to hardware)
reg_model.update()
```

**Register Definitions:**
```python
self.reg_defs = {
    0x0000: "CONTROL",
    0x0004: "STATUS",
    0x0008: "DATA",
    0x000C: "CONFIG",
}
```

**Running the example:**

```bash
./scripts/module5.sh --register-model
# or
cd module5/examples/register_model
make SIM=verilator TEST=register_model_example
```

**Register Model Benefits:**
- Abstract register access interface
- Frontdoor and backdoor operations
- Register update and verification
- Integration with sequences and drivers

## Design Under Test (DUT)

### Multi-Channel Interface (`dut/advanced/multi_channel.v`)

A multi-channel interface for advanced UVM testing.

**Module Interface:**
```verilog
module multi_channel (
    input  wire       clk,            // Clock signal
    input  wire       rst_n,          // Active-low reset
    input  wire       master_valid,   // Master channel valid
    output reg        master_ready,   // Master channel ready
    input  wire [7:0] master_data,    // Master channel data (8-bit)
    input  wire       slave_valid,    // Slave channel valid
    output reg        slave_ready,    // Slave channel ready
    input  wire [7:0] slave_data      // Slave channel data (8-bit)
);
```

**Functionality:**
- Resets to all zeros when `rst_n` is low
- Master channel: asserts `master_ready` when `master_valid` is asserted
- Slave channel: asserts `slave_ready` when `slave_valid` is asserted
- Independent handshaking for each channel
- Simple multi-channel protocol for virtual sequence testing

**Characteristics:**
- Synchronous operation with async reset
- Two independent channels (master and slave)
- Valid/ready handshaking per channel
- Suitable for virtual sequence and multi-agent testing

**Protocol:**
- Master channel: Valid/ready handshaking
- Slave channel: Valid/ready handshaking
- Independent operation of channels

## Testbenches

### pyuvm Tests (`tests/pyuvm_tests/`)

#### Advanced UVM Test (`test_advanced_uvm.py`)

Complete UVM testbench demonstrating advanced concepts:

**UVM Components:**

1. **Transaction (`AdvancedTransaction`)**
   - Contains `data` and `channel` fields
   - Used for multi-channel testing

2. **Sequence (`AdvancedSequence`)**
   - Generates test transactions
   - Creates and sends transactions

3. **Driver (`AdvancedDriver`)**
   - Receives transactions from sequencer
   - Drives DUT inputs (pattern shown)

4. **Monitor (`AdvancedMonitor`)**
   - Samples DUT outputs
   - Creates transactions from sampled data
   - Broadcasts via analysis port

5. **Coverage (`AdvancedCoverage`)**
   - Extends `uvm_subscriber`
   - Receives transactions from monitor
   - Samples coverage for data values

6. **Agent (`AdvancedAgent`)**
   - Contains driver, monitor, and sequencer
   - Connects components

7. **Environment (`AdvancedEnv`)**
   - Contains agent and coverage
   - Connects monitor to coverage

8. **Test (`AdvancedUVMTest`)**
   - Top-level test class
   - Creates environment and runs test
   - Starts sequence and checks coverage

**Test Flow:**
1. `build_phase()` - Create all components
2. `connect_phase()` - Connect components
3. `run_phase()` - Start sequence, generate transactions
4. `check_phase()` - Verify results
5. `report_phase()` - Generate test report

**Running the test:**

```bash
# Via module script
./scripts/module5.sh --pyuvm-tests

# Directly from test directory
cd module5/tests/pyuvm_tests
make SIM=verilator TEST=test_advanced_uvm
```

**Expected Results:**
- 1 test case passing
- All components created and connected
- Sequence execution demonstrated
- Coverage sampling demonstrated
- Advanced UVM concepts integrated

## Running Examples and Tests

### Using the Module Script

The `module5.sh` script provides a convenient way to run all examples and tests:

```bash
# Run everything (all examples + all tests)
./scripts/module5.sh

# Run only examples
./scripts/module5.sh --all-examples

# Run only tests
./scripts/module5.sh --pyuvm-tests

# Run specific examples
./scripts/module5.sh --virtual-sequences
./scripts/module5.sh --coverage
./scripts/module5.sh --configuration
./scripts/module5.sh --callbacks
./scripts/module5.sh --register-model

# Combine options
./scripts/module5.sh --virtual-sequences --coverage --pyuvm-tests
```

### Running Individual Examples

#### Direct Execution from Example Directory

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to example directory
cd module5/examples/virtual_sequences

# Run example
make SIM=verilator TEST=virtual_sequence_example

# Clean build artifacts
make clean
```

#### Running All Examples Sequentially

```bash
cd module5/examples

# Virtual sequences
cd virtual_sequences && make SIM=verilator TEST=virtual_sequence_example && cd ..

# Coverage
cd coverage && make SIM=verilator TEST=coverage_example && cd ..

# Configuration
cd configuration && make SIM=verilator TEST=configuration_example && cd ..

# Callbacks
cd callbacks && make SIM=verilator TEST=callback_example && cd ..

# Register model
cd register_model && make SIM=verilator TEST=register_model_example && cd ..
```

### Running pyuvm Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module5/tests/pyuvm_tests

# Run test
make SIM=verilator TEST=test_advanced_uvm

# Clean build artifacts
make clean
```

## Test Results

When tests complete successfully, you should see output similar to:

### Example Test Output

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** virtual_sequence_example.test_virtual_sequence  PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Expected Test Counts

- **Virtual Sequences example**: 1 test
- **Coverage example**: 1 test
- **Configuration example**: 1 test
- **Callbacks example**: 1 test
- **Register Model example**: 1 test
- **Advanced UVM test**: 1 test
- **Total**: 6 tests across all examples and testbenches

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

#### 3. Virtual Sequence Not Coordinating

**Error:** Virtual sequence doesn't coordinate multiple sequencers

**Solution:**
- Verify virtual sequencer references are set in `connect_phase()`
- Ensure sequences are started on correct sequencers
- Check virtual sequence has references to sequencers
- Verify parallel execution uses `cocotb.start_soon()` correctly

#### 4. Coverage Not Sampling

**Error:** Coverage model doesn't receive transactions

**Solution:**
- Verify coverage extends `uvm_subscriber` (provides `analysis_export`)
- Check monitor's analysis port is connected to coverage's analysis export
- Ensure `write()` method is implemented in coverage model
- Verify connection is made in environment's `connect_phase()`

#### 5. Configuration Not Found

**Error:** Configuration not found in ConfigDB

**Solution:**
- Verify configuration is set before components try to get it
- Check hierarchy path matches exactly
- Use full hierarchy path for component-specific configuration
- Ensure configuration is set in parent's `build_phase()` before child's `build_phase()`

#### 6. Callbacks Not Working

**Error:** Callbacks don't execute

**Solution:**
- Note: pyuvm may have limited callback support compared to SystemVerilog UVM
- This example demonstrates callback patterns conceptually
- Check pyuvm documentation for callback support
- Consider using direct method calls as alternative to callbacks

#### 7. Register Model Issues

**Error:** Register operations fail

**Solution:**
- Verify register model is created and accessible
- Check register address is in `reg_defs` dictionary
- Ensure register operations use correct addresses
- Note: This is a simplified example; full UVM register model may require additional features

### Debugging Tips

1. **Check Virtual Sequencer Connections:**
   ```python
   # Verify sequencer references are set
   self.logger.info(f"Master sequencer: {self.virtual_seqr.master_seqr}")
   self.logger.info(f"Slave sequencer: {self.virtual_seqr.slave_seqr}")
   ```

2. **Monitor Coverage Sampling:**
   ```python
   # Add logging in coverage write method
   self.logger.info(f"Sampling coverage for: {txn}")
   ```

3. **Check Configuration Values:**
   ```python
   # Print configuration after getting it
   self.logger.info(f"Configuration: {self.config}")
   ```

4. **Verify Sequence Execution:**
   ```python
   # Add logging in sequence body
   print(f"Starting sequence on sequencer: {self.sequencer}")
   ```

5. **Inspect Coverage Statistics:**
   ```python
   # Check coverage in report_phase
   coverage_stats = self.coverage.get_coverage()
   self.logger.info(f"Coverage stats: {coverage_stats}")
   ```

6. **Validate Configuration:**
   ```python
   # Validate configuration before use
   if not self.config.validate():
       self.logger.error("Configuration validation failed")
   ```

## Topics Covered

1. **Virtual Sequences** - Coordinating multiple sequencers, parallel/sequential execution
2. **Coverage Models** - Functional coverage, coverpoints, cross coverage
3. **Complex Configuration** - Configuration objects, hierarchy, validation
4. **Callbacks** - Callback patterns, pre/post callbacks (conceptual)
5. **Register Model** - Register operations, frontdoor/backdoor access
6. **Sequence Coordination** - Multi-sequencer coordination, synchronization
7. **Coverage Analysis** - Coverage collection, reporting, closure
8. **Configuration Patterns** - Configuration strategies, validation, inheritance
9. **Advanced Debugging** - Debugging techniques for advanced UVM
10. **Testbench Integration** - Integrating advanced concepts into testbenches

## Next Steps

After completing Module 5, proceed to:

- **Module 6**: Protocol Verification - Multi-agent testbenches, protocol checkers
- **Module 7**: Advanced Topics - DMA, VIP integration, best practices
- **Module 8**: Advanced Utilities - CLP, comparators, pools, queues, recorders

## Additional Resources

- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [UVM User's Guide](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [cocotb Documentation](https://docs.cocotb.org/)
- [Verilator Documentation](https://verilator.org/)

## File Descriptions

### Examples

| File | Description | Tests |
|------|-------------|-------|
| `virtual_sequence_example.py` | Virtual sequencer and sequence coordination | 1 test function |
| `coverage_example.py` | Functional coverage implementation | 1 test function |
| `configuration_example.py` | Complex configuration objects | 1 test function |
| `callback_example.py` | Callback implementation patterns | 1 test function |
| `register_model_example.py` | Register model implementation | 1 test function |

### DUT Modules

| File | Description | Ports |
|------|-------------|-------|
| `multi_channel.v` | Multi-channel interface | `clk`, `rst_n`, `master_valid`, `master_ready`, `master_data[7:0]`, `slave_valid`, `slave_ready`, `slave_data[7:0]` |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_advanced_uvm.py` | pyuvm | Advanced UVM testbench | 1 UVM test |

---

For questions or issues, refer to the main project README or check the test logs for detailed error messages.
