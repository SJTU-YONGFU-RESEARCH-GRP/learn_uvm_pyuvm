"""
Module 2 Example 2.1: Basic Signal Access
Demonstrates accessing and reading DUT signals in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge


@cocotb.test()
async def test_signal_access_basic(dut):
    """
    Basic signal access example.
    
    Demonstrates:
    - Accessing DUT signals
    - Reading signal values
    - Different signal types
    """
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Initialize signals
    dut.rst_n.value = 0
    dut.enable.value = 0
    dut.d.value = 0
    
    # Wait for initial values
    await Timer(10, units="ns")
    
    # Read initial values
    print(f"Initial q value: {dut.q.value}")
    print(f"Initial q value (integer): {dut.q.value.integer}")
    print(f"Initial q value (binary): {dut.q.value.binstr}")
    
    # Deassert reset
    dut.rst_n.value = 1
    await Timer(10, units="ns")
    
    # Read after reset
    print(f"After reset q value: {dut.q.value.integer}")
    
    # Enable and write data
    dut.enable.value = 1
    dut.d.value = 0xAB
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    
    # Read output
    print(f"After write q value: 0x{dut.q.value.integer:02X}")
    assert dut.q.value.integer == 0xAB, f"Expected 0xAB, got 0x{dut.q.value.integer:02X}"


@cocotb.test()
async def test_signal_types(dut):
    """
    Demonstrates different signal types.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    
    # Test single-bit signal
    print(f"enable signal type: {type(dut.enable.value)}")
    print(f"enable value: {int(dut.enable.value)}")
    
    # Test multi-bit signal
    print(f"d signal width: {len(dut.d)}")
    print(f"q signal width: {len(dut.q)}")
    
    # Test different value assignments
    dut.d.value = 0x12  # Integer
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    print(f"Assigned 0x12, got: 0x{dut.q.value.integer:02X}")
    
    dut.d.value = 0b10101010  # Binary literal
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    print(f"Assigned 0b10101010, got: 0x{dut.q.value.integer:02X}")
    assert dut.q.value.integer == 0xAA


@cocotb.test()
async def test_signal_properties(dut):
    """
    Demonstrates signal properties and methods.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    
    # Test signal properties
    print(f"Signal name: {dut.q._name}")
    print(f"Signal path: {dut.q._path}")
    print(f"Signal width: {len(dut.q)}")
    
    # Test value representations
    dut.d.value = 0x5A
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    
    print(f"Integer: {dut.q.value.integer}")
    print(f"Binary: {dut.q.value.binstr}")
    print(f"Hex: {hex(dut.q.value.integer)}")
    print(f"String: {str(dut.q.value)}")

