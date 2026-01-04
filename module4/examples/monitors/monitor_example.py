"""
Module 4 Example 4.2: UVM Monitor Implementation
Demonstrates monitor implementation with signal sampling and analysis ports.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer, RisingEdge


class MonitorTransaction(uvm_sequence_item):
    """Transaction created by monitor."""
    
    def __init__(self, name="MonitorTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.timestamp = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, time={self.timestamp}ns"


class SimpleMonitor(uvm_monitor):
    """
    Simple monitor demonstrating basic monitor implementation.
    
    Shows:
    - Monitor class structure
    - Signal sampling from DUT
    - Transaction creation
    - Analysis port broadcasting
    """
    
    def build_phase(self):
        """Build phase - create analysis port."""
        self.logger.info(f"[{self.get_name()}] Building monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - main monitor loop."""
        self.logger.info(f"[{self.get_name()}] Starting monitor run_phase")
        
        while True:
            # Sample DUT signals and create transaction
            txn = await self.sample_signals()
            
            if txn is not None:
                self.logger.info(f"[{self.get_name()}] Sampled transaction: {txn}")
                # Broadcast transaction via analysis port
                self.ap.write(txn)
                self.logger.info(f"[{self.get_name()}] Broadcasted transaction via analysis port")
    
    async def sample_signals(self):
        """
        Sample DUT signals and create transaction.
        
        In real implementation, this would:
        - Wait for valid data on DUT
        - Sample signal values
        - Create and populate transaction
        """
        # Simulate signal sampling
        await Timer(10, units="ns")
        
        # In real code:
        # await RisingEdge(cocotb.dut.valid)
        # data = cocotb.dut.data.value.integer
        # addr = cocotb.dut.address.value.integer
        
        # Create transaction
        txn = MonitorTransaction()
        txn.data = 0xAB  # Simulated sampled value
        txn.address = 0x1000  # Simulated sampled value
        txn.timestamp = cocotb.utils.get_sim_time(units='ns') if hasattr(cocotb, 'dut') else 0
        
        return txn


class ProtocolMonitor(uvm_monitor):
    """
    Monitor demonstrating protocol-specific sampling.
    
    Shows:
    - Protocol-aware signal sampling
    - Transaction creation from protocol signals
    - Timing-based sampling
    """
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building protocol monitor")
        self.ap = uvm_analysis_port("ap", self)
        self.sample_count = 0
    
    async def run_phase(self):
        """Run phase with protocol sampling."""
        self.logger.info(f"[{self.get_name()}] Starting protocol monitor")
        
        while True:
            # Wait for protocol event
            await self.wait_for_protocol_event()
            
            # Sample on protocol event
            txn = await self.sample_protocol_signals()
            
            if txn is not None:
                self.sample_count += 1
                self.logger.info(f"[{self.get_name()}] Sampled transaction #{self.sample_count}: {txn}")
                self.ap.write(txn)
    
    async def wait_for_protocol_event(self):
        """Wait for protocol-specific event."""
        # In real code: await RisingEdge(cocotb.dut.valid)
        await Timer(10, units="ns")
    
    async def sample_protocol_signals(self):
        """Sample signals based on protocol."""
        # In real code:
        # await RisingEdge(cocotb.dut.clk)
        # if cocotb.dut.valid.value:
        #     txn = MonitorTransaction()
        #     txn.data = cocotb.dut.data.value.integer
        #     return txn
        
        txn = MonitorTransaction()
        txn.data = 0xCD
        txn.address = 0x2000
        return txn


class MonitorAgent(uvm_agent):
    """Agent containing monitor."""
    
    def build_phase(self):
        self.logger.info("Building MonitorAgent")
        self.monitor = SimpleMonitor.create("monitor", self)
    
    def connect_phase(self):
        self.logger.info("Connecting MonitorAgent")


class MonitorTest(uvm_test):
    """Test demonstrating monitor usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Monitor Example Test")
        self.logger.info("=" * 60)
        self.env = MonitorAgent.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running monitor test")
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Monitor test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_monitor(dut):
    """Cocotb test wrapper for pyuvm monitor test."""
    import inspect
    test = MonitorTest.create("test")
    await test.build_phase()
    if hasattr(test, 'connect_phase') and inspect.iscoroutinefunction(test.connect_phase):
        await test.connect_phase()
    await test.run_phase()
    if hasattr(test, 'check_phase'):
        test.check_phase()
    test.report_phase()


if __name__ == "__main__":
    print("This is a pyuvm monitor example.")
    print("To run with cocotb, use the Makefile in the test directory.")

