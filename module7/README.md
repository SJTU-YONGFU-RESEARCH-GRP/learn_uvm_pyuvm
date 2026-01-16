# Module 7: Real-World Applications

This directory contains all examples, exercises, and test cases for Module 7, focusing on real-world verification applications including DMA verification, protocol verification (UART, SPI, I2C), VIP development, and best practices.

## Directory Structure

```
module7/
├── examples/              # pyuvm examples for each topic
│   ├── dma/              # DMA verification examples
│   │   └── dma_example.py
│   ├── protocols/        # Protocol verification examples (UART, SPI, I2C)
│   │   ├── uart_example.py
│   │   ├── spi_example.py
│   │   └── i2c_example.py
│   ├── vip/              # VIP development examples
│   │   └── vip_example.py
│   └── best_practices/   # Best practices examples
│       └── best_practices_example.py
├── dut/                   # Verilog Design Under Test modules
│   ├── dma/              # DMA controller
│   │   └── simple_dma.v
│   └── protocols/        # Protocol modules
│       └── uart.v
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
│       └── test_real_world.py
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

## Real-World Examples

### 1. DMA Verification (`examples/dma/dma_example.py`)

Demonstrates complete DMA controller verification environment:

**Key Concepts:**
- DMA transfer transactions
- DMA register interface
- DMA transfer monitoring
- DMA scoreboard verification
- DMA coverage collection
- Simple and scatter-gather transfers

**DMA Components:**

1. **DMATransaction**
   - Transaction for DMA transfers
   - Fields: `src_addr`, `dst_addr`, `length`, `channel`, `transfer_type`
   - Supports SIMPLE and SCATTER_GATHER transfer types
   - Channel identification

2. **DMARegisterDriver**
   - Driver for DMA register interface
   - Configures DMA registers (source, destination, length)
   - Starts DMA transfers
   - Handles DMA register transactions

3. **DMAMonitor**
   - Monitor for DMA transfers
   - Monitors DMA transfer completion
   - Creates transactions from monitored transfers
   - Broadcasts via analysis port

4. **DMAScoreboard**
   - Scoreboard for DMA verification
   - Tracks expected and actual transfers
   - Matches transfers by source, destination, and length
   - Reports transfer mismatches

5. **DMACoverage**
   - Coverage model for DMA verification
   - Tracks channels used
   - Tracks transfer types
   - Tracks transfer length ranges (small, medium, large)

**DMA Transfer Types:**

**Simple Transfer:**
- Single source to single destination
- Fixed length transfer
- Single channel operation

**Scatter-Gather Transfer:**
- Multiple source/destination pairs
- Variable length transfers
- Multiple channel operation

**DMA Verification Flow:**
```python
# 1. Add expected transfer
txn = DMATransaction()
txn.src_addr = 0x1000
txn.dst_addr = 0x2000
txn.length = 256
self.env.scoreboard.add_expected(txn)

# 2. Start DMA sequence
seq = DMASequence.create("seq")
await seq.start(self.env.agent.seqr)

# 3. Monitor validates transfer
# 4. Scoreboard matches expected vs actual
```

**Running the example:**

```bash
# Via module script
./scripts/module7.sh --dma

# Or directly from example directory
cd module7/examples/dma
make SIM=verilator TEST=dma_example
```

**Expected Output:**
- DMA transfer configuration
- DMA transfer execution
- DMA transfer monitoring
- DMA scoreboard verification
- DMA coverage collection

### 2. UART Protocol Verification (`examples/protocols/uart_example.py`)

Demonstrates UART protocol verification agent:

**Key Concepts:**
- UART transaction handling
- UART transmission protocol
- UART reception monitoring
- Baud rate configuration
- Parity and stop bit handling

**UART Components:**

1. **UARTTransaction**
   - Transaction for UART operations
   - Fields: `data`, `baud_rate`, `parity`, `stop_bits`
   - Supports different baud rates
   - Supports parity types: NONE, EVEN, ODD

2. **UARTDriver**
   - Implements UART transmission protocol
   - Transmits: Start bit → Data bits → Parity → Stop bit(s)
   - Handles baud rate timing
   - Generates UART frame

3. **UARTMonitor**
   - Monitors UART reception
   - Detects start bit
   - Samples data bits
   - Detects stop bit(s)
   - Creates transactions from received data

4. **UARTSequence**
   - Generates UART test sequences
   - Creates test data patterns
   - Configures baud rate and parity
   - Tests various data values

**UART Protocol:**

**Frame Structure:**
- Start bit (0) → 8 Data bits → Parity bit (optional) → Stop bit(s) (1)

**Transmission:**
- Idle line is high (1)
- Start bit pulls line low (0)
- Data bits transmitted LSB first
- Stop bit returns line high (1)

**Running the example:**

```bash
./scripts/module7.sh --uart
# or
cd module7/examples/protocols
make SIM=verilator TEST=uart_example
```

**Expected Output:**
- UART frame transmission
- UART frame reception
- Baud rate handling
- Parity verification

### 3. SPI Protocol Verification (`examples/protocols/spi_example.py`)

Demonstrates SPI protocol verification with master-slave coordination:

**Key Concepts:**
- SPI transaction handling
- Master-slave coordination
- SPI mode configuration
- Chip select handling
- Clock and data synchronization

**SPI Components:**

1. **SPITransaction**
   - Transaction for SPI operations
   - Fields: `data`, `mode`, `cs`, `is_master`
   - Supports SPI modes 0-3
   - Chip select identification
   - Master/slave role

2. **SPIDriver**
   - Implements SPI transmission protocol
   - Transmits: CS low → Clock data → CS high
   - Handles SPI mode timing
   - Transmits MSB or LSB first (depending on mode)

3. **SPIMonitor**
   - Monitors SPI reception
   - Detects CS assertion
   - Samples data on clock edges
   - Creates transactions from received data

4. **SPIEnv**
   - Environment with master and slave agents
   - Coordinates master-slave communication
   - Demonstrates multi-agent protocol verification

**SPI Protocol:**

**Signal Lines:**
- `sclk` - Serial clock
- `mosi` - Master Out Slave In
- `miso` - Master In Slave Out
- `cs` - Chip select (active low)

**Transmission:**
- CS asserted (low) → Clock data → CS deasserted (high)
- Data transmitted synchronously with clock
- SPI mode determines clock polarity and phase

**Running the example:**

```bash
./scripts/module7.sh --spi
# or
cd module7/examples/protocols
make SIM=verilator TEST=spi_example
```

**Expected Output:**
- SPI master transmission
- SPI slave reception
- Master-slave coordination
- SPI mode handling

### 4. I2C Protocol Verification (`examples/protocols/i2c_example.py`)

Demonstrates I2C protocol verification with multi-master support:

**Key Concepts:**
- I2C transaction handling
- Multi-master support
- START/STOP condition handling
- Address and data transmission
- ACK/NACK handling

**I2C Components:**

1. **I2CTransaction**
   - Transaction for I2C operations
   - Fields: `address`, `data[]`, `is_write`, `is_start`, `is_stop`
   - Supports 7-bit and 10-bit addressing
   - Supports read and write operations
   - START and STOP condition flags

2. **I2CDriver**
   - Implements I2C transmission protocol
   - Transmits: START → Address → R/W → ACK → Data → ACK → STOP
   - Handles START and STOP conditions
   - Transmits address and data bits
   - Handles ACK/NACK responses

3. **I2CMonitor**
   - Monitors I2C reception
   - Detects START condition
   - Samples address and data bits
   - Detects STOP condition
   - Creates transactions from received frames

4. **I2CEnv**
   - Environment with multiple masters and slave
   - Supports multi-master scenarios
   - Demonstrates I2C arbitration (conceptual)

**I2C Protocol:**

**Signal Lines:**
- `sda` - Serial data (bidirectional, open-drain)
- `scl` - Serial clock (bidirectional, open-drain)

**Frame Structure:**
- START condition → 7-bit address → R/W bit → ACK → Data bytes → ACK → STOP condition

**Running the example:**

```bash
./scripts/module7.sh --i2c
# or
cd module7/examples/protocols
make SIM=verilator TEST=i2c_example
```

**Expected Output:**
- I2C START/STOP conditions
- I2C address transmission
- I2C data transmission
- Multi-master support

### 5. VIP Development (`examples/vip/vip_example.py`)

Demonstrates creating reusable verification IP:

**Key Concepts:**
- VIP structure and components
- VIP configuration (active/passive)
- VIP reusability patterns
- VIP protocol checking
- VIP coverage collection

**VIP Components:**

1. **VIPAgent**
   - Complete VIP agent structure
   - Contains: driver, monitor, sequencer, checker, coverage
   - Supports active and passive modes
   - Configurable via ConfigDB
   - Reusable across projects

2. **VIPDriver**
   - Driver for VIP protocol
   - Drives transactions to DUT
   - Configurable protocol implementation

3. **VIPMonitor**
   - Monitor for VIP protocol
   - Samples DUT signals
   - Creates transactions from monitored data
   - Broadcasts via analysis port

4. **VIPChecker**
   - Protocol checker for VIP
   - Validates protocol compliance
   - Reports protocol violations
   - Extends `uvm_subscriber`

5. **VIPCoverage**
   - Coverage model for VIP
   - Collects functional coverage
   - Tracks transaction coverage
   - Reports coverage statistics

**VIP Configuration:**

**Active Mode:**
- Creates driver and sequencer
- Can generate and drive transactions
- Suitable for active verification

**Passive Mode:**
- No driver or sequencer
- Only monitor, checker, and coverage
- Suitable for monitoring and checking

**VIP Reusability:**
```python
# VIP can be used in multiple environments
class VIPEnv(uvm_env):
    def build_phase(self):
        # Create VIP with configuration
        self.vip = VIPAgent.create("vip", self)
        
        # Configure VIP (active/passive)
        ConfigDB().set(None, "", "env.vip.active", True)
```

**Running the example:**

```bash
./scripts/module7.sh --vip
# or
cd module7/examples/vip
make SIM=verilator TEST=vip_example
```

**Expected Output:**
- VIP agent creation
- VIP configuration (active/passive)
- VIP protocol checking
- VIP coverage collection

**VIP Benefits:**
- Reusable across projects
- Configurable for different use cases
- Self-contained verification solution
- Industry-standard structure

### 6. Best Practices (`examples/best_practices/best_practices_example.py`)

Demonstrates code organization, documentation, and best practices:

**Key Concepts:**
- Clear code organization
- Comprehensive documentation
- Component reusability
- Error handling
- Logging and reporting

**Best Practices:**

1. **Transaction Best Practices:**
   - Clear class names
   - Comprehensive docstrings
   - Type hints (in real code)
   - Clear field names
   - `__str__` method for debugging

2. **Component Best Practices:**
   - Clear component names
   - Comprehensive docstrings
   - Organized methods
   - Clear logging
   - Error handling

3. **Reusability Best Practices:**
   - Parameterization
   - Configuration support
   - Clear interfaces
   - Documentation
   - Example usage

4. **Organization Best Practices:**
   - Clear structure
   - Logical grouping
   - Clear naming
   - Documentation

**Best Practices Example:**
```python
class BestPracticesComponent(uvm_component):
    """
    Component demonstrating best practices.
    
    Best Practices:
    - Clear component name
    - Comprehensive docstring
    - Organized methods
    - Clear logging
    - Error handling
    """
    
    def build_phase(self):
        """
        Build phase with clear documentation.
        
        Best Practices:
        - Document what is built
        - Use clear variable names
        - Organize code logically
        """
        self.logger.info(f"[{self.get_name()}] Building component")
```

**Running the example:**

```bash
./scripts/module7.sh --best-practices
# or
cd module7/examples/best_practices
make SIM=verilator TEST=best_practices_example
```

**Expected Output:**
- Well-organized code structure
- Clear documentation
- Reusable components
- Clear logging and reporting

**Best Practices Benefits:**
- Improved maintainability
- Better code reuse
- Easier debugging
- Clearer documentation

## Design Under Test (DUT)

### Simple DMA Controller (`dut/dma/simple_dma.v`)

A simple DMA controller for verification.

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

**Characteristics:**
- Simplified DMA implementation
- Synchronous operation with async reset
- Basic transfer state machine
- Suitable for DMA verification

**Protocol:**
- Register-based configuration
- Start-triggered transfers
- Completion indication
- Channel-based operation

### UART Transmitter/Receiver (`dut/protocols/uart.v`)

A simple UART for protocol verification.

**Module Interface:**
```verilog
module uart (
    input  wire       clk,       // Clock signal
    input  wire       rst_n,     // Active-low reset
    output reg        tx,        // Transmit data line
    input  wire       rx,        // Receive data line
    input  wire [7:0] tx_data,   // Data to transmit (8-bit)
    input  wire       tx_start,  // Start transmission
    output reg        tx_busy,   // Transmission in progress
    output reg  [7:0] rx_data,   // Received data (8-bit)
    output reg        rx_ready   // Received data ready
);
```

**Functionality:**
- Full-duplex UART communication
- Transmitter state machine: IDLE → START → DATA → STOP
- Receiver state machine: IDLE → START → DATA → STOP
- 8-bit data transmission
- Start and stop bit handling

**Characteristics:**
- Simplified UART implementation
- Synchronous operation with async reset
- Separate transmitter and receiver
- Suitable for UART protocol verification

**Protocol:**
- Start bit (0) → 8 Data bits → Stop bit (1)
- Idle line is high (1)
- Data transmitted LSB first

## Testbenches

### pyuvm Tests (`tests/pyuvm_tests/`)

#### Real-World Application Test (`test_real_world.py`)

Complete UVM testbench demonstrating real-world verification scenarios:

**UVM Components:**

1. **Transaction (`RealWorldTransaction`)**
   - Contains `data` and `address` fields
   - Used for real-world testing

2. **Sequence (`RealWorldSequence`)**
   - Generates test transactions
   - Creates comprehensive test vectors

3. **Driver (`RealWorldDriver`)**
   - Receives transactions from sequencer
   - Drives DUT inputs

4. **Monitor (`RealWorldMonitor`)**
   - Samples DUT outputs
   - Creates transactions from sampled data
   - Broadcasts via analysis port

5. **Scoreboard (`RealWorldScoreboard`)**
   - Extends `uvm_subscriber`
   - Receives transactions from monitor
   - Tracks received transactions

6. **Agent (`RealWorldAgent`)**
   - Contains driver, monitor, and sequencer
   - Connects components

7. **Environment (`RealWorldEnv`)**
   - Contains agent and scoreboard
   - Connects monitor to scoreboard

8. **Test (`RealWorldTest`)**
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
./scripts/module7.sh --pyuvm-tests

# Directly from test directory
cd module7/tests/pyuvm_tests
make SIM=verilator TEST=test_real_world
```

**Expected Results:**
- 1 test case passing
- All components created and connected
- Sequence execution demonstrated
- Scoreboard tracking demonstrated
- Real-world verification concepts integrated

## Running Examples and Tests

### Using the Module Script

The `module7.sh` script provides a convenient way to run all examples and tests:

```bash
# Run everything (all examples + all tests)
./scripts/module7.sh

# Run only examples
./scripts/module7.sh --all-examples

# Run only tests
./scripts/module7.sh --pyuvm-tests

# Run specific examples
./scripts/module7.sh --dma
./scripts/module7.sh --uart
./scripts/module7.sh --spi
./scripts/module7.sh --i2c
./scripts/module7.sh --vip
./scripts/module7.sh --best-practices

# Combine options
./scripts/module7.sh --dma --uart --pyuvm-tests
```

### Running Individual Examples

#### Direct Execution from Example Directory

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to example directory
cd module7/examples/dma

# Run example
make SIM=verilator TEST=dma_example

# Clean build artifacts
make clean
```

#### Running All Examples Sequentially

```bash
cd module7/examples

# DMA
cd dma && make SIM=verilator TEST=dma_example && cd ..

# UART
cd protocols && make SIM=verilator TEST=uart_example && cd ..

# SPI
cd protocols && make SIM=verilator TEST=spi_example && cd ..

# I2C
cd protocols && make SIM=verilator TEST=i2c_example && cd ..

# VIP
cd vip && make SIM=verilator TEST=vip_example && cd ..

# Best practices
cd best_practices && make SIM=verilator TEST=best_practices_example && cd ..
```

### Running pyuvm Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Change to test directory
cd module7/tests/pyuvm_tests

# Run test
make SIM=verilator TEST=test_real_world

# Clean build artifacts
make clean
```

## Test Results

When tests complete successfully, you should see output similar to:

### Example Test Output

```
** TEST                                        STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** dma_example.test_dma                           PASS         200.00           0.00     123456.78  **
** TESTS=1 PASS=1 FAIL=0 SKIP=0                                 200.00           0.00      12345.67  **
```

### Expected Test Counts

- **DMA example**: 1 test
- **UART example**: 1 test
- **SPI example**: 1 test
- **I2C example**: 1 test
- **VIP example**: 1 test
- **Best practices example**: 1 test
- **Real-world application test**: 1 test
- **Total**: 7 tests across all examples and testbenches

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

#### 3. DMA Transfer Issues

**Error:** DMA transfers don't complete

**Solution:**
- Verify DMA register configuration
- Check DMA start signal assertion
- Verify DMA done signal monitoring
- Ensure transfer length is valid
- Check channel selection

#### 4. UART Protocol Issues

**Error:** UART frames not received correctly

**Solution:**
- Verify baud rate configuration
- Check start/stop bit timing
- Verify parity configuration
- Ensure proper frame synchronization
- Check signal sampling

#### 5. SPI Protocol Issues

**Error:** SPI master-slave communication fails

**Solution:**
- Verify SPI mode configuration
- Check chip select timing
- Verify clock and data synchronization
- Ensure proper master-slave coordination
- Check signal connections

#### 6. I2C Protocol Issues

**Error:** I2C transactions fail

**Solution:**
- Verify START/STOP condition timing
- Check address format (7-bit vs 10-bit)
- Verify ACK/NACK handling
- Ensure proper multi-master coordination
- Check signal connections (open-drain)

#### 7. VIP Configuration Issues

**Error:** VIP doesn't work in passive mode

**Solution:**
- Verify VIP configuration in ConfigDB
- Check active/passive mode settings
- Ensure monitor is always created
- Verify VIP component connections
- Check VIP configuration validation

### Debugging Tips

1. **Check DMA Transfers:**
   ```python
   # Verify DMA configuration
   self.logger.info(f"DMA config: src=0x{src_addr:08X}, dst=0x{src_addr:08X}, len={length}")
   ```

2. **Monitor Protocol Transactions:**
   ```python
   # Add logging in protocol drivers
   self.logger.info(f"Protocol transaction: {txn}")
   ```

3. **Check VIP Configuration:**
   ```python
   # Verify VIP mode
   self.logger.info(f"VIP mode: active={self.active}")
   ```

4. **Inspect Coverage:**
   ```python
   # Check coverage statistics
   self.logger.info(f"Coverage: {self.coverage_data}")
   ```

## Topics Covered

1. **DMA Verification** - Complete DMA controller verification, transfer types, channels
2. **Protocol Verification** - UART, SPI, I2C protocol verification, master-slave coordination
3. **Best Practices** - Code organization, reusability, documentation
4. **VIP Development** - Creating reusable verification IP, active/passive modes
5. **System-Level Verification** - System and SoC verification patterns
6. **Advanced Debugging** - Complex debugging techniques, protocol analysis
7. **Test Planning** - Verification strategy and planning
8. **Industry Patterns** - Common verification patterns, VIP structures
9. **Performance Optimization** - Testbench optimization, efficient protocols
10. **Coverage Closure** - Coverage strategies and closure, functional coverage

## Next Steps

After completing Module 7, proceed to:

- **Module 8**: Advanced Utilities - CLP, comparators, pools, queues, recorders

## Additional Resources

- [pyuvm Documentation](https://pyuvm.readthedocs.io/)
- [UVM User's Guide](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_1.2.pdf)
- [DMA Controller Design](https://en.wikipedia.org/wiki/Direct_memory_access)
- [UART Protocol](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
- [SPI Protocol](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
- [I2C Protocol](https://en.wikipedia.org/wiki/I²C)
- [cocotb Documentation](https://docs.cocotb.org/)
- [Verilator Documentation](https://verilator.org/)

## File Descriptions

### Examples

| File | Description | Tests |
|------|-------------|-------|
| `dma_example.py` | DMA controller verification | 1 test function |
| `uart_example.py` | UART protocol verification | 1 test function |
| `spi_example.py` | SPI protocol verification | 1 test function |
| `i2c_example.py` | I2C protocol verification | 1 test function |
| `vip_example.py` | VIP development | 1 test function |
| `best_practices_example.py` | Best practices demonstration | 1 test function |

### DUT Modules

| File | Description | Ports |
|------|-------------|-------|
| `simple_dma.v` | Simple DMA controller | `clk`, `rst_n`, `dma_start`, `dma_done`, `dma_src_addr[31:0]`, `dma_dst_addr[31:0]`, `dma_length[15:0]`, `dma_channel[2:0]` |
| `uart.v` | UART transmitter/receiver | `clk`, `rst_n`, `tx`, `rx`, `tx_data[7:0]`, `tx_start`, `tx_busy`, `rx_data[7:0]`, `rx_ready` |

### Testbenches

| File | Framework | Description | Tests |
|------|-----------|-------------|-------|
| `test_real_world.py` | pyuvm | Real-world application test | 1 UVM test |

---

For questions or issues, refer to the main project README or check the test logs for detailed error messages.