# Python and Verilog Interaction in Hardware Verification

**A Fundamental Guide to Understanding How Python Testbenches Control Verilog Hardware**

## Overview

This document explains the fundamental concept of how Python and Verilog work together in hardware verification using Cocotb. Understanding this interaction is crucial for mastering hardware verification with PyUVM and Cocotb.

## Table of Contents

1. [The Two-Layer Architecture](#the-two-layer-architecture)
2. [The Bridge: Cocotb](#the-bridge-cocotb)
3. [Signal Flow and Interaction](#signal-flow-and-interaction)
4. [Time Synchronization](#time-synchronization)
5. [Complete Example Walkthrough](#complete-example-walkthrough)
6. [Key Concepts Summary](#key-concepts-summary)
7. [Common Patterns](#common-patterns)

## The Two-Layer Architecture

Hardware verification with Cocotb uses a **two-layer architecture**:

### 1. Verilog Layer (Hardware Design)

The **Verilog layer** contains the actual hardware design - the circuit you want to verify. This is called the **Design Under Test (DUT)**.

**Example: Simple Register (`module2/dut/registers/simple_register.v`)**

```verilog
module simple_register (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       enable,
    input  wire [7:0] d,
    output reg  [7:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q <= 8'h00;
        end else if (enable) begin
            q <= d;
        end
    end

endmodule
```

**What the Verilog does:**
- Defines hardware ports (inputs and outputs)
- Implements hardware behavior (registers, logic, state machines)
- Responds to clock edges and input changes
- Operates in **simulation time** (nanoseconds, picoseconds)

### 2. Python Layer (Testbench)

The **Python layer** contains the testbench code that:
- **Controls** the hardware (drives inputs)
- **Monitors** the hardware (reads outputs)
- **Verifies** correctness (assertions, checks)
- **Orchestrates** test scenarios

**Example: Clock Generation Test (`module2/examples/clock_generation/clock_generation_example.py`)**

```python
@cocotb.test()
async def test_clock_class(dut):
    """
    Demonstrates using Clock class.
    """
    # Create clock with 10ns period
    clock = Clock(dut.clk, 10, units="ns")
    
    # Start clock
    cocotb.start_soon(clock.start())
    
    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.clk)
        print(f"Clock cycle {i+1}")
```

**What the Python does:**
- Generates test stimuli (clocks, data, control signals)
- Reads hardware outputs
- Checks results against expected values
- Coordinates test execution

## The Bridge: Cocotb

**Cocotb** is the bridge that connects Python and Verilog. It provides:

1. **Signal Access**: Python can read/write Verilog signals
2. **Time Synchronization**: Python and Verilog share the same simulation time
3. **Event Coordination**: Python can wait for Verilog events (clock edges, timeouts)

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│  Python Testbench                      │
│  - Generates clock signals             │
│  - Drives inputs (d, enable, rst_n)    │
│  - Monitors outputs (q)                │
│  - Checks correctness                  │
└──────────────┬──────────────────────────┘
               │
               │ Cocotb Bridge
               │ (dut.clk, dut.d, dut.q)
               │
┌──────────────▼──────────────────────────┐
│  Verilog DUT (simple_register)         │
│  - Receives clock on clk port          │
│  - Processes data on clock edges       │
│  - Outputs q register value            │
└─────────────────────────────────────────┘
```

### The Makefile Connection

The Makefile connects everything together:

```makefile
# Python test file
PYTHON_FILES = clock_generation_example.py

# Verilog files
VERILOG_SOURCES = ../../dut/registers/simple_register.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = clock_generation_example
TOPLEVEL = simple_register
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim
```

**What happens when you run `make`:**
1. **Compiles Verilog** → Creates simulation model (via Verilator or other simulator)
2. **Loads Python** → Imports the testbench module
3. **Connects them** → Cocotb creates the `dut` object that bridges Python and Verilog
4. **Runs simulation** → Python and Verilog execute together, synchronized in time

## Signal Flow and Interaction

### 1. Clock Generation (Python → Verilog)

**Python generates clock signals that drive Verilog:**

```python
# Python creates a clock signal
clock = Clock(dut.clk, 10, units="ns")  # 10ns period = 100MHz
cocotb.start_soon(clock.start())       # Start clock in background
```

**What happens:**
- Python creates a coroutine that toggles `dut.clk` every 5ns
- The Verilog `always @(posedge clk)` block reacts to these clock edges
- Clock runs in the background while Python test code continues

**Verilog receives the clock:**
```verilog
always @(posedge clk or negedge rst_n) begin
    // This block executes when Python drives clk from 0→1
    if (!rst_n) begin
        q <= 8'h00;
    end else if (enable) begin
        q <= d;
    end
end
```

### 2. Driving Inputs (Python → Verilog)

**Python drives Verilog input ports:**

```python
dut.d.value = 0xAB        # Python drives data input
dut.enable.value = 1       # Python drives enable signal
dut.rst_n.value = 0        # Python drives reset
```

**What happens:**
- Python assignments directly control Verilog input ports
- Changes are visible immediately in Verilog
- Verilog logic processes these inputs on clock edges

**Verilog receives the inputs:**
```verilog
input  wire [7:0] d,      // Receives dut.d.value from Python
input  wire       enable, // Receives dut.enable.value from Python
input  wire       rst_n   // Receives dut.rst_n.value from Python
```

### 3. Reading Outputs (Verilog → Python)

**Python reads Verilog output ports:**

```python
await RisingEdge(dut.clk)  # Wait for clock edge
value = dut.q.value       # Read output from Verilog
assert value == expected  # Check correctness
```

**What happens:**
- Python can read Verilog output signals at any time
- Values reflect the current state of the Verilog design
- Python uses these values for verification

**Verilog drives the outputs:**
```verilog
output reg [7:0] q  // Python reads this via dut.q.value
```

## Time Synchronization

**Python and Verilog share the same simulation time.** This is crucial for correct verification.

### Simulation Time

Both Python and Verilog operate in **simulation time** (not real time):
- Time units: nanoseconds (ns), picoseconds (ps)
- Time advances only when explicitly requested
- Python controls time advancement

### Time Control in Python

```python
await Timer(10, units="ns")      # Advance time by 10ns
await RisingEdge(dut.clk)        # Wait until next clock rising edge
await FallingEdge(dut.clk)       # Wait until next clock falling edge
```

**What happens:**
- `await` pauses Python execution
- Simulation time advances
- Verilog processes events during this time
- Python resumes when the condition is met

### Example: Time Synchronization

```python
# Time: 0ns
dut.d.value = 0x11
dut.enable.value = 1

# Time: 0ns (still) - inputs set, but no clock edge yet
await RisingEdge(dut.clk)  # Wait for clock edge

# Time: 5ns - clock rising edge occurs
# Verilog: q <= d (register updates)
await Timer(1, units="ns")  # Wait 1ns for propagation

# Time: 6ns - output is stable
assert dut.q.value == 0x11  # Check the result
```

## Complete Example Walkthrough

Let's trace through a complete example to see how everything works together.

### Step 1: Compilation (Makefile)

```bash
make SIM=verilator
```

**What happens:**
1. Verilator compiles `simple_register.v` → creates C++ simulation model
2. Cocotb compiles Python extensions → creates bridge library
3. Everything is linked together → creates executable simulation

### Step 2: Test Execution Starts

```python
@cocotb.test()
async def test_clock_class(dut):
    # 'dut' is automatically created by Cocotb
    # It's a handle to the Verilog module instance
```

**What `dut` is:**
- `dut` is a Python object that represents the Verilog module
- `dut.clk` accesses the `clk` port in Verilog
- `dut.d` accesses the `d` port in Verilog
- `dut.q` accesses the `q` port in Verilog

### Step 3: Clock Generation

```python
clock = Clock(dut.clk, 10, units="ns")
cocotb.start_soon(clock.start())
```

**What happens:**
1. Python creates a Clock object targeting `dut.clk`
2. Clock coroutine starts running in background
3. Every 5ns, it toggles `dut.clk` (0→1→0→1...)
4. Verilog `always @(posedge clk)` blocks react to these edges

**Timeline:**
```
Time: 0ns   → dut.clk = 0
Time: 5ns   → dut.clk = 1 (rising edge - Verilog processes)
Time: 10ns  → dut.clk = 0
Time: 15ns  → dut.clk = 1 (rising edge - Verilog processes)
Time: 20ns  → dut.clk = 0
...
```

### Step 4: Test Logic

```python
for i in range(5):
    await RisingEdge(dut.clk)
    print(f"Clock cycle {i+1}")
```

**What happens:**
1. Python waits for clock rising edge (pauses execution)
2. When edge occurs, Python resumes
3. Prints message
4. Repeats 5 times

**Synchronization:**
- Python waits for Verilog clock edge
- Both are synchronized at the same simulation time
- Python can read Verilog state immediately after edge

## Key Concepts Summary

### The `dut` Object

The `dut` parameter in test functions is a **handle to the Verilog module**:

```python
@cocotb.test()
async def my_test(dut):
    # dut is the Verilog module instance
    dut.clk      # Access clk port
    dut.d        # Access d port
    dut.q        # Access q port
    dut.enable   # Access enable port
```

**Key points:**
- Created automatically by Cocotb
- Provides bidirectional access (read/write)
- Synchronized with Verilog simulation

### Signal Access

**Reading signals:**
```python
value = dut.q.value           # Read current value
int_value = dut.q.value.integer  # Convert to integer
hex_value = f"0x{dut.q.value.integer:02X}"  # Format as hex
```

**Writing signals:**
```python
dut.d.value = 0xAB           # Assign integer
dut.enable.value = 1          # Assign single bit
dut.rst_n.value = 0           # Assign single bit
```

### Time Control

**Advancing time:**
```python
await Timer(10, units="ns")   # Wait 10 nanoseconds
```

**Waiting for events:**
```python
await RisingEdge(dut.clk)     # Wait for clock rising edge
await FallingEdge(dut.clk)     # Wait for clock falling edge
```

**Combining time and events:**
```python
await RisingEdge(dut.clk)      # Wait for edge
await Timer(1, units="ns")    # Wait 1ns for propagation
# Now read outputs
```

### Concurrent Execution

**Multiple coroutines can run simultaneously:**

```python
# Start clock in background
cocotb.start_soon(clock.start())

# Start reset sequence in background
cocotb.start_soon(reset_sequence(dut))

# Main test continues
await Timer(100, units="ns")
```

**This simulates parallel hardware behavior:**
- Clock runs continuously
- Reset sequence executes independently
- Test logic coordinates everything

## Common Patterns

### Pattern 1: Clock and Reset Setup

```python
@cocotb.test()
async def test_with_reset(dut):
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Apply reset
    dut.rst_n.value = 0
    await Timer(20, units="ns")
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    
    # Now test logic
    dut.d.value = 0x42
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    assert dut.q.value == 0x42
```

### Pattern 2: Driving and Sampling

```python
@cocotb.test()
async def test_drive_and_sample(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Drive inputs
    dut.d.value = 0xAA
    dut.enable.value = 1
    
    # Wait for clock edge (register updates)
    await RisingEdge(dut.clk)
    
    # Wait for propagation delay
    await Timer(1, units="ns")
    
    # Sample output
    assert dut.q.value == 0xAA
```

### Pattern 3: Multiple Clock Cycles

```python
@cocotb.test()
async def test_multiple_cycles(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.enable.value = 1
    
    for i in range(10):
        dut.d.value = i
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.q.value == i
```

### Pattern 4: Background Processes

```python
async def monitor_output(dut):
    """Monitor output in background"""
    while True:
        await RisingEdge(dut.clk)
        print(f"Output: 0x{dut.q.value.integer:02X}")

@cocotb.test()
async def test_with_monitor(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    cocotb.start_soon(monitor_output(dut))
    
    # Test logic runs while monitor observes
    for i in range(5):
        dut.d.value = i * 0x11
        await RisingEdge(dut.clk)
```

## Understanding the Flow

When you run a Cocotb test, here's the complete flow:

1. **Makefile Execution**
   - Compiles Verilog → simulation model
   - Prepares Cocotb bridge
   - Links everything together

2. **Simulation Starts**
   - Python interpreter loads testbench
   - Cocotb loads compiled Verilog
   - Creates `dut` object connecting them

3. **Test Execution**
   - Python test function runs
   - Python drives inputs via `dut.signal.value`
   - Python generates clocks via `Clock` class
   - Verilog processes inputs on clock edges
   - Python reads outputs via `dut.signal.value`
   - Python verifies correctness

4. **Time Advancement**
   - Python controls time via `await Timer()`
   - Python waits for events via `await RisingEdge()`
   - Verilog and Python stay synchronized
   - Both operate in the same simulation time

5. **Test Completion**
   - Python assertions verify results
   - Test passes or fails
   - Simulation ends

## Key Takeaways

1. **Verilog = Hardware**: The actual circuit being tested
2. **Python = Testbench**: Controls and verifies the hardware
3. **Cocotb = Bridge**: Connects Python and Verilog
4. **`dut` = Handle**: Python object that accesses Verilog ports
5. **Time is Shared**: Python and Verilog operate in the same simulation time
6. **Signals are Bidirectional**: Python can read and write Verilog signals
7. **Events Synchronize**: Python can wait for Verilog events (clock edges)

## Related Documentation

- [Module 2: cocotb Fundamentals](MODULE2.md) - Detailed Cocotb concepts
- [Module 1: Python and Verification Basics](MODULE1.md) - Python for verification
- [Module 0: Installation and Setup](MODULE0.md) - Setting up the environment

## Examples in This Project

- **Clock Generation**: `module2/examples/clock_generation/clock_generation_example.py`
- **Signal Access**: `module2/examples/signal_access/signal_access_example.py`
- **Reset Patterns**: `module2/examples/reset_patterns/reset_patterns_example.py`
- **Basic Tests**: `module1/tests/cocotb_tests/test_and_gate.py`

## Further Reading

- [Cocotb Documentation](https://docs.cocotb.org/) - Official Cocotb docs
- [PyUVM Documentation](https://pyuvm.readthedocs.io/) - PyUVM framework
- [Verilator Documentation](https://verilator.org/) - Verilator simulator

---

**Remember**: Understanding how Python and Verilog interact is fundamental to hardware verification. The `dut` object is your window into the Verilog world, and Cocotb keeps everything synchronized in simulation time.

