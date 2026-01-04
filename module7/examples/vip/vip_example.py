"""
Module 7 Example: VIP (Verification IP) Development
Demonstrates creating reusable verification IP.
"""

from pyuvm import *


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
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class VIPMonitor(uvm_monitor):
    """Monitor for VIP."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building VIP monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase."""
        while True:
            await Timer(10, units="ns")
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
    
    def __init__(self, name="VIPCoverage"):
        super().__init__(name)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.coverage_data = {}
    
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


@uvm_test()
class VIPTest(uvm_test):
    """Test demonstrating VIP usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("VIP Development Example Test")
        self.logger.info("=" * 60)
        self.env = VIPEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running VIP test")
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("VIP test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm VIP example.")
    print("To run with cocotb, use the Makefile in the test directory.")

