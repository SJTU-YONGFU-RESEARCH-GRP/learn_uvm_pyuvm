# UVM and pyuvm Glossary

A comprehensive glossary of terms used in UVM (Universal Verification Methodology) and pyuvm.

## A

**Active Agent**
- An agent that includes a driver, sequencer, and monitor. Active agents can generate stimulus.

**Analysis Port**
- A TLM port type that supports broadcast communication (one-to-many). Used for publishing transactions to multiple subscribers.

**Agent**
- A reusable verification component that encapsulates a driver, monitor, and sequencer for a specific protocol or interface.

## B

**Base Class**
- The fundamental classes in UVM from which all other classes inherit. Includes `uvm_object` and `uvm_component`.

**Build Phase**
- The first phase in UVM where components are constructed and configured.

## C

**Callback**
- A mechanism for extending component behavior without modifying the component itself. Allows pre/post hooks.

**ConfigDB**
- UVM's configuration database used to pass configuration information between components in the testbench hierarchy.

**Component**
- A class that inherits from `uvm_component`. Components have a hierarchical structure and participate in phases.

**Connect Phase**
- The phase where components establish connections between each other (e.g., ports to exports).

**Coverage**
- A metric that measures how thoroughly a design has been tested. Includes functional coverage and code coverage.

## D

**Driver**
- A UVM component that receives transactions from a sequencer and drives them onto the DUT interface at the signal level.

**DUT (Design Under Test)**
- The hardware design being verified.

## E

**Environment (uvm_env)**
- A container component that holds and connects agents, scoreboards, and other verification components.

**Export**
- A TLM interface that receives transactions. Exports are connected to ports.

## F

**Factory**
- UVM's object creation mechanism that allows type substitution and override without modifying test code.

**FIFO (First-In-First-Out)**
- A queue data structure. In UVM, `uvm_tlm_fifo` is used for TLM communication.

## G

**Get Interface**
- A TLM interface for receiving transactions. Blocking operation that waits for data.

## I

**Implementation (imp)**
- A TLM interface that provides the actual implementation of a TLM method (e.g., `uvm_put_imp`).

## M

**Monitor**
- A UVM component that observes DUT signals and converts them into transaction-level objects.

## O

**Object**
- A class that inherits from `uvm_object`. Objects are not hierarchical and don't participate in phases.

**Objection**
- A mechanism in UVM that prevents simulation from ending. Components raise objections to keep simulation running.

## P

**Passive Agent**
- An agent that includes only a monitor. Used for observing DUT behavior without generating stimulus.

**Peek Interface**
- A TLM interface for non-blocking read operations. Returns immediately even if no data is available.

**Phase**
- A stage in the UVM simulation lifecycle. Phases control when components perform their operations.

**Port**
- A TLM interface that sends transactions. Ports are connected to exports.

**Put Interface**
- A TLM interface for sending transactions. Blocking operation that waits for acceptance.

## R

**Register Model**
- A UVM abstraction that models hardware registers, allowing register access without direct signal manipulation.

**Reporting**
- UVM's messaging system that provides standardized logging with severity and verbosity levels.

**Run Phase**
- The main execution phase in UVM where test stimulus is generated and applied.

## S

**Scoreboard**
- A verification component that checks DUT behavior by comparing expected and actual results.

**Sequence**
- A class that generates a series of transactions. Sequences are executed on sequencers.

**Sequence Item**
- A transaction object that represents a single operation. Sequence items are sent from sequences to drivers.

**Sequencer**
- A UVM component that manages sequence execution and arbitrates between multiple sequences.

**Subscriber**
- A component that receives transactions from analysis ports. Implements the `write()` method.

## T

**TLM (Transaction-Level Modeling)**
- A communication mechanism in UVM that allows components to communicate at the transaction level rather than signal level.

**Transport Interface**
- A bidirectional TLM interface that combines put and get operations in a single call.

**Test (uvm_test)**
- The top-level component in a UVM testbench. Tests instantiate environments and coordinate test execution.

**Transaction**
- An object that represents a high-level operation or data transfer. Transactions are abstracted from signal-level details.

## U

**UVM (Universal Verification Methodology)**
- An industry-standard methodology for functional verification of hardware designs.

**uvm_component**
- Base class for all hierarchical components in UVM. Components have names, parents, and participate in phases.

**uvm_object**
- Base class for all non-hierarchical objects in UVM. Objects include transactions, configurations, and sequences.

## V

**Virtual Sequence**
- A sequence that coordinates multiple sequencers, allowing coordination of stimulus across different interfaces.

**Virtual Sequencer**
- A sequencer that contains references to other sequencers but doesn't execute sequences itself. Used with virtual sequences.

## Additional Terms

**cocotb**
- Coroutine-based testbench framework that enables Python testbenches for hardware verification.

**pyuvm**
- Python implementation of UVM 1.2 that works with cocotb and open-source simulators.

**Verilator**
- An open-source Verilog/SystemVerilog simulator that can be used with cocotb and pyuvm.

## IEEE 1800.2 Standard Terms

**IEEE 1800.2**
- The IEEE standard that defines the Universal Verification Methodology (UVM) Language Reference Manual.

**UVM 1.2**
- The version of UVM standardized in IEEE 1800.2-2020.

## Related Concepts

**Assertion**
- A statement that specifies expected behavior. Assertions can be immediate or concurrent.

**Coverage Closure**
- The process of achieving target coverage goals through test development and analysis.

**Regression Testing**
- Running a suite of tests repeatedly to ensure that changes don't break existing functionality.

**Testbench**
- The verification environment that tests a design. Includes stimulus generation, monitoring, and checking.

**VIP (Verification IP)**
- Reusable verification components, typically for standard protocols, that can be integrated into testbenches.

