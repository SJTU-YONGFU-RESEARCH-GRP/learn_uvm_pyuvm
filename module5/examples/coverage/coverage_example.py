"""
Module 5 Example 5.2: UVM Coverage Models
Demonstrates functional coverage implementation.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer

# Explicit imports for TLM classes that may not be in __all__
try:
    # Try to get it from globals first (in case from pyuvm import * worked)
    uvm_analysis_imp  # type: ignore
except NameError:
    # Not in globals, try to import it explicitly
    _found = False
    # Try TLM module paths
    for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
        try:
            tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_analysis_imp'])
            if hasattr(tlm_module, 'uvm_analysis_imp'):
                uvm_analysis_imp = getattr(tlm_module, 'uvm_analysis_imp')  # type: ignore
                _found = True
                break
        except (ImportError, AttributeError):
            continue
    # If still not found, try pyuvm module directly
    if not _found:
        import pyuvm
        if hasattr(pyuvm, 'uvm_analysis_imp'):
            uvm_analysis_imp = getattr(pyuvm, 'uvm_analysis_imp')  # type: ignore
            _found = True
    if not _found:
        # This should not happen if pyuvm is properly installed
        raise ImportError("Could not import uvm_analysis_imp from pyuvm")


class CoverageTransaction(uvm_sequence_item):
    """Transaction for coverage example."""
    
    def __init__(self, name="CoverageTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.command = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, cmd=0x{self.command:02X}"


class CoverageModel(uvm_subscriber):
    """
    Coverage model demonstrating functional coverage.
    
    Shows:
    - Coverage class structure
    - Coverpoints and bins
    - Coverage sampling
    - Coverage analysis
    """
    
    def __init__(self, name="CoverageModel", parent=None):
        super().__init__(name, parent)
        # Coverage data structures
        self.data_coverage = {}  # data -> count
        self.address_ranges = {
            'low': 0,      # 0x0000-0x3FFF
            'mid': 0,      # 0x4000-0x7FFF
            'high': 0      # 0x8000-0xFFFF
        }
        self.command_coverage = {}  # command -> count
        self.cross_coverage = {}  # (data, command) -> count
    
    def build_phase(self):
        """Build phase - create analysis ports."""
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
    
    def write(self, txn):
        """Write method - sample coverage."""
        self.logger.debug(f"[{self.get_name()}] Sampling coverage for: {txn}")
        
        # Sample data coverage
        if txn.data not in self.data_coverage:
            self.data_coverage[txn.data] = 0
        self.data_coverage[txn.data] += 1
        
        # Sample address range coverage
        if txn.address < 0x4000:
            self.address_ranges['low'] += 1
        elif txn.address < 0x8000:
            self.address_ranges['mid'] += 1
        else:
            self.address_ranges['high'] += 1
        
        # Sample command coverage
        if txn.command not in self.command_coverage:
            self.command_coverage[txn.command] = 0
        self.command_coverage[txn.command] += 1
        
        # Sample cross coverage
        key = (txn.data, txn.command)
        if key not in self.cross_coverage:
            self.cross_coverage[key] = 0
        self.cross_coverage[key] += 1
    
    def get_coverage(self):
        """Get coverage statistics."""
        total_data = len(self.data_coverage)
        total_commands = len(self.command_coverage)
        total_cross = len(self.cross_coverage)
        
        return {
            'data_coverage': total_data,
            'address_low': self.address_ranges['low'],
            'address_mid': self.address_ranges['mid'],
            'address_high': self.address_ranges['high'],
            'command_coverage': total_commands,
            'cross_coverage': total_cross
        }
    
    def report_phase(self):
        """Report phase - print coverage report."""
        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Coverage Report")
        self.logger.info("=" * 60)
        
        coverage = self.get_coverage()
        self.logger.info(f"Data Coverage: {coverage['data_coverage']} unique values")
        self.logger.info(f"Address Coverage:")
        self.logger.info(f"  Low (0x0000-0x3FFF):  {coverage['address_low']} samples")
        self.logger.info(f"  Mid (0x4000-0x7FFF):  {coverage['address_mid']} samples")
        self.logger.info(f"  High (0x8000-0xFFFF): {coverage['address_high']} samples")
        self.logger.info(f"Command Coverage: {coverage['command_coverage']} unique commands")
        self.logger.info(f"Cross Coverage: {coverage['cross_coverage']} unique combinations")
        
        # Coverage percentage (simplified)
        max_data = 256  # 8-bit data
        max_commands = 256  # 8-bit command
        data_percent = (coverage['data_coverage'] / max_data) * 100
        cmd_percent = (coverage['command_coverage'] / max_commands) * 100
        
        self.logger.info(f"Data Coverage: {data_percent:.1f}%")
        self.logger.info(f"Command Coverage: {cmd_percent:.1f}%")
        self.logger.info("=" * 60)


class CoverageMonitor(uvm_monitor):
    """Monitor that sends transactions to coverage."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building coverage monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - generate sample transactions."""
        self.logger.info(f"[{self.get_name()}] Starting coverage monitor")
        
        # Generate sample transactions for coverage
        test_vectors = [
            (0x00, 0x1000, 0x01),
            (0x01, 0x2000, 0x02),
            (0xFF, 0x8000, 0x03),
            (0x7F, 0x5000, 0x01),
            (0x0A, 0x9000, 0x02),
        ]
        
        for data, addr, cmd in test_vectors:
            txn = CoverageTransaction()
            txn.data = data
            txn.address = addr
            txn.command = cmd
            self.ap.write(txn)
            await Timer(10, units="ns")


class CoverageEnv(uvm_env):
    """Environment with coverage."""
    
    def build_phase(self):
        self.logger.info("Building CoverageEnv")
        self.monitor = CoverageMonitor.create("monitor", self)
        self.coverage = CoverageModel.create("coverage", self)
    
    def connect_phase(self):
        self.logger.info("Connecting CoverageEnv")
        self.monitor.ap.connect(self.coverage.ap)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class CoverageTest(uvm_test):
    """Test demonstrating coverage model."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Coverage Example Test")
        self.logger.info("=" * 60)
        self.env = CoverageEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running coverage test")
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Coverage test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_coverage(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["CoverageTest"] = CoverageTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("CoverageTest")


if __name__ == "__main__":
    print("This is a pyuvm coverage example.")
    print("To run with cocotb, use the Makefile in the test directory.")

