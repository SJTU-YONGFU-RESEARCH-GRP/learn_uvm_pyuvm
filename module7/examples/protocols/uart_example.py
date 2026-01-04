"""
Module 7 Example: UART Protocol Verification
Demonstrates UART protocol verification agent.
"""

from pyuvm import *

# Use uvm_seq_item_port (pyuvm doesn't have uvm_seq_item_pull_port)
uvm_seq_item_pull_port = uvm_seq_item_port

import cocotb
from cocotb.triggers import Timer, RisingEdge


class UARTTransaction(uvm_sequence_item):
    """Transaction for UART verification."""
    
    def __init__(self, name="UARTTransaction"):
        super().__init__(name)
        self.data = 0
        self.baud_rate = 9600
        self.parity = "NONE"  # NONE, EVEN, ODD
        self.stop_bits = 1
    
    def __str__(self):
        return f"data=0x{self.data:02X}, baud={self.baud_rate}, parity={self.parity}"


class UARTDriver(uvm_driver):
    """Driver for UART protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building UART driver")
        self.seq_item_port = uvm_seq_item_pull_port("uart_driver_seq_item_port", self)
    
    async def run_phase(self):
        """Run phase - implement UART transmission."""
        self.logger.info(f"[{self.get_name()}] Starting UART driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Transmitting UART: {item}")
            
            # UART transmission: Start bit -> Data bits -> Parity -> Stop bit(s)
            # In real code: cocotb.dut.tx.value = 0  # Start bit
            # In real code: await Timer(bit_time, units="ns")
            # In real code: for i in range(8):  # Data bits
            # In real code:     cocotb.dut.tx.value = (item.data >> i) & 1
            # In real code:     await Timer(bit_time, units="ns")
            # In real code: cocotb.dut.tx.value = 1  # Stop bit
            # In real code: await Timer(bit_time, units="ns")
            
            await Timer(100, unit="ns")  # Simulated transmission time
            self.seq_item_port.item_done()


class UARTMonitor(uvm_monitor):
    """Monitor for UART protocol."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building UART monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - monitor UART reception."""
        self.logger.info(f"[{self.get_name()}] Starting UART monitor")
        
        while True:
            # Monitor UART reception
            # In real code: await FallingEdge(cocotb.dut.rx)  # Start bit
            # In real code: await Timer(bit_time / 2, units="ns")  # Sample at middle
            # In real code: data = 0
            # In real code: for i in range(8):  # Data bits
            # In real code:     await Timer(bit_time, units="ns")
            # In real code:     data |= (cocotb.dut.rx.value << i)
            
            await Timer(100, unit="ns")
            
            # Create transaction from received data
            txn = UARTTransaction()
            txn.data = 0xAA  # Simulated
            txn.baud_rate = 9600
            txn.parity = "NONE"
            
            self.logger.info(f"[{self.get_name()}] Received UART: {txn}")
            self.ap.write(txn)


class UARTAgent(uvm_agent):
    """Agent for UART protocol."""
    
    def build_phase(self):
        self.logger.info("Building UART agent")
        self.driver = UARTDriver.create("driver", self)
        self.monitor = UARTMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class UARTSequence(uvm_sequence):
    """Sequence for UART transactions."""
    
    async def body(self):
        """Generate UART transactions."""
        test_data = [0x00, 0x55, 0xAA, 0xFF, 0x12, 0x34, 0x56, 0x78]
        
        for data in test_data:
            txn = UARTTransaction()
            txn.data = data
            txn.baud_rate = 9600
            txn.parity = "NONE"
            txn.stop_bits = 1
            
            await self.start_item(txn)
            await self.finish_item(txn)


class UARTEnv(uvm_env):
    """Environment for UART verification."""
    
    def build_phase(self):
        self.logger.info("Building UARTEnv")
        self.agent = UARTAgent.create("agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting UARTEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class UARTTest(uvm_test):
    """Test demonstrating UART protocol verification."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("UART Protocol Example Test")
        self.logger.info("=" * 60)
        self.env = UARTEnv.create("env", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting UART Test")
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running UART test")
        
        # Start UART sequence
        seq = UARTSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(1000, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("Checking UART test results")
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("UART test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_uart(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["UARTTest"] = UARTTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("UARTTest")


if __name__ == "__main__":
    print("This is a pyuvm UART protocol example.")
    print("To run with cocotb, use the Makefile in the test directory.")

