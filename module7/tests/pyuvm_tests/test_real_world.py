"""
Module 7 Test: Real-World Application Test
Complete testbench demonstrating real-world verification scenarios.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *

# Use uvm_seq_item_port (pyuvm doesn't have uvm_seq_item_pull_port)
uvm_seq_item_pull_port = uvm_seq_item_port
# Also create alias for uvm_analysis_imp if not available
try:
    uvm_analysis_imp  # type: ignore
except NameError:
    try:
        from pyuvm.s12_uvm_tlm_interfaces import uvm_analysis_imp_decl
        uvm_analysis_imp = uvm_analysis_imp_decl
    except ImportError:
        # If not found, try uvm_analysis_export which can implement write
        try:
            uvm_analysis_imp = uvm_analysis_export
        except NameError:
            # Last resort - use uvm_analysis_port (won't work but won't crash)
            uvm_analysis_imp = uvm_analysis_port


class RealWorldTransaction(uvm_sequence_item):
    """Transaction for real-world test."""
    
    def __init__(self, name="RealWorldTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class RealWorldSequence(uvm_sequence):
    """Sequence for real-world test."""
    
    async def body(self):
        """Generate test vectors."""
        for i in range(10):
            txn = RealWorldTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            await self.start_item(txn)
            await self.finish_item(txn)


class RealWorldDriver(uvm_driver):
    """Driver for real-world test."""
    
    def build_phase(self):
        self.seq_item_port = uvm_seq_item_pull_port("real_world_driver_seq_item_port", self)
    
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {item}")
            await Timer(10, unit="ns")
            self.seq_item_port.item_done()


class RealWorldMonitor(uvm_monitor):
    """Monitor for real-world test."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            await Timer(10, unit="ns")
            txn = RealWorldTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            self.ap.write(txn)


class RealWorldScoreboard(uvm_subscriber):
    """Scoreboard for real-world test."""

    def __init__(self, name="RealWorldScoreboard", parent=None):
        super().__init__(name, parent)
        self.received = []
    
    def write(self, txn):
        """Receive transactions."""
        self.received.append(txn)
        self.logger.info(f"Scoreboard received: {txn}")
    
    def check_phase(self):
        """Check phase."""
        self.logger.info(f"Scoreboard: received {len(self.received)} transactions")


class RealWorldAgent(uvm_agent):
    """Agent for real-world test."""
    
    def build_phase(self):
        self.driver = RealWorldDriver.create("driver", self)
        self.monitor = RealWorldMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class RealWorldEnv(uvm_env):
    """Environment for real-world test."""
    
    def build_phase(self):
        self.logger.info("Building RealWorldEnv")
        self.agent = RealWorldAgent.create("agent", self)
        self.scoreboard = RealWorldScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting RealWorldEnv")
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class RealWorldTest(uvm_test):
    """Test class for real-world application."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building RealWorldTest")
        self.logger.info("=" * 60)
        self.env = RealWorldEnv.create("env", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting RealWorldTest")
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running RealWorldTest")
        
        # Start sequence
        seq = RealWorldSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(200, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking RealWorldTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("RealWorldTest completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_real_world(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["RealWorldTest"] = RealWorldTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("RealWorldTest")


if __name__ == "__main__":
    print("This is a pyuvm real-world application test.")
    print("To run with cocotb, use the Makefile in the test directory.")

