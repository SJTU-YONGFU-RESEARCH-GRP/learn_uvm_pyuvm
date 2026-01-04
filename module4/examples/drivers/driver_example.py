"""
Module 4 Example 4.1: UVM Driver Implementation
Demonstrates driver implementation with transaction reception and signal driving.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer, RisingEdge


class SimpleTransaction(uvm_sequence_item):
    """Simple transaction for driver example."""
    
    def __init__(self, name="SimpleTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class SimpleDriver(uvm_driver):
    """
    Simple driver demonstrating basic driver implementation.
    
    Shows:
    - Driver class structure
    - Transaction reception from sequencer
    - Signal driving to DUT
    - Driver-sequencer communication
    """
    
    def build_phase(self):
        """Build phase - create sequencer port."""
        self.logger.info(f"[{self.get_name()}] Building driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    def connect_phase(self):
        """Connect phase - connect to sequencer."""
        self.logger.info(f"[{self.get_name()}] Connecting driver")
    
    async def run_phase(self):
        """Run phase - main driver loop."""
        self.logger.info(f"[{self.get_name()}] Starting driver run_phase")
        
        while True:
            # Get next transaction from sequencer
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Received transaction: {item}")
            
            # Drive transaction to DUT
            await self.drive_transaction(item)
            
            # Signal completion to sequencer
            await self.seq_item_port.item_done()
            self.logger.info(f"[{self.get_name()}] Transaction completed")
    
    async def drive_transaction(self, txn):
        """
        Drive transaction to DUT.
        
        In real implementation, this would:
        - Drive DUT signals based on transaction fields
        - Implement protocol timing
        - Handle handshaking
        """
        self.logger.info(f"[{self.get_name()}] Driving transaction: {txn}")
        
        # Simulate signal driving
        # In real code: cocotb.dut.data.value = txn.data
        # In real code: cocotb.dut.address.value = txn.address
        # In real code: await RisingEdge(cocotb.dut.clk)
        
        await Timer(10, units="ns")
        self.logger.info(f"[{self.get_name()}] Signals driven: data=0x{txn.data:02X}, addr=0x{txn.address:04X}")


class ProtocolDriver(uvm_driver):
    """
    Driver demonstrating protocol implementation.
    
    Shows:
    - Protocol-specific signal driving
    - Timing control
    - Handshaking
    """
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building protocol driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase with protocol implementation."""
        self.logger.info(f"[{self.get_name()}] Starting protocol driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            
            # Implement protocol: request -> wait for grant -> drive -> complete
            await self.drive_with_protocol(item)
            
            await self.seq_item_port.item_done()
    
    async def drive_with_protocol(self, txn):
        """Drive transaction with protocol handshaking."""
        self.logger.info(f"[{self.get_name()}] Protocol: Asserting request")
        # In real code: cocotb.dut.req.value = 1
        
        await Timer(5, units="ns")
        
        # Wait for grant (simulated)
        self.logger.info(f"[{self.get_name()}] Protocol: Waiting for grant")
        # In real code: await RisingEdge(cocotb.dut.gnt)
        
        await Timer(5, units="ns")
        
        # Drive data
        self.logger.info(f"[{self.get_name()}] Protocol: Driving data")
        # In real code: cocotb.dut.data.value = txn.data
        
        await Timer(10, units="ns")
        
        # Deassert request
        self.logger.info(f"[{self.get_name()}] Protocol: Deasserting request")
        # In real code: cocotb.dut.req.value = 0


class DriverAgent(uvm_agent):
    """Agent containing driver and sequencer."""
    
    def build_phase(self):
        self.logger.info("Building DriverAgent")
        self.driver = SimpleDriver.create("driver", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting DriverAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class DriverTest(uvm_test):
    """Test demonstrating driver usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Driver Example Test")
        self.logger.info("=" * 60)
        self.env = DriverAgent.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running driver test")
        
        # Note: In real test, you would start a sequence here
        # seq = SimpleSequence.create("seq")
        # await seq.start(self.env.seqr)
        
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Driver test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_driver(dut):
    """Cocotb test wrapper for pyuvm driver test."""
    import inspect
    test = DriverTest.create("test")
    await test.build_phase()
    if hasattr(test, 'connect_phase') and inspect.iscoroutinefunction(test.connect_phase):
        await test.connect_phase()
    await test.run_phase()
    if hasattr(test, 'check_phase'):
        test.check_phase()
    test.report_phase()


if __name__ == "__main__":
    print("This is a pyuvm driver example.")
    print("To run with cocotb, use the Makefile in the test directory.")

