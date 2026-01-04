"""
Module 4 Example 4.5: Scoreboard Implementation
Demonstrates scoreboard implementation with analysis port connections.
"""

from pyuvm import *
# Explicitly import uvm_analysis_imp - it may not be exported by from pyuvm import *
# Try multiple possible import paths
_uvm_analysis_imp = None
try:
    # First try: check if it's in the namespace after from pyuvm import *
    _uvm_analysis_imp = globals()['uvm_analysis_imp']
except KeyError:
    # Second try: import from pyuvm module directly
    import pyuvm
    if hasattr(pyuvm, 'uvm_analysis_imp'):
        _uvm_analysis_imp = pyuvm.uvm_analysis_imp
    else:
        # Third try: try TLM module paths
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_analysis_imp'])
                if hasattr(tlm_module, 'uvm_analysis_imp'):
                    _uvm_analysis_imp = tlm_module.uvm_analysis_imp
                    break
            except (ImportError, AttributeError):
                continue

if _uvm_analysis_imp is not None:
    globals()['uvm_analysis_imp'] = _uvm_analysis_imp

import cocotb
from cocotb.triggers import Timer


class ScoreboardTransaction(uvm_sequence_item):
    """Transaction for scoreboard."""
    
    def __init__(self, name="ScoreboardTransaction"):
        super().__init__(name)
        self.data = 0
        self.expected = 0
        self.actual = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, expected=0x{self.expected:02X}, actual=0x{self.actual:02X}"


class SimpleScoreboard(uvm_subscriber):
    """
    Simple scoreboard demonstrating basic scoreboard implementation.
    
    Shows:
    - Scoreboard class structure
    - Analysis port connections
    - Transaction storage
    - Comparison logic
    """
    
    def build_phase(self):
        """Build phase - analysis export provided by uvm_subscriber."""
        self.logger.info(f"[{self.get_name()}] Building scoreboard")
        self.expected = []
        self.actual = []
        self.mismatches = []
    
    def write(self, txn):
        """Write method - receive transactions from analysis port."""
        self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")
        self.actual.append(txn)
        
        # Compare with expected
        if len(self.expected) > 0:
            expected_txn = self.expected.pop(0)
            if txn.actual != expected_txn.expected:
                self.mismatches.append((expected_txn, txn))
                self.logger.error(f"[{self.get_name()}] Mismatch: expected=0x{expected_txn.expected:02X}, "
                                f"actual=0x{txn.actual:02X}")
            else:
                self.logger.info(f"[{self.get_name()}] Match: expected=0x{expected_txn.expected:02X}, "
                               f"actual=0x{txn.actual:02X}")
    
    def add_expected(self, txn):
        """Add expected transaction."""
        self.expected.append(txn)
        self.logger.info(f"[{self.get_name()}] Added expected: {txn}")
    
    def check_phase(self):
        """Check phase - verify results."""
        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Scoreboard Check")
        self.logger.info(f"  Total expected: {len(self.expected)}")
        self.logger.info(f"  Total actual: {len(self.actual)}")
        self.logger.info(f"  Mismatches: {len(self.mismatches)}")
        
        if len(self.mismatches) == 0:
            self.logger.info(f"  ✓ All transactions matched")
        else:
            self.logger.error(f"  ✗ Found {len(self.mismatches)} mismatches")
            for exp, act in self.mismatches:
                self.logger.error(f"    Expected: {exp}, Actual: {act}")


class ReferenceModelScoreboard(uvm_subscriber):
    """
    Scoreboard with reference model.
    
    Shows:
    - Reference model implementation
    - Expected value calculation
    - Comparison with reference
    """
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building reference model scoreboard")
        self.actual = []
    
    def write(self, txn):
        """Write method - compare with reference model."""
        self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")
        self.actual.append(txn)
        
        # Calculate expected using reference model
        expected = self.reference_model(txn.data)
        
        if txn.actual != expected:
            self.logger.error(f"[{self.get_name()}] Mismatch: data=0x{txn.data:02X}, "
                            f"expected=0x{expected:02X}, actual=0x{txn.actual:02X}")
        else:
            self.logger.info(f"[{self.get_name()}] Match: data=0x{txn.data:02X}, "
                           f"expected=0x{expected:02X}, actual=0x{txn.actual:02X}")
    
    def reference_model(self, data):
        """Reference model - calculate expected output."""
        # Simple reference model: double the input
        return (data * 2) & 0xFF
    
    def check_phase(self):
        """Check phase."""
        self.logger.info(f"[{self.get_name()}] Reference model scoreboard check completed")


class ScoreboardEnv(uvm_env):
    """Environment with scoreboard."""
    
    def build_phase(self):
        self.logger.info("Building ScoreboardEnv")
        self.scoreboard = SimpleScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting ScoreboardEnv")


class ScoreboardTest(uvm_test):
    """Test demonstrating scoreboard usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Scoreboard Example Test")
        self.logger.info("=" * 60)
        self.env = ScoreboardEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running scoreboard test")
        
        # Add expected transactions
        for i in range(5):
            txn = ScoreboardTransaction()
            txn.data = i * 0x10
            txn.expected = i * 0x10
            self.env.scoreboard.add_expected(txn)
        
        # Send actual transactions (some matching, some not)
        for i in range(5):
            txn = ScoreboardTransaction()
            txn.data = i * 0x10
            if i == 2:  # Introduce mismatch
                txn.actual = 0xFF
            else:
                txn.actual = i * 0x10
            self.env.scoreboard.write(txn)
        
        await Timer(10, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Scoreboard test completed")
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
async def test_scoreboard(dut):
    """Cocotb test wrapper for pyuvm scoreboard test."""
    import inspect
    test = ScoreboardTest.create("test")
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
    print("This is a pyuvm scoreboard example.")
    print("To run with cocotb, use the Makefile in the test directory.")

