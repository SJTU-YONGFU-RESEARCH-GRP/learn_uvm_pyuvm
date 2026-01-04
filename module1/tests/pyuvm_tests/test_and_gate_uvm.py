"""
Module 1: AND Gate UVM Test
pyuvm testbench for AND gate.

Demonstrates:
- UVM test structure
- UVM phases
- UVM reporting
"""

from pyuvm import *


class AndGateTransaction(uvm_sequence_item):
    """Transaction for AND gate test."""
    
    def __init__(self, name="AndGateTransaction"):
        super().__init__(name)
        self.a = 0
        self.b = 0
        self.expected_y = 0
    
    def __str__(self):
        return f"a={self.a}, b={self.b}, expected_y={self.expected_y}"


class AndGateSequence(uvm_sequence):
    """Sequence to generate AND gate test vectors."""
    
    async def body(self):
        """Generate test vectors."""
        test_vectors = [
            (0, 0, 0),
            (0, 1, 0),
            (1, 0, 0),
            (1, 1, 1),
        ]
        
        for a, b, expected_y in test_vectors:
            txn = AndGateTransaction()
            txn.a = a
            txn.b = b
            txn.expected_y = expected_y
            await self.start_item(txn)
            await self.finish_item(txn)


class AndGateDriver(uvm_driver):
    """
    Driver to apply inputs to DUT.
    
    In a real cocotb+pyuvm testbench, the DUT would be accessed via
    cocotb handles. This example shows the pattern for driving signals.
    """
    
    def build_phase(self):
        """Build phase: create sequence item port."""
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
        # In real implementation with cocotb:
        # self.dut = cocotb.top  # Access DUT from cocotb
    
    async def run_phase(self):
        """
        Run phase: drive transactions to DUT.
        
        This demonstrates the pattern for driving DUT signals from transactions.
        In a real testbench with cocotb, you would:
        1. Get transaction from sequencer
        2. Drive DUT input signals (dut.a.value, dut.b.value)
        3. Wait for signal propagation (await Timer)
        4. Signal completion to sequencer
        """
        while True:
            txn = await self.seq_item_port.get_next_item()
            
            # Drive DUT signals from transaction
            # In real cocotb implementation:
            # self.dut.a.value = txn.a
            # self.dut.b.value = txn.b
            # await Timer(10, units="ns")  # Wait for combinational logic
            
            self.logger.info(f"Driving DUT: a={txn.a}, b={txn.b} (expected y={txn.expected_y})")
            
            # Signal completion to sequencer
            await self.seq_item_port.item_done()


class AndGateMonitor(uvm_monitor):
    """
    Monitor to observe DUT outputs.
    
    In a real cocotb+pyuvm testbench, the monitor would sample DUT outputs
    and create transactions for the scoreboard. This example shows the pattern.
    """
    
    def build_phase(self):
        """Build phase: create analysis port for sending transactions."""
        self.ap = uvm_analysis_port("ap", self)
        # In real implementation with cocotb:
        # self.dut = cocotb.top  # Access DUT from cocotb
    
    async def run_phase(self):
        """
        Run phase: monitor DUT outputs.
        
        This demonstrates the pattern for monitoring DUT signals.
        In a real testbench with cocotb, you would:
        1. Sample DUT output signals (dut.y.value)
        2. Create transaction with observed values
        3. Send transaction to scoreboard via analysis port
        4. Wait for next clock edge or time step
        """
        while True:
            # Sample DUT output
            # In real cocotb implementation:
            # observed_y = self.dut.y.value.integer
            # 
            # Create transaction with observed value
            # observed_txn = AndGateTransaction()
            # observed_txn.y = observed_y
            # 
            # Send to scoreboard via analysis port
            # self.ap.write(observed_txn)
            
            await Timer(10, units="ns")  # Wait for next sampling point
            self.logger.info("Monitoring DUT: sampling output y")


class AndGateAgent(uvm_agent):
    """Agent containing driver and monitor."""
    
    def build_phase(self):
        self.driver = AndGateDriver.create("driver", self)
        self.monitor = AndGateMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AndGateEnv(uvm_env):
    """Test environment."""
    
    def build_phase(self):
        self.agent = AndGateAgent.create("agent", self)
    
    def connect_phase(self):
        pass


@uvm_test()
class AndGateTest(uvm_test):
    """Test class for AND gate."""
    
    async def build_phase(self):
        self.env = AndGateEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        seq = AndGateSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        await Timer(100, units="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking test results")


if __name__ == "__main__":
    # Note: This is a simplified example
    # In practice, you would use cocotb to run this with a simulator
    print("This is a pyuvm test structure example.")
    print("To run with cocotb, use the Makefile in the test directory.")

