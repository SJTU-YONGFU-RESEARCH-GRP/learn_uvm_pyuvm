"""
Module 8 Test: Utilities Test
Complete testbench demonstrating utility usage.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *


class UtilitiesTransaction(uvm_sequence_item):
    """Transaction for utilities test."""
    
    def __init__(self, name="UtilitiesTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class UtilitiesSequence(uvm_sequence):
    """Sequence for utilities test."""
    
    async def body(self):
        """Generate test vectors."""
        for i in range(10):
            txn = UtilitiesTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            await self.start_item(txn)
            await self.finish_item(txn)


class UtilitiesDriver(uvm_driver):
    """Driver for utilities test."""
    
    def build_phase(self):
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {item}")
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class UtilitiesMonitor(uvm_monitor):
    """Monitor for utilities test."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            await Timer(10, units="ns")
            txn = UtilitiesTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            self.ap.write(txn)


class UtilitiesScoreboard(uvm_scoreboard):
    """Scoreboard for utilities test."""
    
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


class UtilitiesAgent(uvm_agent):
    """Agent for utilities test."""
    
    def build_phase(self):
        self.driver = UtilitiesDriver.create("driver", self)
        self.monitor = UtilitiesMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class UtilitiesEnv(uvm_env):
    """Environment for utilities test."""
    
    def build_phase(self):
        self.logger.info("Building UtilitiesEnv")
        self.agent = UtilitiesAgent.create("agent", self)
        self.scoreboard = UtilitiesScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting UtilitiesEnv")
        self.agent.monitor.ap.connect(self.scoreboard.ap)


@uvm_test()
class UtilitiesTest(uvm_test):
    """Test class for utilities."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building UtilitiesTest")
        self.logger.info("=" * 60)
        self.env = UtilitiesEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running UtilitiesTest")
        
        # Start sequence
        seq = UtilitiesSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(200, units="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking UtilitiesTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("UtilitiesTest completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm utilities test.")
    print("To run with cocotb, use the Makefile in the test directory.")

