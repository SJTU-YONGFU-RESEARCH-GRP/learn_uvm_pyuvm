"""
Module 2 Test: Simple Register
Comprehensive testbench for simple_register module.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


async def reset_dut(dut, duration_ns=50, propagation_delay_ns=10):
    """
    Reset the DUT.
    
    Args:
        dut: Device under test
        duration_ns: Reset duration in nanoseconds
        propagation_delay_ns: Delay after deasserting reset to allow
                              signal propagation and DUT stabilization
    """
    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.d.value = 0
    await Timer(duration_ns, units="ns")
    dut.rst_n.value = 1
    # Wait for reset signal to propagate through DUT logic
    await Timer(propagation_delay_ns, units="ns")


@cocotb.test()
async def test_register_reset(dut):
    """Test register reset functionality."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    # Verify reset state
    assert dut.q.value.integer == 0, "Register should be reset to 0"


@cocotb.test()
async def test_register_write(dut):
    """Test register write functionality."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    # Enable and write
    dut.enable.value = 1
    dut.d.value = 0xAB
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    
    assert dut.q.value.integer == 0xAB, "Register should store written value"


@cocotb.test()
async def test_register_enable(dut):
    """Test register enable control."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    # Write with enable
    dut.enable.value = 1
    dut.d.value = 0x12
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value.integer == 0x12
    
    # Try to write with enable off
    dut.enable.value = 0
    dut.d.value = 0x34
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value.integer == 0x12, "Register should not update when enable is off"


@cocotb.test()
async def test_register_all_values(dut):
    """Test register with all possible 8-bit values."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    dut.enable.value = 1
    
    # Test boundary values
    test_values = [0x00, 0x01, 0x7F, 0x80, 0xFE, 0xFF]
    
    for value in test_values:
        dut.d.value = value
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.q.value.integer == value, \
            f"Failed for value 0x{value:02X}, got 0x{dut.q.value.integer:02X}"

