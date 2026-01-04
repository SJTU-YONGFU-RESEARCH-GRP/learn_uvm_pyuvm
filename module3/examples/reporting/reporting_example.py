"""
Module 3 Example 3.3: UVM Reporting System
Demonstrates UVM reporting with different severity and verbosity levels.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class ReportingTest(uvm_test):
    """
    Test demonstrating UVM reporting system.
    
    Shows different severity levels and verbosity control.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("UVM Reporting Example")
        self.logger.info("=" * 60)
    
    async def run_phase(self):
        """Run phase - demonstrate reporting."""
        self.raise_objection()
        
        # Severity levels
        self.logger.info("Demonstrating UVM severity levels:")
        self.logger.info("This is an INFO message")
        self.logger.warning("This is a WARNING message")
        self.logger.error("This is an ERROR message")
        self.logger.fatal("This is a FATAL message (would stop simulation)")
        
        # Message formatting
        self.logger.info("=" * 60)
        self.logger.info("Demonstrating message formatting:")
        
        data = 0xAB
        address = 0x1000
        self.logger.info(f"Formatted message: data=0x{data:02X}, addr=0x{address:04X}")
        
        # Context information
        self.logger.info("=" * 60)
        self.logger.info("Component context:")
        self.logger.info(f"  Component name: {self.get_name()}")
        self.logger.info(f"  Component type: {self.get_type_name()}")
        self.logger.info(f"  Full name: {self.get_full_name()}")
        
        # Verbosity demonstration
        self.logger.info("=" * 60)
        self.logger.info("Verbosity levels (controlled by UVM verbosity setting):")
        self.logger.info("  UVM_LOW: Basic messages")
        self.logger.info("  UVM_MEDIUM: More detailed messages")
        self.logger.info("  UVM_HIGH: Very detailed messages")
        self.logger.info("  UVM_FULL: All messages")
        self.logger.info("  UVM_DEBUG: Debug messages")
        
        await Timer(10, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("Reporting test completed")
        self.logger.info("=" * 60)


class ReportingComponent(uvm_component):
    """
    Component demonstrating reporting in different phases.
    """
    
    def build_phase(self):
        """Build phase reporting."""
        self.logger.info(f"[{self.get_name()}] Building component")
    
    async def run_phase(self):
        """Run phase reporting."""
        self.logger.info(f"[{self.get_name()}] Running component")
        await Timer(10, unit="ns")
    
    def report_phase(self):
        """Report phase reporting."""
        self.logger.info(f"[{self.get_name()}] Component reporting")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class HierarchicalReportingTest(uvm_test):
    """
    Test demonstrating hierarchical reporting.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("Building HierarchicalReportingTest")
        self.comp = ReportingComponent.create("comp", self)
    
    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        self.logger.info("Running HierarchicalReportingTest")
        await Timer(10, unit="ns")
        self.drop_objection()


# Cocotb test functions to run the pyuvm tests
@cocotb.test()
async def test_reporting(dut):
    """Cocotb test wrapper for ReportingTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ReportingTest"] = ReportingTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ReportingTest")

@cocotb.test()
async def test_hierarchical_reporting(dut):
    """Cocotb test wrapper for HierarchicalReportingTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["HierarchicalReportingTest"] = HierarchicalReportingTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("HierarchicalReportingTest")

if __name__ == "__main__":
    print("This is a pyuvm reporting example.")
    print("To run with cocotb, use the Makefile in the test directory.")

