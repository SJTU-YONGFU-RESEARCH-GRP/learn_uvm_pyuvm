"""
Module 3 Test Case 3.1: Simple UVM Test
Complete UVM testbench for simple adder.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from pyuvm import *
# Explicitly import uvm_seq_item_pull_port - it may not be exported by from pyuvm import *
# Try multiple possible import paths (pattern from module4/examples/agents/agent_example.py)
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
        # Third try: try TLM module paths
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
else:
    # If still not found, try one more time to see if it's available directly
    # This handles edge cases where from pyuvm import * worked but globals() check didn't
    try:
        # Try to use it - if it's available, this will work
        _ = uvm_seq_item_pull_port  # type: ignore
        # If we get here, it's available, so we're good
    except NameError:
        # It's truly not available - this will cause an error when used
        # But we'll let the error happen at usage time for clearer error messages
        pass


class AdderTransaction(uvm_sequence_item):
    """Transaction for adder test."""
    
    def __init__(self, name="AdderTransaction"):
        super().__init__(name)
        self.a = 0
        self.b = 0
        self.expected_sum = 0
        self.expected_carry = 0
    
    def __str__(self):
        return (f"a=0x{self.a:02X}, b=0x{self.b:02X}, "
                f"expected_sum=0x{self.expected_sum:02X}, "
                f"expected_carry={self.expected_carry}")


class AdderSequence(uvm_sequence):
    """Sequence generating adder test vectors."""
    
    async def body(self):
        """Generate test vectors."""
        test_vectors = [
            (0x00, 0x00, 0x00, 0),
            (0x01, 0x01, 0x02, 0),
            (0xFF, 0x01, 0x00, 1),  # Overflow
            (0x80, 0x80, 0x00, 1),  # Overflow
            (0x0A, 0x05, 0x0F, 0),
        ]
        
        for a, b, expected_sum, expected_carry in test_vectors:
            txn = AdderTransaction()
            txn.a = a
            txn.b = b
            txn.expected_sum = expected_sum
            txn.expected_carry = expected_carry
            await self.start_item(txn)
            await self.finish_item(txn)


class AdderDriver(uvm_driver):
    """Driver for adder DUT."""
    
    def build_phase(self):
        # uvm_seq_item_pull_port should be available from the import logic above
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)  # type: ignore
    
    async def run_phase(self):
        while True:
            txn = await self.seq_item_port.get_next_item()
            # In real implementation, drive DUT signals
            # cocotb.dut.a.value = txn.a
            # cocotb.dut.b.value = txn.b
            self.logger.info(f"Driving: {txn}")
            await Timer(10, unit="ns")
            await self.seq_item_port.item_done()


class AdderMonitor(uvm_monitor):
    """Monitor for adder DUT."""
    
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        while True:
            # In real implementation, sample DUT outputs
            # sum = cocotb.dut.sum.value.integer
            # carry = cocotb.dut.carry.value.integer
            await Timer(10, unit="ns")
            self.logger.debug("Monitoring DUT")


class AdderScoreboard(uvm_scoreboard):
    """Scoreboard for adder verification."""
    
    def build_phase(self):
        self.ap = uvm_analysis_export("ap", self)
        self.expected = []
        self.actual = []
    
    def write(self, txn):
        """Receive transactions from monitor."""
        self.actual.append(txn)
        self.logger.info(f"Scoreboard received: {txn}")
    
    def check_phase(self):
        """Check phase - verify results."""
        self.logger.info("=" * 60)
        self.logger.info("Scoreboard Check")
        self.logger.info(f"Total transactions: {len(self.actual)}")
        if len(self.expected) == len(self.actual):
            self.logger.info("✓ Transaction count matches")
        else:
            self.logger.error(f"✗ Transaction count mismatch: "
                            f"expected={len(self.expected)}, actual={len(self.actual)}")


class AdderAgent(uvm_agent):
    """Agent for adder."""
    
    def build_phase(self):
        self.driver = AdderDriver.create("driver", self)
        self.monitor = AdderMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.monitor.ap.connect(self.env.scoreboard.ap)


class AdderEnv(uvm_env):
    """Environment for adder test."""
    
    def build_phase(self):
        self.logger.info("Building AdderEnv")
        self.agent = AdderAgent.create("agent", self)
        self.scoreboard = AdderScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting AdderEnv")
        self.agent.monitor.ap.connect(self.scoreboard.ap)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class AdderTest(uvm_test):
    """Test class for adder."""
    
    def build_phase(self):
        """Build phase - create environment."""
        self.logger.info("=" * 60)
        self.logger.info("Building AdderTest")
        self.logger.info("=" * 60)
        self.env = AdderEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running AdderTest")
        
        # Start sequence
        seq = AdderSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        self.logger.info("Checking AdderTest results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AdderTest completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_adder(dut):
    """Cocotb test wrapper for AdderTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["AdderTest"] = AdderTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("AdderTest")

if __name__ == "__main__":
    # Note: This is a structural example
    # In practice, you would use cocotb to run this with a simulator
    print("This is a pyuvm test structure example.")
    print("To run with cocotb, use the Makefile in the test directory.")

