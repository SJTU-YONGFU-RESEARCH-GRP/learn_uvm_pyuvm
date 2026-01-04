"""
Module 7 Example: I2C Protocol Verification
Demonstrates I2C protocol verification with multi-master support.
"""

from pyuvm import *

# Use uvm_seq_item_port (pyuvm doesn't have uvm_seq_item_pull_port)
uvm_seq_item_pull_port = uvm_seq_item_port

import cocotb
from cocotb.triggers import Timer, RisingEdge


class I2CTransaction(uvm_sequence_item):
    """Transaction for I2C verification."""
    
    def __init__(self, name="I2CTransaction"):
        super().__init__(name)
        self.address = 0
        self.data = []
        self.is_write = True
        self.is_start = True
        self.is_stop = True
    
    def __str__(self):
        op = "WRITE" if self.is_write else "READ"
        return f"{op}: addr=0x{self.address:02X}, data={[hex(d) for d in self.data]}"


class I2CDriver(uvm_driver):
    """Driver for I2C protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building I2C driver")
        self.seq_item_port = uvm_seq_item_pull_port("i2c_driver_seq_item_port", self)
    
    async def run_phase(self):
        """Run phase - implement I2C transmission."""
        self.logger.info(f"[{self.get_name()}] Starting I2C driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Transmitting I2C: {item}")
            
            # I2C transmission: START -> Address -> R/W -> ACK -> Data -> ACK -> STOP
            # In real code: cocotb.dut.sda.value = 0  # START condition
            # In real code: await Timer(period, units="ns")
            # In real code: # Transmit address
            # In real code: for i in range(7):  # 7-bit address
            # In real code:     cocotb.dut.sda.value = (item.address >> (6-i)) & 1
            # In real code:     cocotb.dut.scl.value = 1
            # In real code:     await Timer(period, units="ns")
            # In real code:     cocotb.dut.scl.value = 0
            # In real code: # Transmit R/W bit
            # In real code: cocotb.dut.sda.value = 0 if item.is_write else 1
            # In real code: # Transmit data bytes
            # In real code: for byte in item.data:
            # In real code:     for i in range(8):  # 8 bits
            # In real code:         cocotb.dut.sda.value = (byte >> (7-i)) & 1
            # In real code:         cocotb.dut.scl.value = 1
            # In real code:         await Timer(period, units="ns")
            # In real code:         cocotb.dut.scl.value = 0
            # In real code: cocotb.dut.sda.value = 1  # STOP condition
            
            await Timer(200, unit="ns")
            self.seq_item_port.item_done()


class I2CMonitor(uvm_monitor):
    """Monitor for I2C protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building I2C monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - monitor I2C reception."""
        self.logger.info(f"[{self.get_name()}] Starting I2C monitor")
        
        while True:
            # Monitor I2C reception
            # In real code: await FallingEdge(cocotb.dut.sda)  # START condition
            # In real code: address = 0
            # In real code: for i in range(7):  # 7-bit address
            # In real code:     await RisingEdge(cocotb.dut.scl)
            # In real code:     address |= (cocotb.dut.sda.value << (6-i))
            # In real code:     await FallingEdge(cocotb.dut.scl)
            
            await Timer(200, unit="ns")
            
            txn = I2CTransaction()
            txn.address = 0x50  # Simulated
            txn.data = [0xAA, 0xBB]  # Simulated
            txn.is_write = True
            
            self.logger.info(f"[{self.get_name()}] Received I2C: {txn}")
            self.ap.write(txn)


class I2CAgent(uvm_agent):
    """Agent for I2C protocol."""
    
    def build_phase(self):
        self.logger.info("Building I2C agent")
        self.driver = I2CDriver.create("driver", self)
        self.monitor = I2CMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class I2CSequence(uvm_sequence):
    """Sequence for I2C transactions."""
    
    async def body(self):
        """Generate I2C transactions."""
        # Write transaction
        txn = I2CTransaction()
        txn.address = 0x50
        txn.data = [0x01, 0x02, 0x03]
        txn.is_write = True
        await self.start_item(txn)
        await self.finish_item(txn)
        
        # Read transaction
        txn = I2CTransaction()
        txn.address = 0x50
        txn.data = []
        txn.is_write = False
        await self.start_item(txn)
        await self.finish_item(txn)


class I2CEnv(uvm_env):
    """Environment for I2C verification."""
    
    def build_phase(self):
        self.logger.info("Building I2CEnv")
        self.master1_agent = I2CAgent.create("master1_agent", self)
        self.master2_agent = I2CAgent.create("master2_agent", self)
        self.slave_agent = I2CAgent.create("slave_agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting I2CEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class I2CTest(uvm_test):
    """Test demonstrating I2C protocol verification."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("I2C Protocol Example Test")
        self.logger.info("=" * 60)
        self.env = I2CEnv.create("env", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting I2C Test")
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running I2C test")
        
        # Start I2C sequence on master
        seq = I2CSequence.create("seq")
        await seq.start(self.env.master1_agent.seqr)
        
        await Timer(1000, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("Checking I2C test results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("I2C test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_i2c(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["I2CTest"] = I2CTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("I2CTest")


if __name__ == "__main__":
    print("This is a pyuvm I2C protocol example.")
    print("To run with cocotb, use the Makefile in the test directory.")

