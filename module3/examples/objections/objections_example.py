"""
Module 3 Example: Objection Mechanism
Demonstrates UVM objection mechanism for test control.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


class ObjectionComponent(uvm_component):
    """
    Component demonstrating objection usage.
    """
    
    async def run_phase(self):
        """Run phase with objections."""
        self.raise_objection()
        self.logger.info(f"[{self.get_name()}] Raised objection")
        
        # Simulate work
        await Timer(50, unit="ns")
        self.logger.info(f"[{self.get_name()}] Work completed")
        
        self.drop_objection()
        self.logger.info(f"[{self.get_name()}] Dropped objection")


class MultipleObjectionsComponent(uvm_component):
    """
    Component with multiple objections.
    """
    
    async def run_phase(self):
        """Run phase with multiple objections."""
        # Raise multiple objections
        self.raise_objection()
        self.raise_objection()
        self.logger.info(f"[{self.get_name()}] Raised 2 objections")
        
        await Timer(30, unit="ns")
        
        # Drop one objection
        self.drop_objection()
        self.logger.info(f"[{self.get_name()}] Dropped 1 objection, 1 remaining")
        
        await Timer(20, unit="ns")
        
        # Drop remaining objection
        self.drop_objection()
        self.logger.info(f"[{self.get_name()}] Dropped all objections")


class ObjectionEnv(uvm_env):
    """Environment with objection components."""
    
    def build_phase(self):
        self.logger.info("Building ObjectionEnv")
        self.comp1 = ObjectionComponent.create("comp1", self)
        self.comp2 = ObjectionComponent.create("comp2", self)
        self.comp3 = MultipleObjectionsComponent.create("comp3", self)
    
    async def run_phase(self):
        """Environment can also raise objections."""
        self.raise_objection()
        self.logger.info("[ObjectionEnv] Raised objection")
        await Timer(100, unit="ns")
        self.drop_objection()
        self.logger.info("[ObjectionEnv] Dropped objection")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class ObjectionTest(uvm_test):
    """
    Test demonstrating objection mechanism.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("Objection Mechanism Example")
        self.logger.info("=" * 60)
        self.env = ObjectionEnv.create("env", self)
    
    async def run_phase(self):
        """Run phase - main test with objections."""
        # Test raises objection to keep simulation running
        self.raise_objection()
        self.logger.info("[Test] Raised objection - simulation will run")
        
        # Components will raise/drop their own objections
        # Simulation continues until all objections are dropped
        await Timer(200, unit="ns")
        
        self.logger.info("[Test] Dropping objection - simulation will end")
        self.drop_objection()
    
    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("Objection test completed")
        self.logger.info("=" * 60)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class ObjectionTimingTest(uvm_test):
    """
    Test demonstrating objection timing.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("Objection Timing Example")
        self.logger.info("=" * 60)
        self.env = ObjectionEnv.create("env", self)
    
    async def run_phase(self):
        """Run phase - demonstrate objection timing."""
        self.raise_objection()
        
        self.logger.info("Test started - objection raised")
        
        # Wait for components to complete
        await Timer(150, unit="ns")
        
        self.logger.info("All components should have dropped objections")
        self.logger.info("Dropping test objection - simulation will end")
        self.drop_objection()


# Cocotb test functions to run the pyuvm tests
@cocotb.test()
async def test_objection(dut):
    """Cocotb test wrapper for ObjectionTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ObjectionTest"] = ObjectionTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ObjectionTest")

@cocotb.test()
async def test_objection_timing(dut):
    """Cocotb test wrapper for ObjectionTimingTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ObjectionTimingTest"] = ObjectionTimingTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ObjectionTimingTest")

if __name__ == "__main__":
    print("This is a pyuvm objection example.")
    print("To run with cocotb, use the Makefile in the test directory.")

