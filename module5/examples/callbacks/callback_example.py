"""
Module 5 Example 5.4: UVM Callbacks
Demonstrates callback implementation and usage.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer

# Try to import uvm_callback explicitly if available
try:
    import pyuvm
    if hasattr(pyuvm, 'uvm_callback'):
        uvm_callback = pyuvm.uvm_callback
    else:
        # If uvm_callback is not available, use uvm_object as base class
        # This is a workaround for pyuvm versions that don't export uvm_callback
        uvm_callback = uvm_object
except (ImportError, AttributeError):
    # Fallback to uvm_object if anything goes wrong
    uvm_callback = uvm_object

# Explicit imports for TLM classes that may not be in __all__
try:
    # Try to get it from globals first (in case from pyuvm import * worked)
    uvm_seq_item_pull_port  # type: ignore
except NameError:
    # Not in globals, try to import it explicitly
    _found = False
    # Try TLM module paths
    for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
        try:
            tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_seq_item_pull_port'])
            if hasattr(tlm_module, 'uvm_seq_item_pull_port'):
                uvm_seq_item_pull_port = getattr(tlm_module, 'uvm_seq_item_pull_port')  # type: ignore
                _found = True
                break
        except (ImportError, AttributeError):
            continue
    # If still not found, try pyuvm module directly
    if not _found:
        import pyuvm
        if hasattr(pyuvm, 'uvm_seq_item_pull_port'):
            uvm_seq_item_pull_port = getattr(pyuvm, 'uvm_seq_item_pull_port')  # type: ignore
            _found = True
    if not _found:
        # This should not happen if pyuvm is properly installed
        raise ImportError("Could not import uvm_seq_item_pull_port from pyuvm")


class DriverTransaction(uvm_sequence_item):
    """Transaction for callback example."""
    
    def __init__(self, name="DriverTransaction"):
        super().__init__(name)
        self.data = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}"


class DriverCallback(uvm_callback):
    """
    Callback class for driver.
    
    Shows:
    - Callback class definition
    - Callback methods
    - Callback registration
    """
    
    def pre_drive(self, driver, txn):
        """Pre-drive callback."""
        self.logger.info(f"[{self.get_name()}] Pre-drive callback: {txn}")
        # Can modify transaction before driving
        return txn
    
    def post_drive(self, driver, txn):
        """Post-drive callback."""
        self.logger.info(f"[{self.get_name()}] Post-drive callback: {txn}")
        # Can perform actions after driving


class DriverWithCallbacks(uvm_driver):
    """Driver that uses callbacks."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building driver with callbacks")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase with callback execution."""
        self.logger.info(f"[{self.get_name()}] Starting driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            
            # Execute pre-drive callbacks
            self.logger.info(f"[{self.get_name()}] Executing pre-drive callbacks")
            for callback in self.get_callbacks(DriverCallback):
                item = callback.pre_drive(self, item)
            
            # Drive transaction
            self.logger.info(f"[{self.get_name()}] Driving: {item}")
            await Timer(10, units="ns")
            
            # Execute post-drive callbacks
            self.logger.info(f"[{self.get_name()}] Executing post-drive callbacks")
            for callback in self.get_callbacks(DriverCallback):
                callback.post_drive(self, item)
            
            await self.seq_item_port.item_done()


class MonitorCallback(uvm_callback):
    """Callback for monitor."""
    
    def pre_sample(self, monitor, txn):
        """Pre-sample callback."""
        self.logger.info(f"[{self.get_name()}] Pre-sample callback: {txn}")
        return txn
    
    def post_sample(self, monitor, txn):
        """Post-sample callback."""
        self.logger.info(f"[{self.get_name()}] Post-sample callback: {txn}")


class MonitorWithCallbacks(uvm_monitor):
    """Monitor that uses callbacks."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building monitor with callbacks")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase with callback execution."""
        self.logger.info(f"[{self.get_name()}] Starting monitor")
        
        while True:
            # Sample DUT (simulated)
            await Timer(10, units="ns")
            
            txn = DriverTransaction()
            txn.data = 0xAA
            
            # Execute pre-sample callbacks
            for callback in self.get_callbacks(MonitorCallback):
                txn = callback.pre_sample(self, txn)
            
            # Sample transaction
            self.logger.info(f"[{self.get_name()}] Sampled: {txn}")
            
            # Execute post-sample callbacks
            for callback in self.get_callbacks(MonitorCallback):
                callback.post_sample(self, txn)
            
            self.ap.write(txn)


class CallbackAgent(uvm_agent):
    """Agent with callbacks."""
    
    def build_phase(self):
        self.logger.info("Building CallbackAgent")
        self.driver = DriverWithCallbacks.create("driver", self)
        self.monitor = MonitorWithCallbacks.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting CallbackAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
    
    def end_of_elaboration_phase(self):
        """End of elaboration - register callbacks."""
        self.logger.info("Registering callbacks")
        
        # Register driver callbacks
        driver_callback = DriverCallback.create("driver_callback")
        self.driver.add_callback(driver_callback)
        self.logger.info("Registered driver callback")
        
        # Register monitor callbacks
        monitor_callback = MonitorCallback.create("monitor_callback")
        self.monitor.add_callback(monitor_callback)
        self.logger.info("Registered monitor callback")


class CallbackEnv(uvm_env):
    """Environment with callbacks."""
    
    def build_phase(self):
        self.logger.info("Building CallbackEnv")
        self.agent = CallbackAgent.create("agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting CallbackEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class CallbackTest(uvm_test):
    """Test demonstrating callbacks."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Callback Example Test")
        self.logger.info("=" * 60)
        self.env = CallbackEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running callback test")
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Callback test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_callback(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["CallbackTest"] = CallbackTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("CallbackTest")


if __name__ == "__main__":
    print("This is a pyuvm callback example.")
    print("To run with cocotb, use the Makefile in the test directory.")

