"""
Module 1 Example 1.3: Async/Await for Simulation
Demonstrates async/await patterns for verification and simulation.
"""

import asyncio
from typing import List, Coroutine
import time

# Simulation time scaling factor
# In real hardware simulation with cocotb, you would use cocotb.triggers.Timer
# which handles actual simulation time. This factor is only for demonstration
# purposes to make the async examples runnable without a simulator.
# 
# For demonstration: 1 nanosecond = 0.000001 seconds (1 microsecond)
# This makes simulation delays visible but fast enough for examples.
SIM_TIME_SCALE_FACTOR: float = 0.000001  # nanoseconds to seconds conversion


async def wait_ns(nanoseconds: int) -> None:
    """
    Wait for a specified number of nanoseconds (simulated).
    
    This is a demonstration function. In real cocotb testbenches, you would use:
    ```python
    from cocotb.triggers import Timer
    await Timer(nanoseconds, units="ns")
    ```
    
    Args:
        nanoseconds: Number of nanoseconds to wait (simulated)
    """
    # Convert nanoseconds to seconds using the simulation time scale factor
    # In real cocotb, Timer handles this automatically
    await asyncio.sleep(nanoseconds * SIM_TIME_SCALE_FACTOR)


async def clock_generator(period_ns: int, num_cycles: int) -> List[int]:
    """
    Generate clock signal.
    
    Args:
        period_ns: Clock period in nanoseconds
        num_cycles: Number of clock cycles to generate
        
    Returns:
        List of clock values
    """
    clock_values = []
    for i in range(num_cycles):
        clock_values.append(1)  # High
        await wait_ns(period_ns // 2)
        clock_values.append(0)  # Low
        await wait_ns(period_ns // 2)
    return clock_values


async def reset_sequence(reset_signal: List[bool], duration_ns: int) -> None:
    """
    Generate reset sequence.
    
    Args:
        reset_signal: Reset signal to control
        duration_ns: Reset duration in nanoseconds
    """
    reset_signal[0] = True  # Assert reset
    await wait_ns(duration_ns)
    reset_signal[0] = False  # Deassert reset
    await wait_ns(10)  # Wait a bit after reset


async def stimulus_generator(data_queue: asyncio.Queue, num_items: int) -> None:
    """
    Generate stimulus data.
    
    Args:
        data_queue: Queue to put data into
        num_items: Number of data items to generate
    """
    for i in range(num_items):
        data = i * 2
        await data_queue.put(data)
        await wait_ns(10)
    await data_queue.put(None)  # Sentinel to signal completion


async def monitor(data_queue: asyncio.Queue, results: List[int]) -> None:
    """
    Monitor data from queue.
    
    Args:
        data_queue: Queue to read data from
        results: List to store results
    """
    while True:
        data = await data_queue.get()
        if data is None:
            break
        results.append(data)
        await wait_ns(5)


async def parallel_tasks_example() -> None:
    """Demonstrate parallel coroutine execution."""
    print("Running parallel tasks example...")
    
    # Create queues and shared data
    data_queue: asyncio.Queue = asyncio.Queue()
    results: List[int] = []
    reset_signal = [False]
    
    # Run multiple coroutines in parallel
    await asyncio.gather(
        clock_generator(period_ns=10, num_cycles=5),
        reset_sequence(reset_signal, duration_ns=20),
        stimulus_generator(data_queue, num_items=5),
        monitor(data_queue, results)
    )
    
    print(f"Results collected: {results}")


async def timeout_example() -> None:
    """Demonstrate timeout handling."""
    print("Running timeout example...")
    
    async def slow_operation() -> str:
        """Simulate a slow operation."""
        await wait_ns(1000)
        return "Operation completed"
    
    try:
        # Wait with timeout
        result = await asyncio.wait_for(slow_operation(), timeout=0.001)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")


async def exception_handling_example() -> None:
    """Demonstrate exception handling in async code."""
    print("Running exception handling example...")
    
    async def operation_with_error() -> None:
        """Operation that may raise an error."""
        await wait_ns(10)
        raise ValueError("Simulated error")
    
    try:
        await operation_with_error()
    except ValueError as e:
        print(f"Caught exception: {e}")


async def sequential_execution() -> None:
    """Demonstrate sequential coroutine execution."""
    print("Running sequential execution example...")
    
    async def step1() -> str:
        await wait_ns(10)
        return "Step 1 complete"
    
    async def step2(prev_result: str) -> str:
        await wait_ns(10)
        return f"{prev_result}, Step 2 complete"
    
    async def step3(prev_result: str) -> str:
        await wait_ns(10)
        return f"{prev_result}, Step 3 complete"
    
    result1 = await step1()
    result2 = await step2(result1)
    result3 = await step3(result2)
    print(f"Final result: {result3}")


def main() -> None:
    """Run async/await examples."""
    print("=" * 60)
    print("Module 1 Example 1.3: Async/Await for Simulation")
    print("=" * 60)
    print()
    
    print("1. Sequential execution:")
    asyncio.run(sequential_execution())
    print()
    
    print("2. Parallel tasks:")
    asyncio.run(parallel_tasks_example())
    print()
    
    print("3. Timeout handling:")
    asyncio.run(timeout_example())
    print()
    
    print("4. Exception handling:")
    asyncio.run(exception_handling_example())
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

