"""
Module 2 Example: Common Verification Patterns
Demonstrates common verification patterns in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import random


async def async_reset(dut, duration_ns=50, propagation_delay_ns=10):
    """
    Async reset helper.
    
    Args:
        dut: Device under test
        duration_ns: Reset duration in nanoseconds
        propagation_delay_ns: Delay after deasserting reset to allow
                              signal propagation and DUT stabilization
    """
    dut.rst_n.value = 0
    await Timer(duration_ns, units="ns")
    dut.rst_n.value = 1
    # Wait for reset signal to propagate through DUT logic
    await Timer(propagation_delay_ns, units="ns")


class Scoreboard:
    """Simple scoreboard for verification."""
    
    def __init__(self):
        self.expected = []
        self.actual = []
        self.mismatches = []
    
    def add_expected(self, value):
        """Add expected value."""
        self.expected.append(value)
    
    def add_actual(self, value):
        """Add actual value and check."""
        self.actual.append(value)
        if len(self.expected) > 0:
            expected = self.expected.pop(0)
            if value != expected:
                self.mismatches.append((expected, value))
                return False
        return True
    
    def get_statistics(self):
        """Get scoreboard statistics."""
        return {
            'total': len(self.actual),
            'matches': len(self.actual) - len(self.mismatches),
            'mismatches': len(self.mismatches),
            'mismatch_list': self.mismatches
        }


@cocotb.test()
async def test_sequential_pattern(dut):
    """
    Demonstrates sequential stimulus pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await async_reset(dut)
    dut.enable.value = 1
    
    # Sequential pattern
    test_data = [0x01, 0x02, 0x03, 0x04, 0x05]
    
    for data in test_data:
        dut.d.value = data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        print(f"Wrote 0x{data:02X}, read 0x{dut.q.value.integer:02X}")
        assert dut.q.value.integer == data


@cocotb.test()
async def test_random_pattern(dut):
    """
    Demonstrates random stimulus pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await async_reset(dut)
    dut.enable.value = 1
    
    # Random pattern
    random.seed(42)  # For reproducibility
    
    for i in range(10):
        data = random.randint(0, 255)
        dut.d.value = data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        print(f"Random data 0x{data:02X}, read 0x{dut.q.value.integer:02X}")
        assert dut.q.value.integer == data


@cocotb.test()
async def test_scoreboard_pattern(dut):
    """
    Demonstrates scoreboard pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await async_reset(dut)
    dut.enable.value = 1
    
    scoreboard = Scoreboard()
    
    # Generate expected values
    test_data = [0x10, 0x20, 0x30, 0x40, 0x50]
    for data in test_data:
        scoreboard.add_expected(data)
    
    # Drive and check
    for data in test_data:
        dut.d.value = data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        scoreboard.add_actual(dut.q.value.integer)
    
    # Check statistics
    stats = scoreboard.get_statistics()
    print(f"Scoreboard stats: {stats}")
    assert stats['mismatches'] == 0, "No mismatches expected"


@cocotb.test()
async def test_reference_model(dut):
    """
    Demonstrates reference model pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await async_reset(dut)
    dut.enable.value = 1
    
    # Reference model (simple register)
    # This models the expected behavior of the DUT
    reference_q = 0
    
    # Test data pattern: using 0x11 (17 decimal) as multiplier
    # creates interesting test values: 0x00, 0x11, 0x22, 0x33, 0x44
    # This pattern exercises different bit combinations
    DATA_PATTERN_MULTIPLIER = 0x11
    
    for i in range(5):
        data = i * DATA_PATTERN_MULTIPLIER
        dut.d.value = data
        
        # Update reference model
        reference_q = data
        
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        
        # Compare with reference
        actual_q = dut.q.value.integer
        print(f"Data: 0x{data:02X}, Reference: 0x{reference_q:02X}, Actual: 0x{actual_q:02X}")
        assert actual_q == reference_q, f"Mismatch: expected 0x{reference_q:02X}, got 0x{actual_q:02X}"


@cocotb.test()
async def test_transaction_level(dut):
    """
    Demonstrates transaction-level modeling.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await async_reset(dut)
    
    class RegisterTransaction:
        """Transaction class for register operations."""
        
        def __init__(self, enable, data):
            self.enable = enable
            self.data = data
            self.expected_result = data if enable else None
    
    # Generate transactions
    transactions = [
        RegisterTransaction(enable=1, data=0xAA),
        RegisterTransaction(enable=0, data=0xBB),  # Should not update
        RegisterTransaction(enable=1, data=0xCC),
    ]
    
    # Execute transactions
    for txn in transactions:
        dut.enable.value = txn.enable
        dut.d.value = txn.data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        
        if txn.expected_result is not None:
            assert dut.q.value.integer == txn.expected_result, \
                f"Transaction failed: expected 0x{txn.expected_result:02X}"
            print(f"Transaction passed: data=0x{txn.data:02X}, result=0x{dut.q.value.integer:02X}")

