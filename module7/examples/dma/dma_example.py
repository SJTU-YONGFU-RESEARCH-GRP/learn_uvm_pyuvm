"""
Module 7 Example 7.1: DMA Verification
Demonstrates complete DMA controller verification environment.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer


class DMATransaction(uvm_sequence_item):
    """Transaction for DMA verification."""
    
    def __init__(self, name="DMATransaction"):
        super().__init__(name)
        self.src_addr = 0
        self.dst_addr = 0
        self.length = 0
        self.channel = 0
        self.transfer_type = "SIMPLE"  # SIMPLE, SCATTER_GATHER
    
    def __str__(self):
        return (f"channel={self.channel}, type={self.transfer_type}, "
                f"src=0x{self.src_addr:08X}, dst=0x{self.dst_addr:08X}, "
                f"len={self.length}")


class DMASequence(uvm_sequence):
    """Sequence for DMA transfers."""
    
    async def body(self):
        """Generate DMA transfer transactions."""
        self.logger.info(f"[{self.get_name()}] Starting DMA sequence")
        
        # Simple transfer
        txn = DMATransaction()
        txn.channel = 0
        txn.transfer_type = "SIMPLE"
        txn.src_addr = 0x1000
        txn.dst_addr = 0x2000
        txn.length = 256
        await self.start_item(txn)
        await self.finish_item(txn)
        
        # Scatter-gather transfer
        txn = DMATransaction()
        txn.channel = 1
        txn.transfer_type = "SCATTER_GATHER"
        txn.src_addr = 0x3000
        txn.dst_addr = 0x4000
        txn.length = 512
        await self.start_item(txn)
        await self.finish_item(txn)


class DMARegisterDriver(uvm_driver):
    """Driver for DMA register interface."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building DMA register driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase - drive DMA register transactions."""
        self.logger.info(f"[{self.get_name()}] Starting DMA register driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Configuring DMA: {item}")
            
            # Configure DMA registers
            # In real code: cocotb.dut.dma_src_addr.value = item.src_addr
            # In real code: cocotb.dut.dma_dst_addr.value = item.dst_addr
            # In real code: cocotb.dut.dma_length.value = item.length
            # In real code: cocotb.dut.dma_start.value = 1
            
            await Timer(10, units="ns")
            await self.seq_item_port.item_done()


class DMAMonitor(uvm_monitor):
    """Monitor for DMA transfers."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building DMA monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - monitor DMA transfers."""
        self.logger.info(f"[{self.get_name()}] Starting DMA monitor")
        
        while True:
            # Monitor DMA transfer completion
            # In real code: await RisingEdge(cocotb.dut.dma_done)
            
            await Timer(20, units="ns")
            
            # Create transaction from monitored transfer
            txn = DMATransaction()
            txn.channel = 0  # Simulated
            txn.transfer_type = "SIMPLE"  # Simulated
            txn.src_addr = 0x1000  # Simulated
            txn.dst_addr = 0x2000  # Simulated
            txn.length = 256  # Simulated
            
            self.logger.info(f"[{self.get_name()}] Monitored DMA transfer: {txn}")
            self.ap.write(txn)


class DMAScoreboard(uvm_scoreboard):
    """Scoreboard for DMA verification."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building DMA scoreboard")
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.expected = []
        self.actual = []
        self.mismatches = []
    
    def write(self, txn):
        """Receive DMA transfer transactions."""
        self.actual.append(txn)
        self.logger.info(f"[{self.get_name()}] Scoreboard received: {txn}")
        
        # Check against expected
        if len(self.expected) > 0:
            exp = self.expected.pop(0)
            if (txn.src_addr == exp.src_addr and 
                txn.dst_addr == exp.dst_addr and 
                txn.length == exp.length):
                self.logger.info(f"[{self.get_name()}] Transfer match: {txn}")
            else:
                self.mismatches.append((exp, txn))
                self.logger.error(f"[{self.get_name()}] Transfer mismatch: expected={exp}, actual={txn}")
    
    def add_expected(self, txn):
        """Add expected DMA transfer."""
        self.expected.append(txn)
    
    def check_phase(self):
        """Check phase."""
        self.logger.info(f"[{self.get_name()}] DMA Scoreboard: expected={len(self.expected)}, "
                        f"actual={len(self.actual)}, mismatches={len(self.mismatches)}")


class DMACoverage(uvm_subscriber):
    """Coverage model for DMA verification."""
    
    def __init__(self, name="DMACoverage"):
        super().__init__(name)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.coverage_data = {
            'channels': set(),
            'transfer_types': set(),
            'length_ranges': {'small': 0, 'medium': 0, 'large': 0}
        }
    
    def write(self, txn):
        """Sample coverage."""
        self.coverage_data['channels'].add(txn.channel)
        self.coverage_data['transfer_types'].add(txn.transfer_type)
        
        if txn.length < 256:
            self.coverage_data['length_ranges']['small'] += 1
        elif txn.length < 1024:
            self.coverage_data['length_ranges']['medium'] += 1
        else:
            self.coverage_data['length_ranges']['large'] += 1
    
    def report_phase(self):
        """Report coverage."""
        self.logger.info(f"[{self.get_name()}] DMA Coverage:")
        self.logger.info(f"  Channels: {len(self.coverage_data['channels'])}")
        self.logger.info(f"  Transfer types: {self.coverage_data['transfer_types']}")
        self.logger.info(f"  Length ranges: {self.coverage_data['length_ranges']}")


class DMAAgent(uvm_agent):
    """Agent for DMA register interface."""
    
    def build_phase(self):
        self.logger.info("Building DMAAgent")
        self.driver = DMARegisterDriver.create("driver", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class DMAEnv(uvm_env):
    """Environment for DMA verification."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building DMA Environment")
        self.logger.info("=" * 60)
        self.agent = DMAAgent.create("agent", self)
        self.monitor = DMAMonitor.create("monitor", self)
        self.scoreboard = DMAScoreboard.create("scoreboard", self)
        self.coverage = DMACoverage.create("coverage", self)
    
    def connect_phase(self):
        self.logger.info("Connecting DMA Environment")
        self.monitor.ap.connect(self.scoreboard.ap)
        self.monitor.ap.connect(self.coverage.ap)


@uvm_test()
class DMATest(uvm_test):
    """Test demonstrating DMA verification."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("DMA Verification Example Test")
        self.logger.info("=" * 60)
        self.env = DMAEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running DMA test")
        
        # Add expected transfers
        txn = DMATransaction()
        txn.channel = 0
        txn.src_addr = 0x1000
        txn.dst_addr = 0x2000
        txn.length = 256
        self.env.scoreboard.add_expected(txn)
        
        # Start DMA sequence
        seq = DMASequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("DMA test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm DMA verification example.")
    print("To run with cocotb, use the Makefile in the test directory.")

