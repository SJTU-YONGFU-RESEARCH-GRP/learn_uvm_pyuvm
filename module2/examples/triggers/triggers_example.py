"""
Module 2 Example 2.4: Trigger Usage
Demonstrates various triggers in cocotb.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import (
    Timer, RisingEdge, FallingEdge, Edge,
    ReadOnly, ReadWrite, Combine, First, Lock
)
from cocotb.result import SimTimeoutError


@cocotb.test()
async def test_edge_triggers(dut):
    """
    Demonstrates edge triggers.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Rising edge trigger
    print("Waiting for rising edge...")
    await RisingEdge(dut.clk)
    print("Rising edge detected")
    
    # Falling edge trigger
    print("Waiting for falling edge...")
    await FallingEdge(dut.clk)
    print("Falling edge detected")
    
    # Any edge trigger
    print("Waiting for any edge...")
    await Edge(dut.clk)
    print("Edge detected")


@cocotb.test()
async def test_timer_trigger(dut):
    """
    Demonstrates timer triggers.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Wait for specific time
    print("Waiting 50ns...")
    await Timer(50, units="ns")
    print("50ns elapsed")
    
    # Wait for multiple time periods
    for delay in [10, 20, 30]:
        await Timer(delay, units="ns")
        print(f"Waited {delay}ns")


@cocotb.test()
async def test_readonly_trigger(dut):
    """
    Demonstrates ReadOnly trigger (end of time step).
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.enable.value = 1
    dut.d.value = 0xAA
    
    # Drive signal
    await RisingEdge(dut.clk)
    
    # Wait for ReadOnly (end of time step)
    await ReadOnly()
    
    # Now signal should be stable
    print(f"Signal value after ReadOnly: 0x{dut.q.value.integer:02X}")


@cocotb.test()
async def test_combine_trigger(dut):
    """
    Demonstrates combining multiple triggers.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Wait for clock edge AND timer
    print("Waiting for clock edge and timer...")
    await Combine(RisingEdge(dut.clk), Timer(5, units="ns"))
    print("Both conditions met")


@cocotb.test()
async def test_first_trigger(dut):
    """
    Demonstrates First trigger (first to occur).
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    
    # Wait for first of multiple triggers
    print("Waiting for first trigger...")
    try:
        await First(
            RisingEdge(dut.clk),
            Timer(100, units="ns")
        )
        print("Clock edge occurred first")
    except SimTimeoutError:
        print("Timer would occur first")


@cocotb.test()
async def test_timeout_handling(dut):
    """
    Demonstrates timeout handling with triggers.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Wait with timeout
    try:
        await Timer(1000, units="ns")
        print("Operation completed")
    except SimTimeoutError:
        print("Operation timed out")


@cocotb.test()
async def test_parallel_triggers(dut):
    """
    Demonstrates parallel coroutines with triggers.
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    async def monitor_clock():
        for i in range(5):
            await RisingEdge(dut.clk)
            print(f"Monitor: Clock cycle {i+1}")
    
    async def monitor_timer():
        for i in range(3):
            await Timer(20, units="ns")
            print(f"Monitor: Timer {i+1}")
    
    # Run both in parallel
    await cocotb.start_soon(monitor_clock())
    await cocotb.start_soon(monitor_timer())
    
    # Wait for completion
    await Timer(100, units="ns")

