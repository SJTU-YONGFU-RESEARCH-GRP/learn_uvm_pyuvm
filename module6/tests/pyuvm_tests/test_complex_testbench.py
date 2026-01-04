"""
Module 6 Test: Complex Testbench Test
Complete testbench demonstrating complex multi-agent environment.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *


class ComplexTransaction(uvm_sequence_item):
    """Transaction for complex testbench."""
    
    def __init__(self, name="ComplexTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.channel = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, channel={self.channel}"


class ComplexSequence(uvm_sequence):
    """Sequence for complex testbench."""
    
    async def body(self):
        """Generate test vectors."""
        for i in range(5):
            txn = ComplexTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            txn.channel = 0
            await self.start_item(txn)
            await self.finish_item(txn)


class ComplexDriver(uvm_driver):
    """Driver for complex testbench."""
    
    def build_phase(self):
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {item}")
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class ComplexMonitor(uvm_monitor):
    """Monitor for complex testbench."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            await Timer(10, units="ns")
            txn = ComplexTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            txn.channel = 0
            self.ap.write(txn)


class ComplexScoreboard(uvm_scoreboard):
    """Scoreboard for complex testbench."""
    
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


class ComplexAgent(uvm_agent):
    """Agent for complex testbench."""
    
    def build_phase(self):
        self.driver = ComplexDriver.create("driver", self)
        self.monitor = ComplexMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class ComplexEnv(uvm_env):
    """Environment for complex testbench."""
    
    def build_phase(self):
        self.logger.info("Building ComplexEnv")
        self.agent = ComplexAgent.create("agent", self)
        self.scoreboard = ComplexScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting ComplexEnv")
        self.agent.monitor.ap.connect(self.scoreboard.ap)


@uvm_test()
class ComplexTestbenchTest(uvm_test):
    """Test class for complex testbench."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building ComplexTestbenchTest")
        self.logger.info("=" * 60)
        self.env = ComplexEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running ComplexTestbenchTest")
        
        # Start sequence
        seq = ComplexSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking ComplexTestbenchTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("ComplexTestbenchTest completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm complex testbench test.")
    print("To run with cocotb, use the Makefile in the test directory.")

