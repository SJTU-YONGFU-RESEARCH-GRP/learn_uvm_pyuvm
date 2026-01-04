"""
Module 7 Example: SPI Protocol Verification
Demonstrates SPI protocol verification with master-slave coordination.
"""

from pyuvm import *

# Explicitly import TLM classes that may not be in __all__
# Try direct imports from known TLM module paths
try:
    from pyuvm.s15_uvm_tlm_1 import uvm_seq_item_pull_port
except (ImportError, AttributeError):
    try:
        from pyuvm.s15_uvm_tlm import uvm_seq_item_pull_port
    except (ImportError, AttributeError):
        try:
            from pyuvm.s16_uvm_tlm_1 import uvm_seq_item_pull_port
        except (ImportError, AttributeError):
            try:
                from pyuvm.s16_uvm_tlm import uvm_seq_item_pull_port
            except (ImportError, AttributeError):
                # If all imports fail, try to get from globals (might be available from pyuvm import *)
                try:
                    uvm_seq_item_pull_port = globals()['uvm_seq_item_pull_port']
                except KeyError:
                    pass

import cocotb
from cocotb.triggers import Timer, RisingEdge


class SPITransaction(uvm_sequence_item):
    """Transaction for SPI verification."""
    
    def __init__(self, name="SPITransaction"):
        super().__init__(name)
        self.data = 0
        self.mode = 0  # SPI mode (0-3)
        self.cs = 0  # Chip select
        self.is_master = True
    
    def __str__(self):
        role = "MASTER" if self.is_master else "SLAVE"
        return f"{role}: data=0x{self.data:02X}, mode={self.mode}, cs={self.cs}"


class SPIDriver(uvm_driver):
    """Driver for SPI protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building SPI driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase - implement SPI transmission."""
        self.logger.info(f"[{self.get_name()}] Starting SPI driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Transmitting SPI: {item}")
            
            # SPI transmission: CS low -> Clock data -> CS high
            # In real code: cocotb.dut.cs.value = 0  # Assert CS
            # In real code: for i in range(8):  # 8 bits
            # In real code:     cocotb.dut.sclk.value = 0
            # In real code:     cocotb.dut.mosi.value = (item.data >> (7-i)) & 1
            # In real code:     await Timer(period/2, units="ns")
            # In real code:     cocotb.dut.sclk.value = 1
            # In real code:     await Timer(period/2, units="ns")
            # In real code: cocotb.dut.cs.value = 1  # Deassert CS
            
            await Timer(100, unit="ns")
            await self.seq_item_port.item_done()


class SPIMonitor(uvm_monitor):
    """Monitor for SPI protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building SPI monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - monitor SPI reception."""
        self.logger.info(f"[{self.get_name()}] Starting SPI monitor")
        
        while True:
            # Monitor SPI reception
            # In real code: await FallingEdge(cocotb.dut.cs)  # CS asserted
            # In real code: data = 0
            # In real code: for i in range(8):  # 8 bits
            # In real code:     await RisingEdge(cocotb.dut.sclk)
            # In real code:     data |= (cocotb.dut.miso.value << (7-i))
            
            await Timer(100, unit="ns")
            
            txn = SPITransaction()
            txn.data = 0xBB  # Simulated
            txn.mode = 0
            txn.cs = 0
            
            self.logger.info(f"[{self.get_name()}] Received SPI: {txn}")
            self.ap.write(txn)


class SPIAgent(uvm_agent):
    """Agent for SPI protocol."""
    
    def build_phase(self):
        self.logger.info("Building SPI agent")
        self.driver = SPIDriver.create("driver", self)
        self.monitor = SPIMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class SPISequence(uvm_sequence):
    """Sequence for SPI transactions."""
    
    async def body(self):
        """Generate SPI transactions."""
        test_data = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        
        for data in test_data:
            txn = SPITransaction()
            txn.data = data
            txn.mode = 0
            txn.cs = 0
            txn.is_master = True
            
            await self.start_item(txn)
            await self.finish_item(txn)


class SPIEnv(uvm_env):
    """Environment for SPI verification."""
    
    def build_phase(self):
        self.logger.info("Building SPIEnv")
        self.master_agent = SPIAgent.create("master_agent", self)
        self.slave_agent = SPIAgent.create("slave_agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting SPIEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class SPITest(uvm_test):
    """Test demonstrating SPI protocol verification."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("SPI Protocol Example Test")
        self.logger.info("=" * 60)
        self.env = SPIEnv.create("env", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting SPI Test")
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running SPI test")
        
        # Start SPI sequence on master
        seq = SPISequence.create("seq")
        await seq.start(self.env.master_agent.seqr)
        
        await Timer(1000, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("Checking SPI test results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("SPI test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_spi(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["SPITest"] = SPITest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("SPITest")


if __name__ == "__main__":
    print("This is a pyuvm SPI protocol example.")
    print("To run with cocotb, use the Makefile in the test directory.")

