# Module 6: Complex Testbenches

**Goal**: Build complex multi-agent testbenches with protocol verification

## Overview

This module focuses on building complex verification environments with multiple agents, protocol verification, advanced testbench architecture, and debugging techniques. You'll learn industry patterns and best practices.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module6/` directory:

```
module6/
├── examples/              # pyuvm examples for each topic
│   ├── multi_agent/      # Multi-agent environment examples
│   ├── protocol/         # Protocol verification examples
│   ├── protocol_checkers/# Protocol checker examples
│   ├── scoreboards/      # Multi-channel scoreboard examples
│   └── architecture/     # Testbench architecture examples
├── dut/                   # Verilog Design Under Test modules
│   └── protocols/        # Protocol modules for testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── README.md             # Module 6 documentation
```

### Quick Start

**Run all examples using the orchestrator script:**
```bash
# Run all examples
./scripts/module6.sh

# Run specific examples
./scripts/module6.sh --multi-agent
./scripts/module6.sh --protocol
./scripts/module6.sh --protocol-checkers
./scripts/module6.sh --scoreboards
./scripts/module6.sh --architecture
./scripts/module6.sh --pyuvm-tests
```

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run pyuvm tests
cd module6/tests/pyuvm_tests
make SIM=verilator TEST=test_complex_testbench

# Examples are pyuvm structural examples
# They can be imported and used in your testbenches
```

## Topics Covered

### 1. Multi-Agent Environments

- **Environment Architecture**
  - Multiple agent coordination
  - Agent communication
  - Environment hierarchy
  - Environment patterns

- **Agent Coordination**
  - Master-slave agents
  - Peer-to-peer agents
  - Multi-channel agents
  - Agent synchronization

- **Environment Patterns**
  - Layered environments
  - Hierarchical environments
  - Flat environments
  - Mixed environments

### 2. Protocol Verification

- **Protocol Verification Overview**
  - What is protocol verification?
  - Protocol compliance
  - Protocol checking
  - Protocol coverage

- **AXI Protocol Verification**
  - AXI protocol basics
  - AXI4-Lite agent
  - AXI4 agent
  - AXI protocol checker

- **Custom Protocol Verification**
  - Protocol definition
  - Protocol agent creation
  - Protocol checker implementation
  - Protocol coverage

- **Protocol Checkers**
  - Checker implementation
  - Protocol rule checking
  - Error detection
  - Protocol compliance

### 3. Testbench Architecture Patterns

- **Layered Testbench**
  - Abstraction layers
  - Layer communication
  - Layer organization
  - Layer patterns

- **Reusable Components**
  - Component design
  - Component reuse
  - Component libraries
  - Component patterns

- **Testbench Templates**
  - Standard templates
  - Template customization
  - Template patterns
  - Template best practices

### 4. Debugging and Analysis

- **UVM Debugging Techniques**
  - Phase debugging
  - Component debugging
  - Transaction debugging
  - Configuration debugging

- **Transaction Recording**
  - Transaction logging
  - Transaction tracing
  - Transaction replay
  - Transaction analysis

- **Waveform Analysis**
  - VCD/FST generation
  - Waveform viewing
  - Signal tracing
  - Timing analysis

- **Log Analysis**
  - Log parsing
  - Error analysis
  - Performance analysis
  - Coverage analysis

### 5. Multi-Channel Verification

- **Channel Coordination**
  - Multiple channels
  - Channel synchronization
  - Channel independence
  - Channel patterns

- **Bidirectional Interfaces**
  - Master-slave interfaces
  - Bidirectional agents
  - Interface coordination
  - Interface patterns

### 6. Performance Verification

- **Performance Monitoring**
  - Performance metrics
  - Performance collection
  - Performance analysis
  - Performance reporting

- **Throughput Analysis**
  - Throughput measurement
  - Bandwidth analysis
  - Latency measurement
  - Performance optimization

### 7. Error Injection and Recovery

- **Error Injection**
  - Error scenarios
  - Error injection mechanisms
  - Error patterns
  - Error testing

- **Recovery Testing**
  - Recovery scenarios
  - Recovery verification
  - Recovery patterns
  - Recovery testing

### 8. Testbench Integration

- **Component Integration**
  - Integration strategies
  - Integration testing
  - Integration patterns
  - Integration best practices

- **System Integration**
  - System-level integration
  - Integration verification
  - Integration patterns
  - Integration challenges

### 9. Advanced Scoreboarding

- **Multi-Channel Scoreboards**
  - Multiple channel checking
  - Channel coordination
  - Scoreboard patterns
  - Scoreboard optimization

- **Time-Based Matching**
  - Temporal matching
  - Time windows
  - Matching algorithms
  - Matching patterns

### 10. Testbench Maintenance

- **Code Organization**
  - File organization
  - Class organization
  - Namespace management
  - Documentation

- **Version Control**
  - Git workflows
  - Branching strategies
  - Code review
  - Release management

## Learning Outcomes

By the end of this module, you should be able to:

- Design multi-agent environments
- Implement protocol verification
- Apply testbench architecture patterns
- Debug complex testbenches
- Analyze simulation results
- Coordinate multiple channels
- Monitor performance
- Integrate components
- Maintain testbenches
- Apply industry best practices

## Test Cases

### Test Case 6.1: Multi-Agent Environment
**Objective**: Create environment with multiple agents

**Topics**:
- Multiple agents
- Agent coordination
- Environment structure

#### Example 6.1: Multi-Agent Environment (`module6/examples/multi_agent/multi_agent_example.py`)

**What it demonstrates:**
- **Multiple Agent Instantiation**: Creating multiple agents in environment
- **Agent Coordination**: Coordinating sequences across multiple agents
- **Virtual Sequence**: Using virtual sequence to coordinate agents
- **Multi-Channel Scoreboard**: Scoreboard receiving from multiple agents
- **Environment Hierarchy**: Organizing multiple agents in environment
- **Parallel Agent Execution**: Running sequences on multiple agents concurrently

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --multi-agent

# Or directly (syntax check)
cd module6/examples/multi_agent
python3 -c "import pyuvm; exec(open('multi_agent_example.py').read())"
```

**Expected Output:**
```
============================================================
Multi-Agent Environment Example Test
============================================================
Building MultiAgentEnv
Building agent 0
Building agent 1
Building agent 2
[VirtualSequence] Starting multi-agent coordination
[seq_agent_0] Starting sequence for agent 0
[seq_agent_1] Starting sequence for agent 1
[seq_agent_2] Starting sequence for agent 2
...
[VirtualSequence] Multi-agent coordination completed
```

**Key Concepts:**
- **Multiple Agents**: Create multiple agent instances in environment
- **Agent Coordination**: Use virtual sequences to coordinate agents
- **Virtual Sequence**: Sequence that coordinates multiple sequencers
- **Multi-Channel Scoreboard**: Scoreboard with multiple analysis ports
- **Environment Organization**: Structure environment for multiple agents
- **Parallel Execution**: Run sequences on multiple agents concurrently

### Test Case 6.2: AXI4-Lite Agent
**Objective**: Create AXI4-Lite verification agent

**Topics**:
- AXI protocol
- Protocol agent
- Protocol checker

#### Example 6.2: Protocol Verification (`module6/examples/protocol/protocol_example.py`)

**What it demonstrates:**
- **AXI4-Lite Protocol**: Implementing AXI4-Lite write and read protocols
- **Protocol Driver**: Driver implementing AXI4-Lite handshaking
- **Protocol Monitor**: Monitor sampling AXI4-Lite signals
- **Write Protocol**: Write address, data, and response channels
- **Read Protocol**: Read address and data channels
- **Protocol Agent**: Complete agent for AXI4-Lite verification

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --protocol

# Or directly
cd module6/examples/protocol
python3 -c "import pyuvm; exec(open('protocol_example.py').read())"
```

**Expected Output:**
```
============================================================
AXI4-Lite Protocol Example Test
============================================================
Building AXI4LiteEnv
Building AXI4-Lite agent
[driver] Building AXI4-Lite driver
[monitor] Building AXI4-Lite monitor
[driver] Starting AXI4-Lite driver
[driver] AXI4-Lite Write: WRITE: addr=0x00001000, data=0xDEADBEEF
[driver] Write address channel: addr=0x00001000
[driver] Write data channel: data=0xDEADBEEF
[driver] Write response: OKAY
```

**Key Concepts:**
- **AXI4-Lite Protocol**: Simplified AXI protocol with 5 channels
- **Write Channels**: AW (address), W (data), B (response)
- **Read Channels**: AR (address), R (data)
- **Handshaking**: Valid/ready handshaking on each channel
- **Protocol Implementation**: Implement protocol timing in driver
- **Protocol Monitoring**: Sample protocol signals in monitor

### Test Case 6.3: Protocol Checker
**Objective**: Implement protocol compliance checker

**Topics**:
- Protocol rules
- Checker implementation
- Error detection

#### Example 6.3: Protocol Checker (`module6/examples/protocol_checkers/protocol_checker_example.py`)

**What it demonstrates:**
- **Protocol Rules**: Defining protocol compliance rules
- **Rule Checking**: Checking protocol rules in real-time
- **Error Detection**: Detecting protocol violations
- **Warning Detection**: Detecting protocol warnings
- **Compliance Reporting**: Reporting protocol compliance status
- **State Tracking**: Tracking protocol state for rule checking

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --protocol-checkers

# Or directly
cd module6/examples/protocol_checkers
python3 -c "import pyuvm; exec(open('protocol_checker_example.py').read())"
```

**Expected Output:**
```
============================================================
Protocol Checker Example Test
============================================================
Building ProtocolEnv
[checker] Checking: valid=False, ready=False, data=0x00
[checker] Warning: valid asserted without ready at time 10
[checker] Protocol OK: Valid handshake, data=0xBB
[checker] Warning: valid asserted without ready at time 40
[checker] Protocol OK: Valid handshake, data=0xEE
============================================================
[checker] Protocol Checker Report
============================================================
Total errors: 0
Total warnings: 2
✓ Protocol compliance: PASSED
```

**Key Concepts:**
- **Protocol Rules**: Define rules for protocol compliance
- **State Tracking**: Track previous state for rule checking
- **Error Detection**: Detect and report protocol violations
- **Warning Detection**: Detect and report protocol warnings
- **Compliance Checking**: Check compliance in real-time
- **Compliance Reporting**: Report compliance in check_phase

### Test Case 6.4: Multi-Channel Scoreboard
**Objective**: Implement multi-channel scoreboard

**Topics**:
- Multiple channels
- Channel coordination
- Scoreboard patterns

#### Example 6.4: Multi-Channel Scoreboard (`module6/examples/scoreboards/multi_channel_scoreboard_example.py`)

**What it demonstrates:**
- **Multiple Channels**: Scoreboard handling multiple channels
- **Channel-Specific Analysis Ports**: Separate analysis ports for each channel
- **Channel Coordination**: Coordinating checking across channels
- **Channel-Specific Matching**: Matching expected vs actual per channel
- **Channel Statistics**: Reporting statistics per channel
- **Multi-Channel Patterns**: Patterns for multi-channel scoreboarding

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --scoreboards

# Or directly
cd module6/examples/scoreboards
python3 -c "import pyuvm; exec(open('multi_channel_scoreboard_example.py').read())"
```

**Expected Output:**
```
============================================================
Multi-Channel Scoreboard Example Test
============================================================
[scoreboard] Building multi-channel scoreboard (3 channels)
[monitor_channel_0] Starting monitor for channel 0
[monitor_channel_1] Starting monitor for channel 1
[monitor_channel_2] Starting monitor for channel 2
[scoreboard] Received from channel 0: channel=0, data=0x00, ...
[scoreboard] Channel 0 match: expected=0x00, actual=0x00
============================================================
[scoreboard] Multi-Channel Scoreboard Check
============================================================
Channel 0:
  Expected: 0 remaining
  Actual: 5
  Matches: 5
  Mismatches: 0
...
✓ All channels: PASSED
```

**Key Concepts:**
- **Multiple Channels**: Handle transactions from multiple channels
- **Channel-Specific Ports**: Create analysis ports for each channel
- **Channel Matching**: Match expected vs actual per channel
- **Channel Statistics**: Track statistics per channel
- **Channel Coordination**: Coordinate checking across channels
- **Multi-Channel Patterns**: Reusable patterns for multi-channel scoreboarding

#### Example 6.5: Testbench Architecture (`module6/examples/architecture/architecture_example.py`)

**What it demonstrates:**
- **Layered Architecture**: Implementing layered testbench architecture
- **Layer Communication**: Communication between abstraction layers
- **Reusable Components**: Creating reusable, parameterized components
- **Component Patterns**: Patterns for component reuse
- **Architecture Patterns**: Standard testbench architecture patterns

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --architecture

# Or directly
cd module6/examples/architecture
python3 -c "import pyuvm; exec(open('architecture_example.py').read())"
```

**Key Concepts:**
- **Layered Architecture**: Organize testbench into abstraction layers
- **Layer Communication**: Use analysis ports for layer communication
- **Reusable Components**: Design components for reuse
- **Component Parameterization**: Use configuration for component customization
- **Architecture Patterns**: Apply standard architecture patterns

#### Test: Complex Testbench Test (`module6/tests/pyuvm_tests/test_complex_testbench.py`)

**What it demonstrates:**
- Complete complex testbench structure
- Multi-agent integration
- Protocol verification
- Scoreboard integration
- Full test flow

**Execution:**
```bash
# Using orchestrator script
./scripts/module6.sh --pyuvm-tests

# Or manually
cd module6/tests/pyuvm_tests
make SIM=verilator TEST=test_complex_testbench
```

**Test Structure:**
- `ComplexTransaction`: Transaction for complex testbench
- `ComplexSequence`: Generates test vectors
- `ComplexDriver`: Drives transactions
- `ComplexMonitor`: Monitors DUT
- `ComplexScoreboard`: Checks results
- `ComplexAgent`: Contains driver, monitor, sequencer
- `ComplexEnv`: Contains agent and scoreboard
- `ComplexTestbenchTest`: Top-level test class

### Design Under Test (DUT) Modules

#### AXI4-Lite Slave (`module6/dut/protocols/axi4_lite_slave.v`)
- **Purpose**: AXI4-Lite slave for protocol verification
- **Used in**: Protocol verification examples
- **Features**: Full AXI4-Lite implementation with all 5 channels, memory interface

## Exercises

1. **Multi-Agent Environment**
   - Design environment
   - Implement agents
   - Coordinate agents
   - **Location**: Extend `module6/examples/multi_agent/multi_agent_example.py`
   - **Hint**: Add more agents and coordinate them with virtual sequences

2. **Protocol Verification**
   - Choose protocol
   - Create agent
   - Implement checker
   - **Location**: Extend `module6/examples/protocol/protocol_example.py`
   - **Hint**: Add more protocol rules and implement full AXI4-Lite protocol

3. **Testbench Architecture**
   - Design architecture
   - Implement patterns
   - Organize code
   - **Location**: Extend `module6/examples/architecture/architecture_example.py`
   - **Hint**: Add more layers and implement reusable component library

4. **Debugging**
   - Add debugging
   - Analyze results
   - Fix issues
   - **Location**: Add to existing examples
   - **Hint**: Add transaction logging and waveform generation

5. **Performance Analysis**
   - Monitor performance
   - Analyze metrics
   - Optimize
   - **Location**: Create new example
   - **Hint**: Add performance monitoring components

## Assessment

- [ ] Can design multi-agent environments
- [ ] Can implement protocol verification
- [ ] Understands architecture patterns
- [ ] Can debug complex testbenches
- [ ] Can analyze simulation results
- [ ] Can coordinate multiple channels
- [ ] Can monitor performance
- [ ] Can integrate components
- [ ] Can maintain testbenches
- [ ] Understands best practices

## Next Steps

After completing this module, proceed to [Module 7: Real-World Applications](MODULE7.md) to apply UVM to real-world verification scenarios.

## Additional Resources

- **pyuvm Documentation**: https://pyuvm.readthedocs.io/
- **UVM 1.2 User's Guide**: Accellera Systems Initiative
- **Advanced UVM**: Ray Salemi
- **AXI Protocol Specification**: ARM AMBA Specification
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

**Issue: Multi-agent coordination not working**
```bash
# Solution: Ensure virtual sequence has references to all sequencers
# Set sequencer references: virtual_seq.agent_seqrs = [agent.seqr for agent in env.agents]
# Use cocotb.start_soon() for parallel execution
```

**Issue: Protocol checker not detecting violations**
```bash
# Solution: Check protocol rules are correctly implemented
# Ensure state tracking is correct
# Verify checker receives transactions from monitor
```

**Issue: Multi-channel scoreboard not receiving from all channels**
```bash
# Solution: Check analysis port connections
# Ensure: monitor.ap.connect(scoreboard.analysis_exports[channel_id])
# Verify write() method handles channel_id parameter
```

**Issue: AXI protocol implementation errors**
```bash
# Solution: Review AXI4-Lite specification
# Ensure proper handshaking on all channels
# Check signal timing and sequencing
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module6/README.md` for directory structure
- Run examples individually to understand each complex pattern
- Study multi-agent coordination in `multi_agent_example.py`
- Review protocol implementation in `protocol_example.py`
- Check AXI protocol specification for protocol details

### Summary of Examples and Tests

**Examples (pyuvm structural examples in `module6/examples/`):**
1. **Example 6.1: Multi-Agent Environment** (`multi_agent/`) - Multiple agent coordination
2. **Example 6.2: Protocol Verification** (`protocol/`) - AXI4-Lite protocol implementation
3. **Example 6.3: Protocol Checker** (`protocol_checkers/`) - Protocol compliance checking
4. **Example 6.4: Multi-Channel Scoreboard** (`scoreboards/`) - Multi-channel scoreboarding
5. **Example 6.5: Testbench Architecture** (`architecture/`) - Layered and reusable patterns

**Testbenches (runnable tests in `module6/tests/pyuvm_tests/`):**
1. **Complex Testbench Test** (`test_complex_testbench.py`) - Complete complex testbench

**DUT Modules (in `module6/dut/`):**
1. **AXI4-Lite Slave** (`protocols/axi4_lite_slave.v`) - AXI4-Lite slave for protocol verification

**Coverage:**
- ✅ Multi-agent environment design
- ✅ Protocol verification (AXI4-Lite)
- ✅ Protocol compliance checking
- ✅ Multi-channel scoreboarding
- ✅ Testbench architecture patterns
- ✅ Complex testbench integration

