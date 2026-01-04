"""
Module 6 Test: Complex Testbench Test
Complete testbench demonstrating complex multi-agent environment.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *
# Explicitly import uvm_seq_item_pull_port - it may not be exported by from pyuvm import *
# Try multiple possible import paths
_uvm_seq_item_pull_port = None
try:
    # First try: check if it's in the namespace after from pyuvm import *
    _uvm_seq_item_pull_port = globals()['uvm_seq_item_pull_port']
except KeyError:
    # Second try: import from pyuvm module directly
    import pyuvm
    if hasattr(pyuvm, 'uvm_seq_item_pull_port'):
        _uvm_seq_item_pull_port = pyuvm.uvm_seq_item_pull_port
    else:
        # Third try: try TLM module paths using __import__
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_seq_item_pull_port'])
                if hasattr(tlm_module, 'uvm_seq_item_pull_port'):
                    _uvm_seq_item_pull_port = tlm_module.uvm_seq_item_pull_port
                    break
            except (ImportError, AttributeError):
                continue

if _uvm_seq_item_pull_port is not None:
    globals()['uvm_seq_item_pull_port'] = _uvm_seq_item_pull_port

# Explicitly import uvm_analysis_imp - it may not be exported by from pyuvm import *
# Try multiple possible import paths
_uvm_analysis_imp = None
try:
    # First try: check if it's in the namespace after from pyuvm import *
    _uvm_analysis_imp = globals()['uvm_analysis_imp']
except KeyError:
    # Second try: import from pyuvm module directly
    import pyuvm
    if hasattr(pyuvm, 'uvm_analysis_imp'):
        _uvm_analysis_imp = pyuvm.uvm_analysis_imp
    else:
        # Third try: try TLM module paths using __import__
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_analysis_imp'])
                if hasattr(tlm_module, 'uvm_analysis_imp'):
                    _uvm_analysis_imp = tlm_module.uvm_analysis_imp
                    break
            except (ImportError, AttributeError):
                continue

if _uvm_analysis_imp is not None:
    globals()['uvm_analysis_imp'] = _uvm_analysis_imp


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


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class ComplexTestbenchTest(uvm_test):
    """Test class for complex testbench."""
    
    def build_phase(self):
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


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_complex_testbench(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ComplexTestbenchTest"] = ComplexTestbenchTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ComplexTestbenchTest")


if __name__ == "__main__":
    print("This is a pyuvm complex testbench test.")
    print("To run with cocotb, use the Makefile in the test directory.")

