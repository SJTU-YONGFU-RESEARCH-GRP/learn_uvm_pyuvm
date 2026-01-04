"""
Module 7 Example: VIP (Verification IP) Development
Demonstrates creating reusable verification IP.
"""

from pyuvm import *

# Explicitly import TLM classes that may not be in __all__
# Try direct imports from known TLM module paths
try:
    from pyuvm.s15_uvm_tlm_1 import uvm_seq_item_pull_port, uvm_analysis_imp
except (ImportError, AttributeError):
    try:
        from pyuvm.s15_uvm_tlm import uvm_seq_item_pull_port, uvm_analysis_imp
    except (ImportError, AttributeError):
        try:
            from pyuvm.s16_uvm_tlm_1 import uvm_seq_item_pull_port, uvm_analysis_imp
        except (ImportError, AttributeError):
            try:
                from pyuvm.s16_uvm_tlm import uvm_seq_item_pull_port, uvm_analysis_imp
            except (ImportError, AttributeError):
                # If all imports fail, try to get from globals (might be available from pyuvm import *)
                try:
                    uvm_seq_item_pull_port = globals()['uvm_seq_item_pull_port']
                except KeyError:
                    pass
                try:
                    uvm_analysis_imp = globals()['uvm_analysis_imp']
                except KeyError:
                    pass

import cocotb
from cocotb.triggers import Timer


class VIPTransaction(uvm_sequence_item):
    """Transaction for VIP example."""
    
    def __init__(self, name="VIPTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class VIPDriver(uvm_driver):
    """Driver for VIP."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building VIP driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase."""
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Driving: {item}")
            await Timer(10, unit="ns")
            await self.seq_item_port.item_done()


class VIPMonitor(uvm_monitor):
    """Monitor for VIP."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building VIP monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase."""
        while True:
            await Timer(10, unit="ns")
            txn = VIPTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            self.ap.write(txn)


class VIPChecker(uvm_component):
    """Protocol checker for VIP."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building VIP checker")
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.errors = []
    
    def write(self, txn):
        """Check protocol compliance."""
        self.logger.debug(f"[{self.get_name()}] Checking: {txn}")
        # Protocol checking logic here
    
    def check_phase(self):
        """Check phase."""
        if len(self.errors) == 0:
            self.logger.info(f"[{self.get_name()}] Protocol compliance: PASSED")
        else:
            self.logger.error(f"[{self.get_name()}] Protocol compliance: FAILED")


class VIPCoverage(uvm_subscriber):
    """Coverage model for VIP."""
    
    def __init__(self, name="VIPCoverage", parent=None):
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
    
    def report_phase(self):
        """Report coverage."""
        self.logger.info(f"[{self.get_name()}] Coverage: {len(self.coverage_data)} unique values")


class VIPAgent(uvm_agent):
    """
    Complete VIP agent.
    
    Shows:
    - VIP structure
    - VIP components
    - VIP configuration
    - VIP reusability
    """
    
    def build_phase(self):
        """Build phase - create VIP components."""
        self.logger.info(f"[{self.get_name()}] Building VIP agent")
        
        # Get VIP configuration
        self.active = True
        config = None
        if ConfigDB().get(None, "", f"{self.get_full_name()}.active", config):
            self.active = config
        
        # Always create monitor
        self.monitor = VIPMonitor.create("monitor", self)
        self.checker = VIPChecker.create("checker", self)
        self.coverage = VIPCoverage.create("coverage", self)
        
        # Create driver and sequencer only if active
        if self.active:
            self.driver = VIPDriver.create("driver", self)
            self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        """Connect phase - connect VIP components."""
        self.logger.info(f"[{self.get_name()}] Connecting VIP agent")
        
        if self.active:
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        
        # Connect monitor to checker and coverage
        self.monitor.ap.connect(self.checker.ap)
        self.monitor.ap.connect(self.coverage.ap)


class VIPEnv(uvm_env):
    """Environment using VIP."""
    
    def build_phase(self):
        self.logger.info("Building VIPEnv")
        self.vip = VIPAgent.create("vip", self)
    
    def connect_phase(self):
        self.logger.info("Connecting VIPEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class VIPTest(uvm_test):
    """Test demonstrating VIP usage."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("VIP Development Example Test")
        self.logger.info("=" * 60)
        self.env = VIPEnv.create("env", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting VIP Test")
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running VIP test")
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("Checking VIP test results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("VIP test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_vip(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["VIPTest"] = VIPTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("VIPTest")


if __name__ == "__main__":
    print("This is a pyuvm VIP example.")
    print("To run with cocotb, use the Makefile in the test directory.")

