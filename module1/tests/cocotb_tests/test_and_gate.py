"""
Module 1 Test Case 1.3: Simple Verification Test
cocotb testbench for AND gate.

Demonstrates:
- Testbench structure
- Clock generation
- Signal driving
- Basic checking
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge


@cocotb.test()
async def test_and_gate_basic(dut):
    """
    Basic AND gate test.
    
    Tests all input combinations.
    """
    # Initialize inputs
    dut.a.value = 0
    dut.b.value = 0
    
    # Wait for initial values to settle
    await Timer(10, units="ns")
    
    # Test case 1: 0 & 0 = 0
    dut.a.value = 0
    dut.b.value = 0
    await Timer(10, units="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 2: 0 & 1 = 0
    dut.a.value = 0
    dut.b.value = 1
    await Timer(10, units="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 3: 1 & 0 = 0
    dut.a.value = 1
    dut.b.value = 0
    await Timer(10, units="ns")
    assert dut.y.value == 0, f"Expected 0, got {dut.y.value}"
    
    # Test case 4: 1 & 1 = 1
    dut.a.value = 1
    dut.b.value = 1
    await Timer(10, units="ns")
    assert dut.y.value == 1, f"Expected 1, got {dut.y.value}"


@cocotb.test()
async def test_and_gate_truth_table(dut):
    """
    AND gate truth table test.
    
    Tests all combinations systematically.
    """
    test_cases = [
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (1, 1, 1),
    ]
    
    for a_val, b_val, expected_y in test_cases:
        dut.a.value = a_val
        dut.b.value = b_val
        await Timer(10, units="ns")
        
        actual_y = int(dut.y.value)
        assert actual_y == expected_y, \
            f"Input (a={a_val}, b={b_val}): Expected {expected_y}, got {actual_y}"


@cocotb.test()
async def test_and_gate_timing(dut):
    """
    AND gate timing test.
    
    Tests signal propagation timing.
    """
    # Set initial values
    dut.a.value = 0
    dut.b.value = 0
    await Timer(5, units="ns")
    
    # Change both inputs simultaneously
    dut.a.value = 1
    dut.b.value = 1
    await Timer(5, units="ns")
    
    # Output should be stable
    assert dut.y.value == 1, "Output should be 1 after both inputs are 1"
    
    # Change one input
    dut.a.value = 0
    await Timer(5, units="ns")
    assert dut.y.value == 0, "Output should be 0 when one input is 0"

