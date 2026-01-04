"""
Module 6 Example 6.2: Protocol Verification (AXI4-Lite)
Demonstrates AXI4-Lite protocol verification agent.
"""

from pyuvm import *

# In pyuvm, use uvm_seq_item_port instead of uvm_seq_item_pull_port
# uvm_seq_item_port is available from pyuvm import * and works the same way
try:
    uvm_seq_item_pull_port  # type: ignore
except NameError:
    # Use uvm_seq_item_port as it's the correct class in pyuvm
    uvm_seq_item_pull_port = uvm_seq_item_port

# Also create alias for uvm_analysis_imp if not available
try:
    uvm_analysis_imp  # type: ignore
except NameError:
    # Try to find the correct analysis implementation class
    try:
        from pyuvm.s12_uvm_tlm_interfaces import uvm_analysis_imp_decl
        uvm_analysis_imp = uvm_analysis_imp_decl
    except ImportError:
        # If not found, try uvm_analysis_export which can implement write
        try:
            uvm_analysis_imp = uvm_analysis_export
        except NameError:
            # Last resort - use uvm_analysis_port (won't work but won't crash)
            uvm_analysis_imp = uvm_analysis_port
import cocotb
from cocotb.triggers import Timer, RisingEdge


class AXI4LiteTransaction(uvm_sequence_item):
    """
    AXI4-Lite transaction.
    
    Simplified AXI4-Lite transaction for demonstration.
    """
    
    def __init__(self, name="AXI4LiteTransaction"):
        super().__init__(name)
        self.addr = 0
        self.data = 0
        self.is_write = True
        self.prot = 0  # Protection type
        self.strb = 0  # Write strobe
    
    def __str__(self):
        op = "WRITE" if self.is_write else "READ"
        return f"{op}: addr=0x{self.addr:08X}, data=0x{self.data:08X}"


class AXI4LiteDriver(uvm_driver):
    """
    AXI4-Lite driver.
    
    Implements AXI4-Lite write and read protocols.
    """
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building AXI4-Lite driver")
        # pyuvm drivers already have seq_item_port by default
        # No need to create it manually
    
    async def run_phase(self):
        """Run phase - implement AXI4-Lite protocol."""
        self.logger.info(f"[{self.get_name()}] Starting AXI4-Lite driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            
            if item.is_write:
                await self.write_transaction(item)
            else:
                await self.read_transaction(item)
            
            self.seq_item_port.item_done()
    
    async def write_transaction(self, txn):
        """Implement AXI4-Lite write protocol."""
        self.logger.info(f"[{self.get_name()}] AXI4-Lite Write: {txn}")
        
        # AXI4-Lite Write Address Channel
        # In real code: cocotb.dut.awvalid.value = 1
        # In real code: cocotb.dut.awaddr.value = txn.addr
        # In real code: await RisingEdge(cocotb.dut.awready)
        await Timer(5, unit="ns")
        self.logger.info(f"[{self.get_name()}] Write address channel: addr=0x{txn.addr:08X}")
        
        # AXI4-Lite Write Data Channel
        # In real code: cocotb.dut.wvalid.value = 1
        # In real code: cocotb.dut.wdata.value = txn.data
        # In real code: cocotb.dut.wstrb.value = txn.strb
        await Timer(5, unit="ns")
        self.logger.info(f"[{self.get_name()}] Write data channel: data=0x{txn.data:08X}")
        
        # AXI4-Lite Write Response Channel
        # In real code: await RisingEdge(cocotb.dut.bvalid)
        # In real code: resp = cocotb.dut.bresp.value.integer
        await Timer(5, unit="ns")
        self.logger.info(f"[{self.get_name()}] Write response: OKAY")
    
    async def read_transaction(self, txn):
        """Implement AXI4-Lite read protocol."""
        self.logger.info(f"[{self.get_name()}] AXI4-Lite Read: {txn}")
        
        # AXI4-Lite Read Address Channel
        # In real code: cocotb.dut.arvalid.value = 1
        # In real code: cocotb.dut.araddr.value = txn.addr
        # In real code: await RisingEdge(cocotb.dut.arready)
        await Timer(5, unit="ns")
        self.logger.info(f"[{self.get_name()}] Read address channel: addr=0x{txn.addr:08X}")
        
        # AXI4-Lite Read Data Channel
        # In real code: await RisingEdge(cocotb.dut.rvalid)
        # In real code: txn.data = cocotb.dut.rdata.value.integer
        # In real code: resp = cocotb.dut.rresp.value.integer
        await Timer(5, unit="ns")
        self.logger.info(f"[{self.get_name()}] Read data channel: data=0x{txn.data:08X}")


class AXI4LiteMonitor(uvm_monitor):
    """AXI4-Lite monitor."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building AXI4-Lite monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - monitor AXI4-Lite protocol."""
        self.logger.info(f"[{self.get_name()}] Starting AXI4-Lite monitor")
        
        while True:
            # Monitor AXI4-Lite signals
            # In real code: await RisingEdge(cocotb.dut.awvalid)
            # In real code: await RisingEdge(cocotb.dut.wvalid)
            # In real code: await RisingEdge(cocotb.dut.bvalid)
            
            await Timer(10, unit="ns")
            
            # Create transaction from monitored signals
            txn = AXI4LiteTransaction()
            txn.addr = 0x1000  # Simulated
            txn.data = 0xABCDEF00  # Simulated
            txn.is_write = True  # Simulated
            
            self.logger.info(f"[{self.get_name()}] Monitored: {txn}")
            self.ap.write(txn)


class AXI4LiteAgent(uvm_agent):
    """AXI4-Lite agent."""
    
    def build_phase(self):
        self.logger.info("Building AXI4-Lite agent")
        self.driver = AXI4LiteDriver.create("driver", self)
        self.monitor = AXI4LiteMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting AXI4-Lite agent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AXI4LiteSequence(uvm_sequence):
    """Sequence for AXI4-Lite transactions."""
    
    async def body(self):
        """Generate AXI4-Lite transactions."""
        print(f"[{self.get_name()}] Starting AXI4-Lite sequence")
        
        # Write transactions
        for i in range(3):
            txn = AXI4LiteTransaction()
            txn.addr = 0x1000 + i * 4
            txn.data = 0xDEADBEEF + i
            txn.is_write = True
            txn.strb = 0xF
            
            await self.start_item(txn)
            await self.finish_item(txn)
        
        # Read transactions
        for i in range(3):
            txn = AXI4LiteTransaction()
            txn.addr = 0x1000 + i * 4
            txn.data = 0
            txn.is_write = False
            
            await self.start_item(txn)
            await self.finish_item(txn)


class AXI4LiteEnv(uvm_env):
    """Environment for AXI4-Lite verification."""
    
    def build_phase(self):
        self.logger.info("Building AXI4LiteEnv")
        self.agent = AXI4LiteAgent.create("agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting AXI4LiteEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class AXI4LiteTest(uvm_test):
    """Test demonstrating AXI4-Lite protocol verification."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AXI4-Lite Protocol Example Test")
        self.logger.info("=" * 60)
        self.env = AXI4LiteEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running AXI4-Lite test")
        
        # Start AXI4-Lite sequence
        seq = AXI4LiteSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("AXI4-Lite test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_protocol(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["AXI4LiteTest"] = AXI4LiteTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("AXI4LiteTest")


if __name__ == "__main__":
    print("This is a pyuvm AXI4-Lite protocol example.")
    print("To run with cocotb, use the Makefile in the test directory.")

