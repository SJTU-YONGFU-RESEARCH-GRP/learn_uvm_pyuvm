# Module 3: UVM Basics

**Goal**: Master UVM class hierarchy and phases

## Overview

This module introduces the Universal Verification Methodology (UVM) and its implementation in pyuvm. You'll learn the fundamental UVM concepts, class hierarchy, phases, and how to structure UVM testbenches.

### Examples and Code Structure

This module includes comprehensive examples and testbenches located in the `module3/` directory:

```
module3/
├── examples/              # pyuvm examples for each topic
│   ├── class_hierarchy/   # UVM class hierarchy examples
│   ├── phases/           # UVM phases examples
│   ├── reporting/        # UVM reporting examples
│   ├── configdb/         # ConfigDB examples
│   ├── factory/          # Factory pattern examples
│   └── objections/       # Objection mechanism examples
├── dut/                   # Verilog Design Under Test modules
│   └── simple_blocks/     # Simple blocks for UVM testing
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── README.md             # Module 3 documentation
```

### Quick Start

**Run all examples using the orchestrator script:**
```bash
# Run all examples
./scripts/module3.sh

# Run specific examples
./scripts/module3.sh --class-hierarchy
./scripts/module3.sh --phases
./scripts/module3.sh --reporting
./scripts/module3.sh --configdb
./scripts/module3.sh --factory
./scripts/module3.sh --objections
./scripts/module3.sh --pyuvm-tests
```

**Run examples individually:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Run pyuvm tests
cd module3/tests/pyuvm_tests
make SIM=verilator TEST=test_simple_uvm

# Examples are pyuvm structural examples
# They can be imported and used in your testbenches
```

## Topics Covered

### 1. Introduction to UVM

- **What is UVM?**
  - Universal Verification Methodology
  - Industry standard for verification
  - Methodology vs library
  - History and evolution

- **Why UVM?**
  - Reusability
  - Standardization
  - Scalability
  - Maintainability

- **UVM in Python (pyuvm)**
  - Python implementation of UVM 1.2
  - Advantages over SystemVerilog UVM
  - Compatibility and features

### 2. UVM Class Hierarchy

- **Base Classes**
  - `uvm_object` - Base for all UVM objects
  - `uvm_component` - Base for all UVM components
  - Differences and use cases

- **Component Classes**
  - `uvm_test` - Top-level test class
  - `uvm_env` - Environment container
  - `uvm_agent` - Agent (driver, monitor, sequencer)
  - `uvm_driver` - Drives transactions to DUT
  - `uvm_monitor` - Monitors DUT signals
  - `uvm_sequencer` - Manages sequences
  - `uvm_scoreboard` - Checks results

- **Object Classes**
  - `uvm_sequence_item` - Transaction objects
  - `uvm_sequence` - Sequence of transactions
  - `uvm_config_object` - Configuration objects

- **Class Relationships**
  - Inheritance hierarchy
  - Composition patterns
  - Factory pattern

### 3. UVM Phases

- **Phase Overview**
  - Why phases exist
  - Phase execution order
  - Phase synchronization
  - Phase types

- **Build Phases**
  - `build_phase()` - Component construction
  - `connect_phase()` - Component connections
  - `end_of_elaboration_phase()` - Final setup

- **Run Phases**
  - `run_phase()` - Main test execution
  - `pre_reset_phase()` - Before reset
  - `reset_phase()` - Reset sequence
  - `post_reset_phase()` - After reset
  - `pre_configure_phase()` - Before configuration
  - `configure_phase()` - Configuration
  - `post_configure_phase()` - After configuration
  - `pre_main_phase()` - Before main test
  - `main_phase()` - Main test execution
  - `post_main_phase()` - After main test
  - `pre_shutdown_phase()` - Before shutdown
  - `shutdown_phase()` - Shutdown sequence
  - `post_shutdown_phase()` - After shutdown

- **Cleanup Phases**
  - `extract_phase()` - Extract results
  - `check_phase()` - Final checks
  - `report_phase()` - Generate reports
  - `final_phase()` - Final cleanup

- **Phase Implementation**
  - Synchronous phases (build, connect)
  - Asynchronous phases (run phases)
  - Phase methods
  - Phase ordering

### 4. UVM Reporting System

- **Reporting Overview**
  - UVM messaging system
  - Severity levels
  - Verbosity levels
  - Message formatting

- **Severity Levels**
  - `UVM_FATAL` - Fatal errors
  - `UVM_ERROR` - Errors
  - `UVM_WARNING` - Warnings
  - `UVM_INFO` - Informational
  - `UVM_DEBUG` - Debug messages

- **Verbosity Levels**
  - `UVM_NONE` - No messages
  - `UVM_LOW` - Low verbosity
  - `UVM_MEDIUM` - Medium verbosity
  - `UVM_HIGH` - High verbosity
  - `UVM_FULL` - Full verbosity
  - `UVM_DEBUG` - Debug verbosity

- **Using Reporting**
  - `self.logger.info()`
  - `self.logger.warning()`
  - `self.logger.error()`
  - `self.logger.fatal()`
  - Message formatting
  - Verbosity control

### 5. UVM Configuration Database (ConfigDB)

- **ConfigDB Overview**
  - What is ConfigDB?
  - Why use ConfigDB?
  - Configuration hierarchy

- **Setting Configuration**
  - `ConfigDB().set()`
  - Configuration paths
  - Configuration objects
  - Scalar configuration

- **Getting Configuration**
  - `ConfigDB().get()`
  - Configuration lookup
  - Default values
  - Configuration checking

- **Configuration Patterns**
  - Agent configuration
  - Environment configuration
  - Test configuration
  - Hierarchical configuration

### 6. Factory Pattern

- **Factory Overview**
  - What is the factory?
  - Why use factory?
  - Factory benefits

- **Factory Usage**
  - Type registration
  - Object creation
  - Override mechanism
  - Factory patterns

### 7. First UVM Test Class

- **Test Structure**
  - Test class definition
  - Inheriting from `uvm_test`
  - Required methods
  - Test organization

- **Environment Creation**
  - Creating environment
  - Environment hierarchy
  - Component instantiation

- **Test Execution**
  - `run_phase()` implementation
  - Objection mechanism
  - Test flow
  - Completion

### 8. Environment Structure

- **Environment Basics**
  - What is environment?
  - Environment purpose
  - Environment structure

- **Environment Components**
  - Agent instantiation
  - Scoreboard instantiation
  - Coverage instantiation
  - Other components

- **Environment Connections**
  - Component connections
  - Analysis port connections
  - TLM connections

### 9. Objection Mechanism

- **Objections Overview**
  - What are objections?
  - Why objections?
  - Objection lifecycle

- **Using Objections**
  - `raise_objection()`
  - `drop_objection()`
  - Objection timing
  - Multiple objections

- **Objection Patterns**
  - Test objections
  - Sequence objections
  - Component objections
  - Best practices

### 10. UVM Test Execution

- **Test Flow**
  - Test startup
  - Phase execution
  - Test completion
  - Cleanup

- **Running Tests**
  - `uvm_root().run_test()`
  - Test selection
  - Test parameters
  - Test execution

- **Test Organization**
  - Multiple tests
  - Test inheritance
  - Test libraries
  - Test selection

## Learning Outcomes

By the end of this module, you should be able to:

- Understand UVM methodology
- Explain UVM class hierarchy
- Understand and use UVM phases
- Use UVM reporting effectively
- Use ConfigDB for configuration
- Understand factory pattern
- Create UVM test classes
- Structure UVM environments
- Use objection mechanism
- Execute UVM tests

## Test Cases

### Test Case 3.1: Simple UVM Test
**Objective**: Create first UVM test class

**Topics**:
- Test class definition
- Basic phases
- Objection mechanism

#### Example 3.1: Class Hierarchy (`module3/examples/class_hierarchy/class_hierarchy_example.py`)

**What it demonstrates:**
- **uvm_object Hierarchy**: `uvm_sequence_item` for transactions
- **uvm_component Hierarchy**: `uvm_driver`, `uvm_monitor`, `uvm_agent`, `uvm_env`, `uvm_test`
- **Component Composition**: Building hierarchy (Test → Env → Agent → Driver/Monitor)
- **Phase Implementation**: `build_phase()`, `connect_phase()`, `run_phase()`
- **Factory Pattern**: Using `create()` method for component instantiation
- **Component Relationships**: Parent-child relationships in UVM

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --class-hierarchy

# Or directly (syntax check)
cd module3/examples/class_hierarchy
python3 -c "import pyuvm; exec(open('class_hierarchy_example.py').read())"
```

**Expected Output:**
```
============================================================
Building ClassHierarchyTest
============================================================
[BUILD] Building MyEnv
[BUILD] Building MyAgent
[BUILD] Building MyDriver
[BUILD] Building MyMonitor
[CONNECT] Connecting MyAgent
[CONNECT] Connecting MyDriver
Running ClassHierarchyTest
Created transaction: MyTransaction: data=0xAB, addr=0x1000
============================================================
ClassHierarchyTest completed
============================================================
```

**Key Concepts:**
- **`uvm_object`**: Base for all UVM objects (transactions, configs)
- **`uvm_component`**: Base for all UVM components (test, env, agent, driver, monitor)
- **`uvm_test`**: Top-level test class
- **`uvm_env`**: Environment container for agents and other components
- **`uvm_agent`**: Contains driver, monitor, sequencer
- **`create()`**: Factory method for component creation
- **Component Hierarchy**: Test → Env → Agent → Driver/Monitor

### Test Case 3.2: UVM Environment
**Objective**: Create UVM environment

**Topics**:
- Environment structure
- Component instantiation
- Phase implementation

#### Example 3.2: UVM Phases (`module3/examples/phases/phases_example.py`)

**What it demonstrates:**
- **Build Phases**: `build_phase()`, `connect_phase()`, `end_of_elaboration_phase()`
- **Run Phases**: All 12 run phases (pre_reset, reset, post_reset, etc.)
- **Cleanup Phases**: `extract_phase()`, `check_phase()`, `report_phase()`, `final_phase()`
- **Phase Execution Order**: Synchronous phases execute top-down, async phases run concurrently
- **Phase Synchronization**: How phases coordinate across components
- **Phase Implementation**: Implementing all phases in a component

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --phases

# Or directly
cd module3/examples/phases
python3 -c "import pyuvm; exec(open('phases_example.py').read())"
```

**Expected Output:**
```
============================================================
PHASES TEST - Build Phase
============================================================
[BUILD] Building PhasesEnv
[BUILD] Building PhasesComponent
[CONNECT] Connecting PhasesEnv
[END_OF_ELAB] PhasesEnv elaboration complete
[END_OF_ELAB] PhasesComponent: Elaboration complete
PHASES TEST - Run Phase (all run phases execute here)
[PRE_RESET] PhasesComponent: Pre-reset phase
[RESET] PhasesComponent: Reset phase
[POST_RESET] PhasesComponent: Post-reset phase
...
[FINAL] PhasesComponent: Final cleanup
============================================================
PHASES TEST - Report Phase
============================================================
```

**Key Concepts:**
- **Build Phases**: Synchronous, top-down execution
- **Run Phases**: Asynchronous, concurrent execution
- **Cleanup Phases**: Synchronous, bottom-up execution
- **Phase Order**: Build → Connect → End_of_Elab → Run Phases → Extract → Check → Report → Final
- **Synchronous Phases**: Execute in order, one component at a time
- **Asynchronous Phases**: All components run phases concurrently

### Test Case 3.3: UVM Reporting
**Objective**: Use UVM reporting

**Topics**:
- Severity levels
- Verbosity control
- Message formatting

#### Example 3.3: UVM Reporting (`module3/examples/reporting/reporting_example.py`)

**What it demonstrates:**
- **Severity Levels**: `info()`, `warning()`, `error()`, `fatal()`
- **Message Formatting**: Using f-strings and format specifiers
- **Component Context**: Getting component name, type, full name
- **Verbosity Control**: Understanding verbosity levels (LOW, MEDIUM, HIGH, FULL, DEBUG)
- **Hierarchical Reporting**: Messages include component hierarchy
- **Logging Integration**: UVM reporting uses Python logging

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --reporting

# Or directly
cd module3/examples/reporting
python3 -c "import pyuvm; exec(open('reporting_example.py').read())"
```

**Expected Output:**
```
============================================================
UVM Reporting Example
============================================================
Demonstrating UVM severity levels:
This is an INFO message
WARNING: This is a WARNING message
ERROR: This is an ERROR message
FATAL: This is a FATAL message (would stop simulation)
============================================================
Demonstrating message formatting:
Formatted message: data=0xAB, addr=0x1000
============================================================
Component context:
  Component name: ReportingTest
  Component type: ReportingTest
  Full name: uvm_test_top
```

**Key Concepts:**
- **`self.logger.info()`**: Informational messages
- **`self.logger.warning()`**: Warning messages
- **`self.logger.error()`**: Error messages
- **`self.logger.fatal()`**: Fatal errors (stops simulation)
- **`get_name()`**: Get component instance name
- **`get_type_name()`**: Get component class name
- **`get_full_name()`**: Get full hierarchical name
- **Verbosity**: Controls which messages are displayed

### Test Case 3.4: ConfigDB Usage
**Objective**: Use ConfigDB

**Topics**:
- Setting configuration
- Getting configuration
- Configuration hierarchy

#### Example 3.4: ConfigDB (`module3/examples/configdb/configdb_example.py`)

**What it demonstrates:**
- **Setting Configuration**: `ConfigDB().set()` for objects and scalars
- **Getting Configuration**: `ConfigDB().get()` with lookup
- **Configuration Objects**: Creating custom config classes
- **Hierarchical Configuration**: Setting/getting at different hierarchy levels
- **Configuration Lookup**: How ConfigDB searches the hierarchy
- **Default Values**: Providing defaults when config not found

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --configdb

# Or directly
cd module3/examples/configdb
python3 -c "import pyuvm; exec(open('configdb_example.py').read())"
```

**Expected Output:**
```
============================================================
ConfigDB Example
============================================================
Building ConfigurableEnv
Set agent_config in ConfigDB
Set scalar configs in ConfigDB
[agent] Building agent
  Got config: active=True, has_coverage=True
  Got address_width: 16
Running ConfigDBTest
============================================================
Hierarchical Configuration Example:
Set configurations at different hierarchy levels
  Global config: global_value
  Test config: test_value
  Env config: env_value
============================================================
ConfigDB test completed
============================================================
```

**Key Concepts:**
- **`ConfigDB().set(context, path, name, value)`**: Set configuration
- **`ConfigDB().get(context, path, name, value)`**: Get configuration
- **Configuration Objects**: Custom classes inheriting from `uvm_object`
- **Hierarchy**: ConfigDB searches from specific to general (component → parent → global)
- **Path Matching**: Use empty string for current component, specific path for hierarchy
- **Type Safety**: ConfigDB maintains type information

#### Example 3.5: Factory Pattern (`module3/examples/factory/factory_example.py`)

**What it demonstrates:**
- **Factory Registration**: Automatic registration of UVM classes
- **Factory Creation**: Using factory to create objects and components
- **Type Overrides**: `uvm_factory().set_type_override()` for substitutions
- **Base and Extended Classes**: Creating base and extended versions
- **Factory Benefits**: Polymorphism without explicit type checking
- **Override Mechanism**: How factory resolves types with overrides

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --factory

# Or directly
cd module3/examples/factory
python3 -c "import pyuvm; exec(open('factory_example.py').read())"
```

**Key Concepts:**
- **Factory Registration**: All UVM classes are automatically registered
- **`create()`**: Factory method for component creation
- **`uvm_factory().set_type_override()`**: Override base type with extended type
- **Type Resolution**: Factory resolves types at creation time
- **Polymorphism**: Use base class type, get extended class instance

#### Example 3.6: Objection Mechanism (`module3/examples/objections/objections_example.py`)

**What it demonstrates:**
- **Raising Objections**: `raise_objection()` to keep simulation running
- **Dropping Objections**: `drop_objection()` to allow phase completion
- **Multiple Objections**: Components can raise multiple objections
- **Objection Lifecycle**: How objections control test execution
- **Component Objections**: Each component can manage its own objections
- **Test Control**: Test uses objections to control when simulation ends

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --objections

# Or directly
cd module3/examples/objections
python3 -c "import pyuvm; exec(open('objections_example.py').read())"
```

**Expected Output:**
```
============================================================
Objection Mechanism Example
============================================================
Building ObjectionEnv
[Test] Raised objection - simulation will run
[comp1] Raised objection
[comp2] Raised objection
[comp3] Raised 2 objections
[comp1] Work completed
[comp1] Dropped objection
[comp2] Work completed
[comp2] Dropped objection
[comp3] Dropped 1 objection, 1 remaining
[comp3] Dropped all objections
[Test] Dropping objection - simulation will end
============================================================
Objection test completed
============================================================
```

**Key Concepts:**
- **`raise_objection()`**: Increment objection count, keep phase running
- **`drop_objection()`**: Decrement objection count
- **Phase Completion**: Phase ends when all objections are dropped
- **Multiple Objections**: Can raise multiple times, must drop same number
- **Test Objections**: Test typically raises objection in `run_phase()`
- **Component Objections**: Components raise/drop for their own work

#### Test: Simple UVM Test (`module3/tests/pyuvm_tests/test_simple_uvm.py`)

**What it demonstrates:**
- Complete UVM testbench structure
- Test → Environment → Agent → Driver/Monitor/Sequencer hierarchy
- Sequence and sequence item usage
- Scoreboard integration
- Analysis port connections
- Full phase implementation

**Execution:**
```bash
# Using orchestrator script
./scripts/module3.sh --pyuvm-tests

# Or manually
cd module3/tests/pyuvm_tests
make SIM=verilator TEST=test_simple_uvm
```

**Test Structure:**
- `AdderTransaction`: Sequence item with test data
- `AdderSequence`: Generates test vectors
- `AdderDriver`: Drives transactions to DUT
- `AdderMonitor`: Monitors DUT outputs
- `AdderScoreboard`: Checks results
- `AdderAgent`: Contains driver, monitor, sequencer
- `AdderEnv`: Contains agent and scoreboard
- `AdderTest`: Top-level test class

### Design Under Test (DUT) Modules

#### Adder (`module3/dut/simple_blocks/adder.v`)
- **Purpose**: 8-bit adder with carry output
- **Used in**: Simple UVM test
- **Features**: Clocked operation, reset, 8-bit operands

## Exercises

1. **Test Class Creation**
   - Create test class
   - Implement phases
   - Use objections
   - **Location**: Create new test in `module3/tests/pyuvm_tests/`
   - **Hint**: Start with `AdderTest` as a template

2. **Environment Structure**
   - Design environment
   - Instantiate components
   - Connect components
   - **Location**: Extend `module3/examples/class_hierarchy/class_hierarchy_example.py`
   - **Hint**: Add scoreboard and connect analysis ports

3. **Reporting**
   - Add reporting
   - Control verbosity
   - Format messages
   - **Location**: Extend `module3/examples/reporting/reporting_example.py`
   - **Hint**: Add reporting to all phases

4. **Configuration**
   - Create config objects
   - Set configuration
   - Get configuration
   - **Location**: Extend `module3/examples/configdb/configdb_example.py`
   - **Hint**: Create configuration for multiple agents

5. **Phase Understanding**
   - Implement all phases
   - Understand execution order
   - Synchronize phases
   - **Location**: Extend `module3/examples/phases/phases_example.py`
   - **Hint**: Add multiple components and observe phase order

## Assessment

- [ ] Understands UVM methodology
- [ ] Can explain class hierarchy
- [ ] Understands all UVM phases
- [ ] Can use UVM reporting
- [ ] Can use ConfigDB
- [ ] Understands factory pattern
- [ ] Can create test classes
- [ ] Can structure environments
- [ ] Can use objection mechanism
- [ ] Can execute tests

## Next Steps

After completing this module, proceed to [Module 4: UVM Components](MODULE4.md) to learn how to build complete UVM agents.

## Additional Resources

- **pyuvm Documentation**: https://pyuvm.readthedocs.io/
- **UVM 1.2 User's Guide**: Accellera Systems Initiative
- **The UVM Primer**: Ray Salemi
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

**Issue: "cocotb not found" error (for running tests)**
```bash
# Solution: Install cocotb
./scripts/install_cocotb.sh --pip --venv .venv
# Or
./scripts/module0.sh
```

**Issue: Import errors in examples**
```bash
# Solution: Ensure pyuvm is installed and virtual environment is activated
source .venv/bin/activate
python3 -c "import pyuvm; print(pyuvm.__version__)"
```

**Issue: Phase execution order confusion**
```bash
# Solution: Review phases_example.py to see execution order
# Build phases: top-down, synchronous
# Run phases: concurrent, asynchronous
# Cleanup phases: bottom-up, synchronous
```

**Issue: Objections not working**
```bash
# Solution: Ensure raise_objection() is called in run_phase()
# Simulation ends when all objections are dropped
# Check objection count with uvm_objection methods
```

### Getting Help

- Check the example code comments for detailed explanations
- Review the `module3/README.md` for directory structure
- Run examples individually to understand each concept
- Study the phase execution order in `phases_example.py`
- Review UVM class hierarchy in `class_hierarchy_example.py`
- Check pyuvm documentation for API details

### Summary of Examples and Tests

**Examples (pyuvm structural examples in `module3/examples/`):**
1. **Example 3.1: Class Hierarchy** (`class_hierarchy/`) - UVM base classes and components
2. **Example 3.2: UVM Phases** (`phases/`) - All UVM phases and execution order
3. **Example 3.3: UVM Reporting** (`reporting/`) - Severity levels and verbosity
4. **Example 3.4: ConfigDB** (`configdb/`) - Configuration database usage
5. **Example 3.5: Factory Pattern** (`factory/`) - Factory creation and overrides
6. **Example 3.6: Objections** (`objections/`) - Objection mechanism

**Testbenches (runnable tests in `module3/tests/pyuvm_tests/`):**
1. **Simple UVM Test** (`test_simple_uvm.py`) - Complete UVM testbench with all components

**DUT Modules (in `module3/dut/`):**
1. **Adder** (`simple_blocks/adder.v`) - 8-bit adder for UVM testing

**Coverage:**
- ✅ UVM class hierarchy (uvm_object, uvm_component)
- ✅ All UVM phases (build, run, cleanup)
- ✅ UVM reporting system
- ✅ ConfigDB usage
- ✅ Factory pattern
- ✅ Objection mechanism
- ✅ Complete testbench structure

