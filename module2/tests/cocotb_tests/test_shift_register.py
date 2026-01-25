"""
Module 2 Test: Shift Register
Testbench for shift_register module.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge


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
    dut.shift.value = 0
    dut.data_in.value = 0
    await Timer(duration_ns, units="ns")
    dut.rst_n.value = 1
    # Wait for reset signal to propagate through DUT logic
    await Timer(propagation_delay_ns, units="ns")


@cocotb.test()
async def test_shift_register_reset(dut):
    """Test shift register reset."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    assert dut.q.value.integer == 0, "Shift register should be reset"
    assert int(dut.data_out.value) == 0, "Data out should be reset"


@cocotb.test()
async def test_shift_register_operation(dut):
    """Test shift register shift operation."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    dut.shift.value = 1
    
    # Shift in data
    # Test data: MSB first (first bit becomes MSB after all shifts)
    test_data = [1, 0, 1, 1, 0, 1, 0, 0]
    
    for bit in test_data:
        dut.data_in.value = bit
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
    
    # Calculate expected value from test data
    # First bit shifted in becomes MSB, last bit becomes LSB
    # So we need to reverse the order for calculation
    expected = 0
    for i, bit in enumerate(test_data):
        expected |= (bit << (7 - i))  # MSB first: bit 0 goes to position 7
    
    # Alternative calculation: build binary string and convert
    # expected = int(''.join(str(b) for b in test_data), 2)
    
    assert dut.q.value.integer == expected, \
        f"Expected 0b{expected:08b} (from test_data {test_data}), " \
        f"got 0b{dut.q.value.integer:08b}"


@cocotb.test()
async def test_shift_register_serial_out(dut):
    """Test shift register serial output."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_dut(dut)
    
    # Load data
    dut.shift.value = 1
    for i in range(8):
        dut.data_in.value = (i % 2)
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
    
    # Shift out
    expected_bits = []
    for i in range(8):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        expected_bits.append(int(dut.data_out.value))
    
    print(f"Serial output: {expected_bits}")

