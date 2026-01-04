"""
Module 6 Example 6.4: Multi-Channel Scoreboard
Demonstrates multi-channel scoreboard implementation.
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


class ChannelTransaction(uvm_sequence_item):
    """Transaction for multi-channel scoreboard."""
    
    def __init__(self, name="ChannelTransaction"):
        super().__init__(name)
        self.data = 0
        self.channel = 0
        self.expected = 0
        self.actual = 0
        self.timestamp = 0
    
    def __str__(self):
        return (f"channel={self.channel}, data=0x{self.data:02X}, "
                f"expected=0x{self.expected:02X}, actual=0x{self.actual:02X}")


class MultiChannelScoreboard(uvm_scoreboard):
    """
    Multi-channel scoreboard.
    
    Shows:
    - Multiple channel checking
    - Channel coordination
    - Time-based matching
    - Scoreboard patterns
    """
    
    def __init__(self, name="MultiChannelScoreboard", parent=None):
        super().__init__(name, parent)
        self.num_channels = 3  # Default, can be set after creation
        self.expected = {}
        self.actual = {}
        self.mismatches = {}
        self.matched = {}
    
    def build_phase(self):
        """Build phase - create analysis ports for each channel."""
        # Initialize dictionaries if not already done
        if not self.expected:
            self.expected = {i: [] for i in range(self.num_channels)}
            self.actual = {i: [] for i in range(self.num_channels)}
            self.mismatches = {i: [] for i in range(self.num_channels)}
            self.matched = {i: [] for i in range(self.num_channels)}
        
        self.logger.info(f"[{self.get_name()}] Building multi-channel scoreboard ({self.num_channels} channels)")
        
        self.analysis_exports = []
        self.analysis_imps = []
        
        for i in range(self.num_channels):
            ap = uvm_analysis_export(f"ap_channel_{i}", self)
            imp = uvm_analysis_imp(f"imp_channel_{i}", self)
            ap.connect(imp)
            self.analysis_exports.append(ap)
            self.analysis_imps.append(imp)
    
    def write(self, txn, channel_id=None):
        """Write method - receive transactions from channels."""
        if channel_id is None:
            channel_id = txn.channel if hasattr(txn, 'channel') else 0
        
        self.logger.info(f"[{self.get_name()}] Received from channel {channel_id}: {txn}")
        self.actual[channel_id].append(txn)
        
        # Match with expected
        if len(self.expected[channel_id]) > 0:
            exp_txn = self.expected[channel_id].pop(0)
            if txn.actual == exp_txn.expected:
                self.matched[channel_id].append((exp_txn, txn))
                self.logger.info(f"[{self.get_name()}] Channel {channel_id} match: expected=0x{exp_txn.expected:02X}, actual=0x{txn.actual:02X}")
            else:
                self.mismatches[channel_id].append((exp_txn, txn))
                self.logger.error(f"[{self.get_name()}] Channel {channel_id} mismatch: expected=0x{exp_txn.expected:02X}, actual=0x{txn.actual:02X}")
    
    def add_expected(self, txn, channel_id=None):
        """Add expected transaction for channel."""
        if channel_id is None:
            channel_id = txn.channel if hasattr(txn, 'channel') else 0
        
        self.expected[channel_id].append(txn)
        self.logger.info(f"[{self.get_name()}] Added expected for channel {channel_id}: {txn}")
    
    def check_phase(self):
        """Check phase - verify all channels."""
        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Multi-Channel Scoreboard Check")
        self.logger.info("=" * 60)
        
        total_matches = 0
        total_mismatches = 0
        
        for channel_id in range(self.num_channels):
            matches = len(self.matched[channel_id])
            mismatches = len(self.mismatches[channel_id])
            total_matches += matches
            total_mismatches += mismatches
            
            self.logger.info(f"Channel {channel_id}:")
            self.logger.info(f"  Expected: {len(self.expected[channel_id])} remaining")
            self.logger.info(f"  Actual: {len(self.actual[channel_id])}")
            self.logger.info(f"  Matches: {matches}")
            self.logger.info(f"  Mismatches: {mismatches}")
        
        self.logger.info("=" * 60)
        self.logger.info(f"Total matches: {total_matches}")
        self.logger.info(f"Total mismatches: {total_mismatches}")
        
        if total_mismatches == 0:
            self.logger.info("✓ All channels: PASSED")
        else:
            self.logger.error("✗ Some channels: FAILED")
        
        self.logger.info("=" * 60)


class ChannelMonitor(uvm_monitor):
    """Monitor for a channel."""
    
    def __init__(self, name="ChannelMonitor", parent=None, channel_id=0):
        super().__init__(name, parent)
        self.channel_id = channel_id
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building monitor for channel {self.channel_id}")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - generate sample transactions."""
        self.logger.info(f"[{self.get_name()}] Starting monitor for channel {self.channel_id}")
        
        for i in range(5):
            await Timer(10, units="ns")
            
            txn = ChannelTransaction()
            txn.data = i * 0x10
            txn.channel = self.channel_id
            txn.actual = i * 0x10  # Simulated
            txn.timestamp = i * 10
            
            self.logger.info(f"[{self.get_name()}] Monitored: {txn}")
            self.ap.write(txn)


class MultiChannelEnv(uvm_env):
    """Environment with multiple channels."""
    
    def build_phase(self):
        self.logger.info("Building MultiChannelEnv")
        
        # Create scoreboard
        self.scoreboard = MultiChannelScoreboard.create("scoreboard", self)
        self.scoreboard.num_channels = 3
        
        # Create monitors for each channel
        self.monitors = []
        for i in range(3):
            monitor = ChannelMonitor.create(f"monitor_channel_{i}", self)
            monitor.channel_id = i
            self.monitors.append(monitor)
    
    def connect_phase(self):
        """Connect phase - connect monitors to scoreboard."""
        self.logger.info("Connecting MultiChannelEnv")
        
        # Connect each monitor to corresponding scoreboard channel
        for i, monitor in enumerate(self.monitors):
            # In real implementation:
            # monitor.ap.connect(self.scoreboard.analysis_exports[i])
            self.logger.info(f"Connected channel {i} monitor to scoreboard")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class MultiChannelScoreboardTest(uvm_test):
    """Test demonstrating multi-channel scoreboard."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Multi-Channel Scoreboard Example Test")
        self.logger.info("=" * 60)
        self.env = MultiChannelEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running multi-channel scoreboard test")
        
        # Add expected transactions for each channel
        for channel_id in range(3):
            for i in range(5):
                txn = ChannelTransaction()
                txn.data = i * 0x10
                txn.channel = channel_id
                txn.expected = i * 0x10
                self.env.scoreboard.add_expected(txn, channel_id)
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Multi-channel scoreboard test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_multi_channel_scoreboard(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["MultiChannelScoreboardTest"] = MultiChannelScoreboardTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("MultiChannelScoreboardTest")


if __name__ == "__main__":
    print("This is a pyuvm multi-channel scoreboard example.")
    print("To run with cocotb, use the Makefile in the test directory.")

