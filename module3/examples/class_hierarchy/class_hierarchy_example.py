"""
Module 3 Example 3.1: UVM Class Hierarchy
Demonstrates UVM base classes and component hierarchy.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


# Example 1: uvm_object - Base for all UVM objects
class MyTransaction(uvm_sequence_item):
    """
    Transaction class inheriting from uvm_sequence_item.
    
    Demonstrates uvm_object hierarchy.
    """
    
    def __init__(self, name="MyTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"{self.get_name()}: data=0x{self.data:02X}, addr=0x{self.address:04X}"


# Example 2: uvm_component - Base for all UVM components
class MyDriver(uvm_driver):
    """
    Driver class inheriting from uvm_driver.
    
    Demonstrates uvm_component hierarchy.
    """
    
    def build_phase(self):
        """Build phase - component construction."""
        self.logger.info("Building MyDriver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    def connect_phase(self):
        """Connect phase - component connections."""
        self.logger.info("Connecting MyDriver")
    
    async def run_phase(self):
        """Run phase - main execution."""
        self.logger.info("Running MyDriver")
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving transaction: {item}")
            await self.seq_item_port.item_done()


class MyMonitor(uvm_monitor):
    """
    Monitor class inheriting from uvm_monitor.
    
    Demonstrates uvm_component hierarchy.
    """
    
    def build_phase(self):
        """Build phase."""
        self.logger.info("Building MyMonitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase."""
        self.logger.info("Running MyMonitor")
        # Monitor would sample DUT signals here
        await Timer(100, unit="ns")


class MyAgent(uvm_agent):
    """
    Agent class containing driver and monitor.
    
    Demonstrates component composition.
    """
    
    def build_phase(self):
        """Build phase - create sub-components."""
        self.logger.info("Building MyAgent")
        self.driver = MyDriver.create("driver", self)
        self.monitor = MyMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        """Connect phase - connect components."""
        self.logger.info("Connecting MyAgent")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class MyEnv(uvm_env):
    """
    Environment class containing agents.
    
    Demonstrates environment structure.
    """
    
    def build_phase(self):
        """Build phase."""
        self.logger.info("Building MyEnv")
        self.agent = MyAgent.create("agent", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting MyEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class ClassHierarchyTest(uvm_test):
    """
    Test class demonstrating UVM class hierarchy.
    
    Demonstrates:
    - uvm_test as top-level
    - Component hierarchy
    - Phase implementation
    """
    
    async def build_phase(self):
        """Build phase - create environment."""
        self.logger.info("=" * 60)
        self.logger.info("Building ClassHierarchyTest")
        self.logger.info("=" * 60)
        self.env = MyEnv.create("env", self)
    
    async def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting ClassHierarchyTest")
    
    async def run_phase(self):
        """Run phase - main test execution."""
        self.raise_objection()
        self.logger.info("Running ClassHierarchyTest")
        
        # Demonstrate object creation
        txn = MyTransaction("test_txn")
        txn.data = 0xAB
        txn.address = 0x1000
        self.logger.info(f"Created transaction: {txn}")
        
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase - verify results."""
        self.logger.info("Checking ClassHierarchyTest results")
    
    def report_phase(self):
        """Report phase - generate reports."""
        self.logger.info("=" * 60)
        self.logger.info("ClassHierarchyTest completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_class_hierarchy(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ClassHierarchyTest"] = ClassHierarchyTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ClassHierarchyTest")

if __name__ == "__main__":
    # Note: This is a structural example
    # In practice, you would use cocotb to run this with a simulator
    print("This is a pyuvm class hierarchy example.")
    print("To run with cocotb, use the Makefile in the test directory.")

