"""
Module 7 Test: Real-World Application Test
Complete testbench demonstrating real-world verification scenarios.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *


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
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {item}")
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class RealWorldMonitor(uvm_monitor):
    """Monitor for real-world test."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            await Timer(10, units="ns")
            txn = RealWorldTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            self.ap.write(txn)


class RealWorldScoreboard(uvm_scoreboard):
    """Scoreboard for real-world test."""
    
    def build_phase(self):
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
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
        self.agent.monitor.ap.connect(self.scoreboard.ap)


@uvm_test()
class RealWorldTest(uvm_test):
    """Test class for real-world application."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building RealWorldTest")
        self.logger.info("=" * 60)
        self.env = RealWorldEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running RealWorldTest")
        
        # Start sequence
        seq = RealWorldSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(200, units="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking RealWorldTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("RealWorldTest completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm real-world application test.")
    print("To run with cocotb, use the Makefile in the test directory.")

