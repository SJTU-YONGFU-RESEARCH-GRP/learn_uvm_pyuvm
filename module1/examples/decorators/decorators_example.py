"""
Module 1 Example 1.2: Decorators and Context Managers
Demonstrates Python decorators, context managers, and verification patterns.
"""

import time
import functools
from typing import Callable, Any
from contextlib import contextmanager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Demonstrates function decorators.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def log_calls_decorator(func: Callable) -> Callable:
    """
    Decorator to log function calls.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper


class VerificationContext:
    """
    Context manager for verification operations.
    
    Demonstrates context manager protocol.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize verification context."""
        self.name = name
        self.start_time: float = 0.0
    
    def __enter__(self) -> "VerificationContext":
        """Enter context manager."""
        logger.info(f"Entering verification context: {self.name}")
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Exit context manager."""
        elapsed = time.time() - self.start_time
        if exc_type is None:
            logger.info(f"Exiting verification context: {self.name} (success, {elapsed:.4f}s)")
        else:
            logger.error(f"Exiting verification context: {self.name} (error: {exc_type.__name__}, {elapsed:.4f}s)")
        return False  # Don't suppress exceptions
    
    def elapsed_time(self) -> float:
        """Get elapsed time in context."""
        return time.time() - self.start_time


@contextmanager
def simulation_phase(phase_name: str):
    """
    Context manager for simulation phases.
    
    Demonstrates contextlib.contextmanager decorator.
    """
    logger.info(f"Starting simulation phase: {phase_name}")
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"Completed simulation phase: {phase_name} ({elapsed:.4f}s)")


class VerificationTest:
    """
    Example test class using decorators.
    """
    
    @timing_decorator
    @log_calls_decorator
    def setup(self) -> None:
        """Setup test environment."""
        logger.info("Setting up test environment")
        time.sleep(0.1)  # Simulate setup time
    
    @timing_decorator
    def run_test(self, test_name: str) -> bool:
        """Run a test."""
        logger.info(f"Running test: {test_name}")
        time.sleep(0.05)  # Simulate test execution
        return True
    
    @timing_decorator
    def teardown(self) -> None:
        """Teardown test environment."""
        logger.info("Tearing down test environment")
        time.sleep(0.05)  # Simulate teardown time


def main() -> None:
    """Run decorator and context manager examples."""
    print("=" * 60)
    print("Module 1 Example 1.2: Decorators and Context Managers")
    print("=" * 60)
    print()
    
    # Demonstrate decorators
    print("1. Using function decorators:")
    test = VerificationTest()
    test.setup()
    test.run_test("test_example")
    test.teardown()
    print()
    
    # Demonstrate context manager (class-based)
    print("2. Using context manager (class-based):")
    with VerificationContext("test_context") as ctx:
        time.sleep(0.1)
        print(f"   Elapsed time: {ctx.elapsed_time():.4f}s")
    print()
    
    # Demonstrate context manager (function-based)
    print("3. Using context manager (function-based):")
    with simulation_phase("reset_phase"):
        time.sleep(0.05)
        logger.info("   Performing reset operations")
    
    with simulation_phase("test_phase"):
        time.sleep(0.1)
        logger.info("   Running test operations")
    print()
    
    # Demonstrate nested context managers
    print("4. Using nested context managers:")
    with VerificationContext("outer") as outer:
        with VerificationContext("inner") as inner:
            time.sleep(0.05)
            print(f"   Inner elapsed: {inner.elapsed_time():.4f}s")
        print(f"   Outer elapsed: {outer.elapsed_time():.4f}s")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

