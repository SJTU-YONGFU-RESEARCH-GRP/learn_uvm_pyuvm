"""
Module 3 Example 3.2: UVM Phases
Demonstrates UVM phase implementation and execution order.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


class PhasesComponent(uvm_component):
    """
    Component demonstrating all UVM phases.
    """
    
    def build_phase(self):
        """Build phase - component construction."""
        self.logger.info(f"[BUILD] {self.get_name()}: Building component")
        self.counter = 0
    
    def connect_phase(self):
        """Connect phase - component connections."""
        self.logger.info(f"[CONNECT] {self.get_name()}: Connecting component")
    
    def end_of_elaboration_phase(self):
        """End of elaboration phase - final setup."""
        self.logger.info(f"[END_OF_ELAB] {self.get_name()}: Elaboration complete")
    
    async def pre_reset_phase(self):
        """Pre-reset phase - before reset."""
        self.logger.info(f"[PRE_RESET] {self.get_name()}: Pre-reset phase")
        await Timer(10, unit="ns")
    
    async def reset_phase(self):
        """Reset phase - reset sequence."""
        self.logger.info(f"[RESET] {self.get_name()}: Reset phase")
        await Timer(20, unit="ns")
    
    async def post_reset_phase(self):
        """Post-reset phase - after reset."""
        self.logger.info(f"[POST_RESET] {self.get_name()}: Post-reset phase")
        await Timer(10, unit="ns")
    
    async def pre_configure_phase(self):
        """Pre-configure phase - before configuration."""
        self.logger.info(f"[PRE_CONFIGURE] {self.get_name()}: Pre-configure phase")
        await Timer(10, unit="ns")
    
    async def configure_phase(self):
        """Configure phase - configuration."""
        self.logger.info(f"[CONFIGURE] {self.get_name()}: Configure phase")
        await Timer(10, unit="ns")
    
    async def post_configure_phase(self):
        """Post-configure phase - after configuration."""
        self.logger.info(f"[POST_CONFIGURE] {self.get_name()}: Post-configure phase")
        await Timer(10, unit="ns")
    
    async def pre_main_phase(self):
        """Pre-main phase - before main test."""
        self.logger.info(f"[PRE_MAIN] {self.get_name()}: Pre-main phase")
        await Timer(10, unit="ns")
    
    async def main_phase(self):
        """Main phase - main test execution."""
        self.logger.info(f"[MAIN] {self.get_name()}: Main phase")
        await Timer(50, unit="ns")
    
    async def post_main_phase(self):
        """Post-main phase - after main test."""
        self.logger.info(f"[POST_MAIN] {self.get_name()}: Post-main phase")
        await Timer(10, unit="ns")
    
    async def pre_shutdown_phase(self):
        """Pre-shutdown phase - before shutdown."""
        self.logger.info(f"[PRE_SHUTDOWN] {self.get_name()}: Pre-shutdown phase")
        await Timer(10, unit="ns")
    
    async def shutdown_phase(self):
        """Shutdown phase - shutdown sequence."""
        self.logger.info(f"[SHUTDOWN] {self.get_name()}: Shutdown phase")
        await Timer(10, unit="ns")
    
    async def post_shutdown_phase(self):
        """Post-shutdown phase - after shutdown."""
        self.logger.info(f"[POST_SHUTDOWN] {self.get_name()}: Post-shutdown phase")
        await Timer(10, unit="ns")
    
    def extract_phase(self):
        """Extract phase - extract results."""
        self.logger.info(f"[EXTRACT] {self.get_name()}: Extracting results")
    
    def check_phase(self):
        """Check phase - final checks."""
        self.logger.info(f"[CHECK] {self.get_name()}: Checking results")
    
    def report_phase(self):
        """Report phase - generate reports."""
        self.logger.info(f"[REPORT] {self.get_name()}: Generating report")
    
    def final_phase(self):
        """Final phase - final cleanup."""
        self.logger.info(f"[FINAL] {self.get_name()}: Final cleanup")


class PhasesEnv(uvm_env):
    """Environment with phase demonstration."""
    
    def build_phase(self):
        self.logger.info("[BUILD] Building PhasesEnv")
        self.comp = PhasesComponent.create("comp", self)
    
    def connect_phase(self):
        self.logger.info("[CONNECT] Connecting PhasesEnv")
    
    def end_of_elaboration_phase(self):
        self.logger.info("[END_OF_ELAB] PhasesEnv elaboration complete")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class PhasesTest(uvm_test):
    """
    Test demonstrating all UVM phases.
    
    Shows phase execution order and implementation.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("PHASES TEST - Build Phase")
        self.logger.info("=" * 60)
        self.env = PhasesEnv.create("env", self)
    
    async def connect_phase(self):
        """Connect phase."""
        self.logger.info("PHASES TEST - Connect Phase")
    
    async def run_phase(self):
        """Run phase - main execution."""
        self.raise_objection()
        self.logger.info("PHASES TEST - Run Phase (all run phases execute here)")
        await Timer(200, unit="ns")
        self.drop_objection()
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("PHASES TEST - Check Phase")
    
    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("PHASES TEST - Report Phase")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_phases(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["PhasesTest"] = PhasesTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("PhasesTest")

if __name__ == "__main__":
    print("This is a pyuvm phases example.")
    print("To run with cocotb, use the Makefile in the test directory.")

