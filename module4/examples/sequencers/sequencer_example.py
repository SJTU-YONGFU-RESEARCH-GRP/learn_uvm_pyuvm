"""
Module 4 Example 4.3: UVM Sequencer and Sequences
Demonstrates sequencer usage and sequence implementation.
"""

from pyuvm import *
# Ensure uvm_seq_item_pull_port is available in module namespace
# Try explicit import if not already available
try:
    uvm_seq_item_pull_port  # type: ignore
except NameError:
    try:
        from pyuvm.s15_uvm_tlm_1 import uvm_seq_item_pull_port
    except (ImportError, AttributeError):
        try:
            from pyuvm.s15_uvm_tlm import uvm_seq_item_pull_port
        except (ImportError, AttributeError):
            try:
                import pyuvm.s15_uvm_tlm_1 as tlm1
                uvm_seq_item_pull_port = tlm1.uvm_seq_item_pull_port
            except (ImportError, AttributeError):
                # Last resort: try other TLM modules
                for module_name in ['s16_uvm_tlm_1', 's16_uvm_tlm']:
                    try:
                        tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_seq_item_pull_port'])
                        if hasattr(tlm_module, 'uvm_seq_item_pull_port'):
                            uvm_seq_item_pull_port = getattr(tlm_module, 'uvm_seq_item_pull_port')
                            break
                    except (ImportError, AttributeError):
                        continue

import cocotb
from cocotb.triggers import Timer
import random


class DataTransaction(uvm_sequence_item):
    """Transaction for sequencer example."""
    
    def __init__(self, name="DataTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class SimpleSequence(uvm_sequence):
    """
    Simple sequence demonstrating basic sequence implementation.
    
    Shows:
    - Sequence class structure
    - body() method implementation
    - Transaction creation
    - Sequence execution
    """
    
    async def body(self):
        """Body method - sequence execution."""
        # Ensure logger exists (sequences may not have logger until started)
        if not hasattr(self, 'logger'):
            import logging
            self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
        self.logger.info(f"[{self.get_name()}] Starting sequence body")
        
        # Create and send transactions
        for i in range(5):
            txn = DataTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            
            self.logger.info(f"[{self.get_name()}] Creating transaction {i}: {txn}")
            
            # Start item (request from sequencer)
            await self.start_item(txn)
            self.logger.info(f"[{self.get_name()}] Started item: {txn}")
            
            # Finish item (send to driver)
            await self.finish_item(txn)
            self.logger.info(f"[{self.get_name()}] Finished item: {txn}")
        
        self.logger.info(f"[{self.get_name()}] Sequence body completed")


class RandomSequence(uvm_sequence):
    """
    Sequence demonstrating random transaction generation.
    
    Shows:
    - Random transaction creation
    - Constrained random generation
    - Sequence reuse
    """
    
    def __init__(self, name="RandomSequence", num_items=10):
        super().__init__(name)
        self.num_items = num_items
    
    async def body(self):
        """Body method with random transactions."""
        # Ensure logger exists (sequences may not have logger until started)
        if not hasattr(self, 'logger'):
            import logging
            self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
        self.logger.info(f"[{self.get_name()}] Starting random sequence ({self.num_items} items)")
        
        for i in range(self.num_items):
            txn = DataTransaction()
            # Random data generation
            txn.data = random.randint(0, 255)
            txn.address = random.randint(0, 0xFFFF)
            
            await self.start_item(txn)
            await self.finish_item(txn)
            
            self.logger.info(f"[{self.get_name()}] Generated random transaction {i}: {txn}")


class LayeredSequence(uvm_sequence):
    """
    Sequence demonstrating sequence layering.
    
    Shows:
    - Calling other sequences
    - Sequence composition
    - Hierarchical sequences
    """
    
    async def body(self):
        """Body method with sequence layering."""
        # Ensure logger exists (sequences may not have logger until started)
        if not hasattr(self, 'logger'):
            import logging
            self.logger = logging.getLogger(f"{self.__class__.__name__}.{self.get_name()}")
        self.logger.info(f"[{self.get_name()}] Starting layered sequence")
        
        # Start simple sequence
        simple_seq = SimpleSequence.create("simple_seq")
        await simple_seq.start(self.sequencer)
        self.logger.info(f"[{self.get_name()}] Completed simple sequence")
        
        # Start random sequence
        random_seq = RandomSequence.create("random_seq", num_items=3)
        await random_seq.start(self.sequencer)
        self.logger.info(f"[{self.get_name()}] Completed random sequence")


class SequencerDriver(uvm_driver):
    """Simple driver for sequencer test."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase - consume transactions from sequencer."""
        while True:
            txn = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")
            # Simulate processing
            await Timer(1, unit="ns")
            await self.seq_item_port.item_done()


class SequencerAgent(uvm_agent):
    """Agent with sequencer and driver."""
    
    def build_phase(self):
        self.logger.info("Building SequencerAgent")
        self.seqr = uvm_sequencer("sequencer", self)
        self.driver = SequencerDriver.create("driver", self)
    
    def connect_phase(self):
        self.logger.info("Connecting SequencerAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class SequencerTest(uvm_test):
    """Test demonstrating sequencer and sequence usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Sequencer Example Test")
        self.logger.info("=" * 60)
        self.env = SequencerAgent.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running sequencer test")
        
        # Start simple sequence
        self.logger.info("=" * 60)
        self.logger.info("Starting SimpleSequence")
        seq1 = SimpleSequence.create("seq1")
        await seq1.start(self.env.seqr)
        
        # Start random sequence
        self.logger.info("=" * 60)
        self.logger.info("Starting RandomSequence")
        seq2 = RandomSequence.create("seq2", num_items=5)
        await seq2.start(self.env.seqr)
        
        # Start layered sequence
        self.logger.info("=" * 60)
        self.logger.info("Starting LayeredSequence")
        seq3 = LayeredSequence.create("seq3")
        await seq3.start(self.env.seqr)
        
        await Timer(10, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Sequencer test completed")
        self.logger.info("=" * 60)


# Helper function to recursively call build_phase on all children
async def build_all_children(comp):
    """Recursively call build_phase on component and all its children."""
    import inspect
    # Call build_phase on this component if it hasn't been called
    if hasattr(comp, 'build_phase'):
        if inspect.iscoroutinefunction(comp.build_phase):
            await comp.build_phase()
        else:
            comp.build_phase()
    
    # Get all children and call build_phase on them
    # Try different ways to access children
    children = []
    if hasattr(comp, '_children'):
        children = list(comp._children.values())
    elif hasattr(comp, 'get_children'):
        children = comp.get_children()
    else:
        # Try to find child components by checking attributes
        for attr_name in dir(comp):
            if not attr_name.startswith('_'):
                attr = getattr(comp, attr_name, None)
                if attr is not None and isinstance(attr, uvm_component):
                    children.append(attr)
    
    for child in children:
        await build_all_children(child)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_sequencer(dut):
    """Cocotb test wrapper for pyuvm sequencer test."""
    import inspect
    test = SequencerTest.create("test")
    await test.build_phase()
    # Recursively build all children
    if hasattr(test, 'env') and test.env:
        await build_all_children(test.env)
    if hasattr(test, 'connect_phase') and inspect.iscoroutinefunction(test.connect_phase):
        await test.connect_phase()
    # Ensure env's connect_phase is called
    if hasattr(test, 'env') and test.env and hasattr(test.env, 'connect_phase'):
        if inspect.iscoroutinefunction(test.env.connect_phase):
            await test.env.connect_phase()
        else:
            test.env.connect_phase()
    await test.run_phase()
    if hasattr(test, 'check_phase'):
        test.check_phase()
    test.report_phase()


if __name__ == "__main__":
    print("This is a pyuvm sequencer example.")
    print("To run with cocotb, use the Makefile in the test directory.")

