"""
Module 6 Example: Testbench Architecture Patterns
Demonstrates layered testbench architecture and reusable components.
"""

from pyuvm import *


class ArchitectureTransaction(uvm_sequence_item):
    """Transaction for architecture example."""
    
    def __init__(self, name="ArchitectureTransaction"):
        super().__init__(name)
        self.data = 0
        self.layer = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, layer={self.layer}"


class Layer0Component(uvm_component):
    """Layer 0: Lowest abstraction level."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Layer 0 component")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - Layer 0 processing."""
        self.logger.info(f"[{self.get_name()}] Running Layer 0")
        
        for i in range(3):
            txn = ArchitectureTransaction()
            txn.data = i
            txn.layer = 0
            self.logger.info(f"[{self.get_name()}] Layer 0: {txn}")
            self.ap.write(txn)
            await Timer(10, units="ns")


class Layer1Component(uvm_component):
    """Layer 1: Middle abstraction level."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Layer 1 component")
        self.ap_in = uvm_analysis_export("ap_in", self)
        self.imp_in = uvm_analysis_imp("imp_in", self)
        self.ap_in.connect(self.imp_in)
        self.ap_out = uvm_analysis_port("ap_out", self)
        self.processed = []
    
    def write(self, txn):
        """Write method - process transaction from lower layer."""
        self.logger.info(f"[{self.get_name()}] Layer 1 received: {txn}")
        
        # Process transaction (e.g., add layer 1 processing)
        processed_txn = ArchitectureTransaction()
        processed_txn.data = txn.data + 0x10
        processed_txn.layer = 1
        
        self.processed.append(processed_txn)
        self.ap_out.write(processed_txn)
        self.logger.info(f"[{self.get_name()}] Layer 1 processed: {processed_txn}")
    
    async def run_phase(self):
        """Run phase - Layer 1 processing."""
        self.logger.info(f"[{self.get_name()}] Running Layer 1")
        await Timer(50, units="ns")


class Layer2Component(uvm_component):
    """Layer 2: Highest abstraction level."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Layer 2 component")
        self.ap_in = uvm_analysis_export("ap_in", self)
        self.imp_in = uvm_analysis_imp("imp_in", self)
        self.ap_in.connect(self.imp_in)
        self.received = []
    
    def write(self, txn):
        """Write method - receive from middle layer."""
        self.logger.info(f"[{self.get_name()}] Layer 2 received: {txn}")
        self.received.append(txn)
    
    def check_phase(self):
        """Check phase - verify layered processing."""
        self.logger.info(f"[{self.get_name()}] Layer 2 check: received {len(self.received)} transactions")


class LayeredEnv(uvm_env):
    """
    Layered testbench environment.
    
    Shows:
    - Layered architecture
    - Layer communication
    - Abstraction levels
    """
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Layered Environment")
        self.logger.info("=" * 60)
        
        # Create components for each layer
        self.layer0 = Layer0Component.create("layer0", self)
        self.layer1 = Layer1Component.create("layer1", self)
        self.layer2 = Layer2Component.create("layer2", self)
    
    def connect_phase(self):
        """Connect phase - connect layers."""
        self.logger.info("Connecting Layered Environment")
        # Connect Layer 0 -> Layer 1 -> Layer 2
        self.layer0.ap.connect(self.layer1.ap_in)
        self.layer1.ap_out.connect(self.layer2.ap_in)
        self.logger.info("Layer connections: Layer0 -> Layer1 -> Layer2")


class ReusableComponent(uvm_component):
    """
    Reusable component demonstrating component reuse patterns.
    
    Shows:
    - Component design for reuse
    - Parameterization
    - Component patterns
    """
    
    def __init__(self, name="ReusableComponent", parent=None, config=None):
        super().__init__(name, parent)
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.mode = self.config.get('mode', 'normal')
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building reusable component")
        self.logger.info(f"  Enabled: {self.enabled}, Mode: {self.mode}")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - component operation."""
        if self.enabled:
            self.logger.info(f"[{self.get_name()}] Running in {self.mode} mode")
            await Timer(10, units="ns")
        else:
            self.logger.info(f"[{self.get_name()}] Component disabled")


class ReusableEnv(uvm_env):
    """Environment demonstrating reusable components."""
    
    def build_phase(self):
        self.logger.info("Building Reusable Environment")
        
        # Create multiple instances of reusable component with different configs
        self.comp1 = ReusableComponent.create("comp1", self, config={'enabled': True, 'mode': 'normal'})
        self.comp2 = ReusableComponent.create("comp2", self, config={'enabled': True, 'mode': 'debug'})
        self.comp3 = ReusableComponent.create("comp3", self, config={'enabled': False, 'mode': 'normal'})
    
    def connect_phase(self):
        self.logger.info("Connecting Reusable Environment")


@uvm_test()
class ArchitectureTest(uvm_test):
    """Test demonstrating testbench architecture patterns."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Testbench Architecture Example Test")
        self.logger.info("=" * 60)
        self.env = LayeredEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running architecture test")
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Architecture test completed")
        self.logger.info("=" * 60)


@uvm_test()
class ReusableTest(uvm_test):
    """Test demonstrating reusable components."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Reusable Component Example Test")
        self.logger.info("=" * 60)
        self.env = ReusableEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running reusable component test")
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Reusable component test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm architecture example.")
    print("To run with cocotb, use the Makefile in the test directory.")

