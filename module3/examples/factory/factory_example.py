"""
Module 3 Example: Factory Pattern
Demonstrates UVM factory pattern for object creation and overrides.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


class BaseTransaction(uvm_sequence_item):
    """Base transaction class."""
    
    def __init__(self, name="BaseTransaction"):
        super().__init__(name)
        self.data = 0
    
    def __str__(self):
        return f"{self.get_name()}: data=0x{self.data:02X}"


class ExtendedTransaction(BaseTransaction):
    """Extended transaction class."""
    
    def __init__(self, name="ExtendedTransaction"):
        super().__init__(name)
        self.address = 0
    
    def __str__(self):
        return f"{self.get_name()}: data=0x{self.data:02X}, addr=0x{self.address:04X}"


class BaseDriver(uvm_driver):
    """Base driver class."""
    
    async def run_phase(self):
        self.logger.info(f"[BaseDriver] {self.get_name()}: Running base driver")
        await Timer(10, unit="ns")


class ExtendedDriver(BaseDriver):
    """Extended driver class."""
    
    async def run_phase(self):
        self.logger.info(f"[ExtendedDriver] {self.get_name()}: Running extended driver")
        await Timer(10, unit="ns")


class FactoryAgent(uvm_agent):
    """Agent using factory for component creation."""
    
    def build_phase(self):
        """Build phase - use factory to create components."""
        self.logger.info("Building FactoryAgent")
        
        # Factory creates components
        self.driver = uvm_factory().create_component_by_type(
            BaseDriver, "driver", self
        )
        self.logger.info(f"Created driver: {self.driver.get_type_name()}")
    
    async def run_phase(self):
        """Run phase."""
        self.logger.info("Running FactoryAgent")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class FactoryTest(uvm_test):
    """
    Test demonstrating factory pattern.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("Factory Pattern Example")
        self.logger.info("=" * 60)
        
        # Demonstrate factory registration
        self.logger.info("Factory registration:")
        self.logger.info(f"  BaseTransaction: {BaseTransaction}")
        self.logger.info(f"  ExtendedTransaction: {ExtendedTransaction}")
        self.logger.info(f"  BaseDriver: {BaseDriver}")
        self.logger.info(f"  ExtendedDriver: {ExtendedDriver}")
        
        # Create environment
        self.env = FactoryAgent.create("env", self)
    
    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        
        # Demonstrate factory creation
        self.logger.info("=" * 60)
        self.logger.info("Factory object creation:")
        
        # Create objects using factory
        base_txn = BaseTransaction("base_txn")
        base_txn.data = 0xAA
        self.logger.info(f"Created: {base_txn}")
        
        ext_txn = ExtendedTransaction("ext_txn")
        ext_txn.data = 0xBB
        ext_txn.address = 0x1000
        self.logger.info(f"Created: {ext_txn}")
        
        await Timer(10, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("Factory test completed")
        self.logger.info("=" * 60)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class FactoryOverrideTest(uvm_test):
    """
    Test demonstrating factory overrides.
    """
    
    async def build_phase(self):
        """Build phase - demonstrate factory override."""
        self.logger.info("=" * 60)
        self.logger.info("Factory Override Example")
        self.logger.info("=" * 60)
        
        # Set factory override
        uvm_factory().set_type_override(BaseDriver, ExtendedDriver)
        self.logger.info("Set factory override: BaseDriver -> ExtendedDriver")
        
        # Create environment (should use ExtendedDriver due to override)
        self.env = FactoryAgent.create("env", self)
    
    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        self.logger.info("Running FactoryOverrideTest")
        await Timer(10, unit="ns")
        self.drop_objection()


# Cocotb test functions to run the pyuvm tests
@cocotb.test()
async def test_factory(dut):
    """Cocotb test wrapper for FactoryTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["FactoryTest"] = FactoryTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("FactoryTest")

@cocotb.test()
async def test_factory_override(dut):
    """Cocotb test wrapper for FactoryOverrideTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["FactoryOverrideTest"] = FactoryOverrideTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("FactoryOverrideTest")

if __name__ == "__main__":
    print("This is a pyuvm factory example.")
    print("To run with cocotb, use the Makefile in the test directory.")

