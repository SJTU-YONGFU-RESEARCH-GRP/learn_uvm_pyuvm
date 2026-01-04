"""
Module 5 Test: Advanced UVM Test
Complete testbench demonstrating advanced UVM concepts.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *

# Explicit imports for TLM classes that may not be in __all__
for class_name in ['uvm_seq_item_pull_port', 'uvm_analysis_imp']:
    try:
        # Try to get it from globals first (in case from pyuvm import * worked)
        eval(class_name)  # type: ignore
    except NameError:
        # Not in globals, try to import it explicitly
        _found = False
        # Try TLM module paths
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=[class_name])
                if hasattr(tlm_module, class_name):
                    globals()[class_name] = getattr(tlm_module, class_name)  # type: ignore
                    _found = True
                    break
            except (ImportError, AttributeError):
                continue
        # If still not found, try pyuvm module directly
        if not _found:
            import pyuvm
            if hasattr(pyuvm, class_name):
                globals()[class_name] = getattr(pyuvm, class_name)  # type: ignore
                _found = True
        if not _found:
            # This should not happen if pyuvm is properly installed
            raise ImportError(f"Could not import {class_name} from pyuvm")


class AdvancedTransaction(uvm_sequence_item):
    """Transaction for advanced UVM test."""
    
    def __init__(self, name="AdvancedTransaction"):
        super().__init__(name)
        self.data = 0
        self.channel = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, channel={self.channel}"


class AdvancedSequence(uvm_sequence):
    """Sequence for advanced test."""
    
    async def body(self):
        """Generate transactions."""
        for i in range(5):
            txn = AdvancedTransaction()
            txn.data = i * 0x10
            txn.channel = 0
            await self.start_item(txn)
            await self.finish_item(txn)


class AdvancedDriver(uvm_driver):
    """Driver for advanced test."""
    
    def build_phase(self):
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving: {item}")
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class AdvancedMonitor(uvm_monitor):
    """Monitor for advanced test."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            await Timer(10, units="ns")
            txn = AdvancedTransaction()
            txn.data = 0xAA
            txn.channel = 0
            self.ap.write(txn)


class AdvancedCoverage(uvm_subscriber):
    """Coverage for advanced test."""
    
    def __init__(self, name="AdvancedCoverage", parent=None):
        super().__init__(name, parent)
        self.coverage_data = {}
    
    def build_phase(self):
        """Build phase - create analysis ports."""
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
    
    def write(self, txn):
        """Sample coverage."""
        if txn.data not in self.coverage_data:
            self.coverage_data[txn.data] = 0
        self.coverage_data[txn.data] += 1
        self.logger.info(f"Coverage sampled: {txn}, unique values: {len(self.coverage_data)}")


class AdvancedAgent(uvm_agent):
    """Agent for advanced test."""
    
    def build_phase(self):
        self.driver = AdvancedDriver.create("driver", self)
        self.monitor = AdvancedMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AdvancedEnv(uvm_env):
    """Environment for advanced test."""
    
    def build_phase(self):
        self.logger.info("Building AdvancedEnv")
        self.agent = AdvancedAgent.create("agent", self)
        self.coverage = AdvancedCoverage.create("coverage", self)
    
    def connect_phase(self):
        self.logger.info("Connecting AdvancedEnv")
        self.agent.monitor.ap.connect(self.coverage.ap)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class AdvancedUVMTest(uvm_test):
    """Test class for advanced UVM."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building AdvancedUVMTest")
        self.logger.info("=" * 60)
        self.env = AdvancedEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running AdvancedUVMTest")
        
        # Start sequence
        seq = AdvancedSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking AdvancedUVMTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AdvancedUVMTest completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_advanced_uvm(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["AdvancedUVMTest"] = AdvancedUVMTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("AdvancedUVMTest")


if __name__ == "__main__":
    print("This is a pyuvm advanced UVM test.")
    print("To run with cocotb, use the Makefile in the test directory.")

