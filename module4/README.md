# Module 4: UVM Components

This directory contains all examples, exercises, and test cases for Module 4, focusing on UVM component implementation including transactions, drivers, monitors, sequencers, TLM communication, scoreboards, and complete agents.

## Directory Structure

```
module4/
├── examples/              # pyuvm examples for each topic
│   ├── transactions/     # Transaction modeling examples
│   │   └── transaction_example.py
│   ├── drivers/          # Driver implementation examples
│   │   └── driver_example.py
│   ├── monitors/         # Monitor implementation examples
│   │   └── monitor_example.py
│   ├── sequencers/       # Sequencer and sequence examples
│   │   └── sequencer_example.py
│   ├── tlm/              # TLM communication examples
│   │   └── tlm_example.py
│   ├── scoreboards/      # Scoreboard examples
│   │   └── scoreboard_example.py
│   └── agents/           # Complete agent examples
│       └── agent_example.py
├── dut/                   # Verilog Design Under Test modules
│   └── interfaces/       # Interface modules for testing
│       └── simple_interface.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
│       └── test_complete_agent.py
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

## UVM Component Examples

### 1. Transactions (`examples/transactions/transaction_example.py`)

Demonstrates transaction-level modeling and transaction operations:

**Key Concepts:**
- Transaction class design extending `uvm_sequence_item`
- Transaction fields and data members
- Transaction copy and comparison operations
- Extended transactions with inheritance
- Constrained random transactions
- Transaction packing/unpacking methods

**Transaction Classes:**

1. **BaseTransaction**
   - Basic transaction with `data` and `address` fields
   - Implements `__str__()`, `__eq__()`, and `copy()` methods
   - Demonstrates transaction equality comparison

2. **ExtendedTransaction**
   - Extends `BaseTransaction` with `control` and `status` fields
   - Shows transaction inheritance patterns
   - Demonstrates extended comparison logic

3. **ConstrainedTransaction**
   - Transaction with randomization constraints
   - Address alignment constraint (4-byte boundary)
   - Non-zero data constraint

4. **TransactionWithMethods**
   - Demonstrates useful transaction methods
   - `pack()` - Serialize transaction to bytes
   - `unpack()` - Deserialize bytes to transaction
   - `convert2string()` - String representation
   - `do_copy()` - UVM copy method
   - `do_compare()` - UVM comparison method

**Running the example:**

```bash
# Via module script
./scripts/module4.sh --transactions

# Or directly from example directory
cd module4/examples/transactions
make SIM=verilator TEST=transaction_example
```

**Expected Output:**
- Transaction creation and manipulation
- Copy and comparison operations
- Extended transaction examples
- Constrained randomization
- Pack/unpack operations

### 2. Drivers (`examples/drivers/driver_example.py`)

Demonstrates UVM driver implementation:

**Key Concepts:**
- Driver class structure extending `uvm_driver`
- Transaction reception from sequencer via `seq_item_port`
- Signal driving to DUT
- Driver-sequencer communication
- Protocol-specific driving patterns

**Driver Classes:**

1. **SimpleDriver**
   - Basic driver implementation
   - Receives transactions from sequencer
   - Drives DUT signals (pattern shown)
   - Signals transaction completion

2. **ProtocolDriver**
   - Protocol-aware driver
   - Implements handshaking (request/grant)
   - Protocol timing control
   - Demonstrates protocol-specific patterns

**Driver Flow:**
1. `build_phase()` - Create `seq_item_port`
2. `connect_phase()` - Connect to sequencer
3. `run_phase()` - Main driver loop:
   - `get_next_item()` - Get transaction from sequencer
   - `drive_transaction()` - Drive signals to DUT
   - `item_done()` - Signal completion

**Running the example:**

```bash
./scripts/module4.sh --drivers
# or
cd module4/examples/drivers
make SIM=verilator TEST=driver_example
```

**Driver Patterns:**
- Continuous loop in `run_phase()`
- Transaction-driven signal updates
- Protocol timing implementation
- Handshaking with DUT

### 3. Monitors (`examples/monitors/monitor_example.py`)

Demonstrates UVM monitor implementation:

**Key Concepts:**
- Monitor class structure extending `uvm_monitor`
- Signal sampling from DUT
- Transaction creation from sampled signals
- Analysis port broadcasting
- Protocol-aware monitoring

**Monitor Classes:**

1. **SimpleMonitor**
   - Basic monitor implementation
   - Samples DUT signals
   - Creates transactions from sampled data
   - Broadcasts via analysis port

2. **ProtocolMonitor**
   - Protocol-aware monitoring
   - Waits for protocol events
   - Samples on protocol-specific conditions
   - Tracks sample count

**Monitor Flow:**
1. `build_phase()` - Create `analysis_port`
2. `run_phase()` - Main monitor loop:
   - `sample_signals()` - Sample DUT signals
   - Create transaction from sampled data
   - `ap.write()` - Broadcast via analysis port

**Running the example:**

```bash
./scripts/module4.sh --monitors
# or
cd module4/examples/monitors
make SIM=verilator TEST=monitor_example
```

**Monitor Patterns:**
- Continuous monitoring loop
- Event-driven sampling
- Transaction creation and broadcasting
- Protocol-specific sampling

### 4. Sequencers (`examples/sequencers/sequencer_example.py`)

Demonstrates UVM sequencer and sequence implementation:

**Key Concepts:**
- Sequencer class (`uvm_sequencer`)
- Sequence class extending `uvm_sequence`
- Sequence body implementation
- Transaction generation in sequences
- Sequence layering and composition
- Random sequence generation

**Sequence Classes:**

1. **SimpleSequence**
   - Basic sequence implementation
   - Generates fixed test vectors
   - Uses `start_item()` and `finish_item()`
   - Demonstrates sequence execution

2. **RandomSequence**
   - Random transaction generation
   - Configurable number of items
   - Constrained random values
   - Reusable sequence pattern

3. **LayeredSequence**
   - Sequence composition
   - Calls other sequences
   - Hierarchical sequence structure
   - Demonstrates sequence reuse

**Sequence Flow:**
1. `body()` - Sequence execution method
2. `start_item(txn)` - Request transaction from sequencer
3. `finish_item(txn)` - Send transaction to driver
4. Sequence completes when `body()` returns

**Running the example:**

```bash
./scripts/module4.sh --sequencers
# or
cd module4/examples/sequencers
make SIM=verilator TEST=sequencer_example
```

**Sequence Patterns:**
- Transaction generation loops
- Random vs deterministic sequences
- Sequence composition
- Reusable sequence libraries

### 5. TLM (`examples/tlm/tlm_example.py`)

Demonstrates Transaction-Level Modeling (TLM) interfaces:

**Key Concepts:**
- TLM ports, exports, and implementations
- Put interface (producer-consumer)
- Get interface (provider-consumer)
- Transport interface (request-response)
- TLM FIFO for buffering
- TLM connections and communication

**TLM Interfaces:**

1. **Put Interface**
   - `PutProducer` - Uses `uvm_put_port`
   - `PutConsumer` - Implements `uvm_put_export`
   - Methods: `put()`, `try_put()`, `can_put()`

2. **Get Interface**
   - `GetProducer` - Implements `uvm_get_export`
   - `GetConsumer` - Uses `uvm_get_port`
   - Methods: `get()`, `try_get()`, `can_get()`

3. **Transport Interface**
   - `TransportComponent` - Implements `uvm_transport_export`
   - Request-response pattern
   - Methods: `transport()`, `nb_transport()`

4. **TLM FIFO**
   - `uvm_tlm_fifo` - Buffered communication
   - `FIFOProducer` - Produces to FIFO
   - `FIFOConsumer` - Consumes from FIFO

**TLM Connection:**
```python
# Put interface
producer.put_port.connect(consumer)

# Get interface
consumer.get_port.connect(producer)

# FIFO
producer.put_port.connect(fifo.put_export)
consumer.get_port.connect(fifo.get_export)
```

**Running the example:**

```bash
./scripts/module4.sh --tlm
# or
cd module4/examples/tlm
make SIM=verilator TEST=tlm_example
```

**TLM Benefits:**
- Decoupled component communication
- Transaction-level abstraction
- Flexible connection patterns
- Reusable communication interfaces

### 6. Scoreboards (`examples/scoreboards/scoreboard_example.py`)

Demonstrates scoreboard implementation for result checking:

**Key Concepts:**
- Scoreboard class extending `uvm_subscriber`
- Analysis port connections
- Expected vs actual comparison
- Mismatch detection and reporting
- Reference model integration

**Scoreboard Classes:**

1. **SimpleScoreboard**
   - Basic scoreboard implementation
   - Stores expected and actual transactions
   - Compares and reports mismatches
   - Provides statistics in `check_phase()`

2. **ReferenceModelScoreboard**
   - Scoreboard with reference model
   - Calculates expected values dynamically
   - Compares with reference model output
   - Demonstrates golden reference pattern

**Scoreboard Flow:**
1. `build_phase()` - Initialize storage
2. `write(txn)` - Receive transactions from monitor
3. Compare with expected (or reference model)
4. `check_phase()` - Final verification and reporting

**Running the example:**

```bash
./scripts/module4.sh --scoreboards
# or
cd module4/examples/scoreboards
make SIM=verilator TEST=scoreboard_example
```

**Scoreboard Patterns:**
- Expected queue management
- Transaction comparison logic
- Mismatch tracking
- Reference model integration
- Statistics reporting

### 7. Agents (`examples/agents/agent_example.py`)

Demonstrates complete agent implementation:

**Key Concepts:**
- Agent class structure extending `uvm_agent`
- Active vs passive agent configuration
- Component integration (driver, monitor, sequencer)
- Component connections
- Agent configuration via ConfigDB

**Agent Components:**

1. **CompleteAgent**
   - Contains driver, monitor, and sequencer
   - Active/passive configuration
   - Component creation and connection
   - Demonstrates full agent structure

2. **AgentDriver**
   - Drives transactions to DUT
   - Connected to sequencer

3. **AgentMonitor**
   - Samples DUT signals
   - Broadcasts via analysis port

4. **AgentSequence**
   - Generates test transactions
   - Sends to sequencer

**Agent Modes:**

- **Active Agent**: Contains driver, sequencer, and monitor
  - Can drive and monitor DUT
  - Used for active verification

- **Passive Agent**: Contains only monitor
  - Observes DUT only
  - Used for passive monitoring or reference checking

**Running the example:**

```bash
./scripts/module4.sh --agents
# or
cd module4/examples/agents
make SIM=verilator TEST=agent_example
```

**Test Cases:**
1. `test_complete_agent` - Active agent demonstration
2. `test_passive_agent` - Passive agent demonstration

**Expected Output:**
- Agent component creation
- Active/passive mode configuration
- Component connections
- Agent operation demonstration

## Design Under Test (DUT)

### Simple Interface (`dut/interfaces/simple_interface.v`)

A simple interface module for UVM component testing.

**Module Interface:**
```verilog
module simple_interface (
    input  wire       clk,      // Clock signal
    input  wire       rst_n,    // Active-low reset
    input  wire       valid,    // Valid signal
    output reg        ready,    // Ready signal
    input  wire [7:0] data,     // Data bus (8-bit)
    input  wire [15:0] address,  // Address bus (16-bit)
    output reg  [7:0] result    // Result output (8-bit)
);
```

**Functionality:**
- Resets to all zeros when `rst_n` is low
- When `valid` is asserted, sets `ready` and computes `result = data + 1`
- Simple handshaking protocol (valid/ready)
- Demonstrates basic interface for UVM component testing

**Characteristics:**
- Synchronous operation with async reset
- Valid/ready handshaking
- Simple data transformation (increment)
- Suitable for UVM component demonstration

**Protocol:**
- Driver asserts `valid` with `data` and `address`
- DUT responds with `ready` and `result = data + 1`
- Monitor samples `ready` and `result`

## Testbenches

### pyuvm Tests (`tests/pyuvm_tests/`)

#### Complete Agent Test (`test_complete_agent.py`)

Complete UVM testbench demonstrating all component integration:

**UVM Components:**

1. **Transaction (`InterfaceTransaction`)**
   - Contains `data`, `address`, and `expected_result`
   - Used for stimulus and checking

2. **Sequence (`InterfaceSequence`)**
   - Generates test vectors
   - Creates and sends transactions

3. **Driver (`InterfaceDriver`)**
   - Receives transactions from sequencer
   - Drives DUT inputs (pattern shown)

4. **Monitor (`InterfaceMonitor`)**
   - Samples DUT outputs
   - Creates transactions from sampled data
   - Broadcasts via analysis port

5. **Scoreboard (`InterfaceScoreboard`)**
   - Receives transactions from monitor
   - Compares expected vs actual
   - Reports mismatches

6. **Agent (`InterfaceAgent`)**
   - Contains driver, monitor, and sequencer
   - Connects components

7. **Environment (`InterfaceEnv`)**
   - Contains agent and scoreboard
   - Connects monitor to scoreboard

8. **Test (`CompleteAgentTest`)**
   - Top-level test class
   - Creates environment and runs test

**Test Flow:**
1. `build_phase()` - Create all components
2. `connect_phase()` - Connect components
3. `run_phase()` - Execute test (sequence would start here)
4. `check_phase()` - Verify results in scoreboard
5. `report_phase()` - Generate test report

**Running the test:**

```bash
# Via module script
./scripts/module4.sh --pyuvm-tests

# Directly from test directory
cd module4/tests/pyuvm_tests
make SIM=verilator TEST=test_complete_agent
```

**Expected Results:**
- 1 test case passing
- All components created and connected
- Component integration demonstrated
- Scoreboard verification completed

## Running Examples and Tests

### Using the Module Script

The `module4.sh` script provides a convenient way to run all examples and tests:

```bash
# Run everything (all examples + all tests)
./scripts/module4.sh

# Run only examples
./scripts/module4.sh --all-examples

# Run only tests
./scripts/module4.sh --pyuvm-tests

# Run specific examples
./scripts/module4.sh --transactions
./scripts/module4.sh --drivers
./scripts/module4.sh --monitors
./scripts/module4.sh --sequencers
./scripts/module4.sh --tlm
./scripts/module4.sh --scoreboards
./scripts/module4.sh --agents

# Combine options
./scripts/module4.sh --drivers --monitors --tlm --pyuvm-tests
```

### Running Individual Examples

#### Direct Execution from Example Directory

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to example directory
cd module4/examples/drivers

# Run example
make SIM=verilator TEST=driver_example

# Clean build artifacts
make clean
```

#### Running All Examples Sequentially

```bash
cd module4/examples

# Transactions
cd transactions && make SIM=verilator TEST=transaction_example && cd ..

# Drivers
cd drivers && make SIM=verilator TEST=driver_example && cd ..

# Monitors
cd monitors && make SIM=verilator TEST=monitor_example && cd ..

# Sequencers
cd sequencers && make SIM=verilator TEST=sequencer_example && cd ..

# TLM
cd tlm && make SIM=verilator TEST=tlm_example && cd ..

# Scoreboards
cd scoreboards && make SIM=verilator TEST=scoreboard_example && cd ..

# Agents
cd agents && make SIM=verilator TEST=agent_example && cd ..
```

### Running pyuvm Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module4/tests/pyuvm_tests

# Run test
make SIM=verilator TEST=test_complete_agent

# Clean build artifacts
make clean
```

## Test Results

When tests complete successfully, you should see output similar to:

### Example Test Output

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** transaction_example.test_transaction           PASS          10.00           0.00      12256.88  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 10.00           0.00       7345.54  **
```

### Expected Test Counts

- **Transaction example**: 1 test
- **Driver example**: 1 test
- **Monitor example**: 1 test
- **Sequencer example**: 1 test
- **TLM example**: 1 test
- **Scoreboard example**: 1 test
- **Agent example**: 2 tests (active and passive)
- **Complete Agent test**: 1 test
- **Total**: 9 tests across all examples and testbenches

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

#### 3. TLM Import Errors

**Error:** `NameError: name 'uvm_put_imp' is not defined`

**Solution:** Some TLM classes may need explicit imports. The examples include fallback import logic. If issues persist, check pyuvm version compatibility.

#### 4. Sequence Not Starting

**Error:** Sequence doesn't execute or hangs

**Solution:**
- Ensure sequencer is connected to driver
- Verify sequence is started with correct sequencer reference
- Check that `body()` method is async and uses `await`
- Ensure test raises objection before starting sequence

#### 5. Driver Not Receiving Transactions

**Error:** Driver loop doesn't receive transactions

**Solution:**
- Verify `seq_item_port` is connected to sequencer's `seq_item_export`
- Check connection is made in `connect_phase()`
- Ensure sequence is started on the correct sequencer
- Verify sequencer is created in agent's `build_phase()`

#### 6. Monitor Not Broadcasting

**Error:** Scoreboard doesn't receive transactions from monitor

**Solution:**
- Verify monitor's `analysis_port` is connected to scoreboard's `analysis_export`
- Check connection is made in environment's `connect_phase()`
- Ensure monitor calls `ap.write(txn)` after sampling
- Verify scoreboard extends `uvm_subscriber` (provides `analysis_export`)

#### 7. Scoreboard Mismatches

**Error:** Scoreboard reports unexpected mismatches

**Solution:**
- Verify expected transactions are added before actual transactions arrive
- Check transaction comparison logic
- Ensure transaction fields match (data types, values)
- Review reference model if using one

### Debugging Tips

1. **Check Component Connections:**
   ```python
   # Print component hierarchy
   self.print_topology()
   ```

2. **Verify TLM Connections:**
   ```python
   # Check if ports are connected
   if self.put_port.is_connected():
       self.logger.info("Put port is connected")
   ```

3. **Monitor Transaction Flow:**
   ```python
   # Add logging in driver
   self.logger.info(f"Received transaction: {item}")
   
   # Add logging in monitor
   self.logger.info(f"Sampled transaction: {txn}")
   
   # Add logging in scoreboard
   self.logger.info(f"Received for checking: {txn}")
   ```

4. **Check Sequence Execution:**
   ```python
   # Verify sequence is started
   seq = MySequence.create("seq")
   await seq.start(self.env.agent.seqr)
   self.logger.info("Sequence started")
   ```

5. **Verify Agent Configuration:**
   ```python
   # Check agent mode
   self.logger.info(f"Agent active: {self.active}")
   ```

6. **Inspect Transaction Content:**
   ```python
   # Print transaction details
   self.logger.info(f"Transaction: {txn}")
   self.logger.info(f"Transaction data: 0x{txn.data:02X}")
   ```

## Topics Covered

1. **Transaction Modeling** - Transaction class design, operations, and methods
2. **Driver Implementation** - Transaction reception, signal driving, protocol implementation
3. **Monitor Implementation** - Signal sampling, transaction creation, analysis ports
4. **Sequencer and Sequences** - Sequence generation, execution, and composition
5. **TLM Communication** - Put/Get/Transport interfaces, ports, exports, FIFOs
6. **Scoreboard Implementation** - Expected vs actual comparison, reference models
7. **Complete Agent** - Agent structure, active/passive modes, component integration
8. **Component Connections** - Port/export connections, TLM interfaces
9. **Agent Architecture** - Driver-monitor-sequencer integration
10. **Testbench Integration** - Environment structure, component assembly

## Next Steps

After completing Module 4, proceed to:

- **Module 5**: Advanced UVM - Callbacks, coverage, register model, virtual sequences
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
| `transaction_example.py` | Transaction modeling and operations | 1 test function |
| `driver_example.py` | Driver implementation patterns | 1 test function |
| `monitor_example.py` | Monitor implementation patterns | 1 test function |
| `sequencer_example.py` | Sequencer and sequence patterns | 1 test function |
| `tlm_example.py` | TLM communication interfaces | 1 test function |
| `scoreboard_example.py` | Scoreboard implementation | 1 test function |
| `agent_example.py` | Complete agent implementation | 2 test functions |

### DUT Modules

| File | Description | Ports |
|------|-------------|-------|
| `simple_interface.v` | Simple interface for component testing | `clk`, `rst_n`, `valid`, `ready`, `data[7:0]`, `address[15:0]`, `result[7:0]` |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_complete_agent.py` | pyuvm | Complete agent testbench | 1 UVM test |

---

For questions or issues, refer to the main project README or check the test logs for detailed error messages.
