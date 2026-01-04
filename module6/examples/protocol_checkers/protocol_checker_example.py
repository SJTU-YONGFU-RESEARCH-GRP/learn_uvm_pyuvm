"""
Module 6 Example 6.3: Protocol Checker
Demonstrates protocol compliance checking.
"""

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
import cocotb
from cocotb.triggers import Timer


class ProtocolTransaction(uvm_sequence_item):
    """Transaction for protocol checker."""
    
    def __init__(self, name="ProtocolTransaction"):
        super().__init__(name)
        self.valid = False
        self.ready = False
        self.data = 0
        self.timestamp = 0
    
    def __str__(self):
        return f"valid={self.valid}, ready={self.ready}, data=0x{self.data:02X}"


class ProtocolChecker(uvm_component):
    """
    Protocol checker for compliance verification.
    
    Shows:
    - Protocol rule checking
    - Error detection
    - Protocol compliance monitoring
    """
    
    def __init__(self, name="ProtocolChecker", parent=None):
        super().__init__(name, parent)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        
        # Protocol state
        self.prev_valid = False
        self.prev_ready = False
        self.errors = []
        self.warnings = []
    
    def write(self, txn):
        """Write method - check protocol compliance."""
        self.logger.debug(f"[{self.get_name()}] Checking: {txn}")
        
        # Protocol Rule 1: valid should not change while ready is asserted
        if self.prev_ready and self.prev_valid and txn.valid != self.prev_valid:
            error = f"Protocol violation: valid changed while ready asserted at time {txn.timestamp}"
            self.errors.append(error)
            self.logger.error(f"[{self.get_name()}] {error}")
        
        # Protocol Rule 2: ready should not change while valid is asserted
        if self.prev_valid and self.prev_ready and txn.ready != self.prev_ready:
            error = f"Protocol violation: ready changed while valid asserted at time {txn.timestamp}"
            self.errors.append(error)
            self.logger.error(f"[{self.get_name()}] {error}")
        
        # Protocol Rule 3: Data should be valid when valid and ready are both high
        if txn.valid and txn.ready:
            self.logger.info(f"[{self.get_name()}] Protocol OK: Valid handshake, data=0x{txn.data:02X}")
        
        # Protocol Rule 4: Warning if valid asserted without ready
        if txn.valid and not txn.ready:
            warning = f"Warning: valid asserted without ready at time {txn.timestamp}"
            self.warnings.append(warning)
            self.logger.warning(f"[{self.get_name()}] {warning}")
        
        # Update previous state
        self.prev_valid = txn.valid
        self.prev_ready = txn.ready
    
    def check_phase(self):
        """Check phase - report protocol compliance."""
        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Protocol Checker Report")
        self.logger.info("=" * 60)
        self.logger.info(f"Total errors: {len(self.errors)}")
        self.logger.info(f"Total warnings: {len(self.warnings)}")
        
        if len(self.errors) == 0:
            self.logger.info("✓ Protocol compliance: PASSED")
        else:
            self.logger.error("✗ Protocol compliance: FAILED")
            for error in self.errors:
                self.logger.error(f"  {error}")
        
        if len(self.warnings) > 0:
            for warning in self.warnings:
                self.logger.warning(f"  {warning}")
        
        self.logger.info("=" * 60)


class ProtocolMonitor(uvm_monitor):
    """Monitor that sends transactions to protocol checker."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building protocol monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - generate sample protocol transactions."""
        self.logger.info(f"[{self.get_name()}] Starting protocol monitor")
        
        # Generate protocol transactions (some valid, some invalid)
        protocol_vectors = [
            (False, False, 0x00),  # Idle
            (True, False, 0xAA),   # Valid without ready (warning)
            (True, True, 0xBB),    # Valid handshake (OK)
            (False, True, 0xCC),   # Ready without valid (OK)
            (True, False, 0xDD),   # Valid without ready (warning)
            (False, False, 0x00),  # Idle
            (True, True, 0xEE),    # Valid handshake (OK)
        ]
        
        for i, (valid, ready, data) in enumerate(protocol_vectors):
            txn = ProtocolTransaction()
            txn.valid = valid
            txn.ready = ready
            txn.data = data
            txn.timestamp = i * 10
            
            self.ap.write(txn)
            await Timer(10, unit="ns")


class ProtocolEnv(uvm_env):
    """Environment with protocol checker."""
    
    def build_phase(self):
        self.logger.info("Building ProtocolEnv")
        self.monitor = ProtocolMonitor.create("monitor", self)
        self.checker = ProtocolChecker.create("checker", self)
    
    def connect_phase(self):
        self.logger.info("Connecting ProtocolEnv")
        self.monitor.ap.connect(self.checker.ap)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class ProtocolCheckerTest(uvm_test):
    """Test demonstrating protocol checker."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Protocol Checker Example Test")
        self.logger.info("=" * 60)
        self.env = ProtocolEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running protocol checker test")
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Protocol checker test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_protocol_checker(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ProtocolCheckerTest"] = ProtocolCheckerTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ProtocolCheckerTest")


if __name__ == "__main__":
    print("This is a pyuvm protocol checker example.")
    print("To run with cocotb, use the Makefile in the test directory.")

