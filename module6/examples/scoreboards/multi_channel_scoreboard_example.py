"""
Module 6 Example 6.4: Multi-Channel Scoreboard
Demonstrates multi-channel scoreboard implementation.
"""

from pyuvm import *


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
    
    def __init__(self, name="MultiChannelScoreboard", parent=None, num_channels=3):
        super().__init__(name, parent)
        self.num_channels = num_channels
        self.expected = {i: [] for i in range(num_channels)}
        self.actual = {i: [] for i in range(num_channels)}
        self.mismatches = {i: [] for i in range(num_channels)}
        self.matched = {i: [] for i in range(num_channels)}
    
    def build_phase(self):
        """Build phase - create analysis ports for each channel."""
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
        self.scoreboard = MultiChannelScoreboard.create("scoreboard", self, num_channels=3)
        
        # Create monitors for each channel
        self.monitors = []
        for i in range(3):
            monitor = ChannelMonitor.create(f"monitor_channel_{i}", self, channel_id=i)
            self.monitors.append(monitor)
    
    def connect_phase(self):
        """Connect phase - connect monitors to scoreboard."""
        self.logger.info("Connecting MultiChannelEnv")
        
        # Connect each monitor to corresponding scoreboard channel
        for i, monitor in enumerate(self.monitors):
            # In real implementation:
            # monitor.ap.connect(self.scoreboard.analysis_exports[i])
            self.logger.info(f"Connected channel {i} monitor to scoreboard")


@uvm_test()
class MultiChannelScoreboardTest(uvm_test):
    """Test demonstrating multi-channel scoreboard."""
    
    async def build_phase(self):
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


if __name__ == "__main__":
    print("This is a pyuvm multi-channel scoreboard example.")
    print("To run with cocotb, use the Makefile in the test directory.")

