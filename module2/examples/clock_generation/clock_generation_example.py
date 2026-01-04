"""
Module 2 Example 2.2: Clock Generation and Management
Demonstrates clock generation patterns in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge


async def generate_clock_simple(dut, period_ns=10):
    """
    Simple clock generation function.
    """
    while True:
        dut.clk.value = 1
        await Timer(period_ns // 2, units="ns")
        dut.clk.value = 0
        await Timer(period_ns // 2, units="ns")


@cocotb.test()
async def test_clock_class(dut):
    """
    Demonstrates using Clock class.
    """
    # Create clock with 10ns period
    clock = Clock(dut.clk, 10, units="ns")
    
    # Start clock
    cocotb.start_soon(clock.start())
    
    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.clk)
        print(f"Clock cycle {i+1}")
    
    # Clock continues running in background


@cocotb.test()
async def test_multiple_clocks(dut):
    """
    Demonstrates multiple clock domains.
    Note: This example uses the same clock for demonstration.
    In practice, you'd have multiple clock signals.
    """
    # Create clocks with different periods
    clock_fast = Clock(dut.clk, 5, units="ns")
    clock_slow = Clock(dut.clk, 20, units="ns")
    
    # Start fast clock
    cocotb.start_soon(clock_fast.start())
    
    # Count fast clock cycles
    for i in range(10):
        await RisingEdge(dut.clk)
        if i % 2 == 0:
            print(f"Fast clock cycle {i//2 + 1}")


@cocotb.test()
async def test_clock_gating(dut):
    """
    Demonstrates clock gating pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    clock_enable = True
    
    # Simulate clock gating
    async def gated_clock():
        while True:
            await RisingEdge(dut.clk)
            if not clock_enable:
                print("Clock gated")
                await Timer(50, units="ns")  # Hold for gated period
    
    cocotb.start_soon(gated_clock())
    
    # Enable/disable clock
    await RisingEdge(dut.clk)
    clock_enable = False
    await Timer(30, units="ns")
    clock_enable = True
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_clock_stopping(dut):
    """
    Demonstrates stopping a clock.
    
    In cocotb, Clock objects run as coroutines. To stop a clock, you can:
    1. Use a flag-based approach with a custom clock generator
    2. Use the coroutine handle's kill() method (if supported)
    3. Let the test complete naturally (clock stops when test ends)
    
    This example demonstrates the pattern for controlled clock stopping.
    """
    clock = Clock(dut.clk, 10, units="ns")
    clock_handle = cocotb.start_soon(clock.start())
    
    # Run for a few cycles
    for i in range(5):
        await RisingEdge(dut.clk)
        print(f"Clock cycle {i+1}")
    
    # Note: In cocotb, Clock objects run until the test completes.
    # For explicit clock control, use a custom clock generator with a stop flag:
    # 
    # stop_clock = False
    # async def controlled_clock():
    #     while not stop_clock:
    #         dut.clk.value = 1
    #         await Timer(period_ns // 2, units="ns")
    #         dut.clk.value = 0
    #         await Timer(period_ns // 2, units="ns")
    # 
    # Then set stop_clock = True when you want to stop
    
    print("Clock continues running until test completes")


@cocotb.test()
async def test_clock_division(dut):
    """
    Demonstrates clock division pattern.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    divided_clock = 0
    divide_by = 2
    
    # Create divided clock
    async def clock_divider():
        nonlocal divided_clock
        count = 0
        while True:
            await RisingEdge(dut.clk)
            count += 1
            if count >= divide_by:
                divided_clock = 1 - divided_clock
                count = 0
                print(f"Divided clock: {divided_clock}")
    
    cocotb.start_soon(clock_divider())
    
    # Run for several cycles
    for i in range(10):
        await RisingEdge(dut.clk)

