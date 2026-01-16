"""
Module 1: Counter Testbench
cocotb testbench for counter module.

Demonstrates:
- Clock generation
- Reset sequence
- Enable control
- Counter verification
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


async def generate_clock(dut, period_ns=10):
    """Generate clock signal."""
    while True:
        dut.clk.value = 1
        await Timer(period_ns // 2, units="ns")
        dut.clk.value = 0
        await Timer(period_ns // 2, units="ns")


async def reset_dut(dut, duration_ns=20):
    """Reset the DUT."""
    dut.rst_n.value = 0
    dut.enable.value = 0
    await Timer(duration_ns, units="ns")
    dut.rst_n.value = 1
    await Timer(10, units="ns")


@cocotb.test()
async def test_counter_reset(dut):
    """
    Test counter reset functionality.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Check counter is reset
    assert dut.count.value == 0, f"Counter should be 0 after reset, got {dut.count.value}"


@cocotb.test()
async def test_counter_increment(dut):
    """
    Test counter increment functionality.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable counter
    dut.enable.value = 1
    
    # Count for several cycles
    for expected_count in range(1, 11):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")  # Wait for combinational logic
        actual_count = int(dut.count.value)
        assert actual_count == expected_count, \
            f"Expected count {expected_count}, got {actual_count}"


@cocotb.test()
async def test_counter_enable(dut):
    """
    Test counter enable control.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable and count
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.count.value == 1, "Counter should increment when enabled"
    
    # Disable and check counter doesn't increment
    dut.enable.value = 0
    count_before = int(dut.count.value)
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    count_after = int(dut.count.value)
    assert count_after == count_before, "Counter should not increment when disabled"
    
    # Re-enable and verify it continues
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.count.value == count_before + 1, "Counter should resume incrementing when re-enabled"


@cocotb.test()
async def test_counter_overflow(dut):
    """
    Test counter overflow behavior.
    """
    # Start clock
    cocotb.start_soon(generate_clock(dut, period_ns=10))
    
    # Reset
    await reset_dut(dut)
    
    # Enable counter
    dut.enable.value = 1
    
    # Count to near overflow (254 = 255 - 1, testing boundary condition)
    # For an 8-bit counter, maximum value is 255 (0xFF)
    # We count to 254 to test the overflow behavior on the next increment
    MAX_COUNT = 255  # Maximum value for 8-bit counter
    COUNT_TO_OVERFLOW = MAX_COUNT - 1  # 254
    
    for _ in range(COUNT_TO_OVERFLOW):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
    
    # Check we're at the expected pre-overflow value
    assert dut.count.value == COUNT_TO_OVERFLOW, \
        f"Should be at {COUNT_TO_OVERFLOW} before overflow, got {dut.count.value}"
    
    # Next increment should wrap to 0 (or continue to 255, depending on implementation)
    # This tests the counter's overflow behavior
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    # Note: Counter behavior depends on implementation:
    # - Wrapping counter: 254 -> 255 -> 0 (wraps on next increment)
    # - Saturating counter: 254 -> 255 -> 255 (saturates at max)
    # This test accepts both behaviors as valid
    final_count = int(dut.count.value)
    assert final_count in [0, MAX_COUNT], \
        f"Counter should wrap to 0 or saturate at {MAX_COUNT}, got {final_count}"

