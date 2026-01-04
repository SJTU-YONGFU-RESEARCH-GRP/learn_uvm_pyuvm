"""
Module 1: Error Handling and Logging
Demonstrates exception handling and logging for verification.
"""

import logging
from typing import Optional, List
from enum import Enum


# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('verification.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class VerificationError(Exception):
    """Base exception for verification errors."""
    pass


class MismatchError(VerificationError):
    """Exception for data mismatches."""
    
    def __init__(self, expected: int, actual: int, address: int) -> None:
        """Initialize mismatch error."""
        self.expected = expected
        self.actual = actual
        self.address = address
        super().__init__(f"Mismatch at address 0x{address:X}: expected 0x{expected:X}, got 0x{actual:X}")


class TimeoutError(VerificationError):
    """Exception for timeouts."""
    
    def __init__(self, operation: str, timeout_ns: int) -> None:
        """Initialize timeout error."""
        self.operation = operation
        self.timeout_ns = timeout_ns
        super().__init__(f"Timeout in {operation} after {timeout_ns}ns")


class VerificationResult(Enum):
    """Verification result types."""
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class VerificationChecker:
    """
    Verification checker with error handling.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize checker."""
        self.name = name
        self.results: List[VerificationResult] = []
        self.errors: List[Exception] = []
        logger.info(f"Initialized verification checker: {name}")
    
    def check_data(self, address: int, expected: int, actual: int) -> bool:
        """
        Check data match.
        
        Args:
            address: Memory address
            expected: Expected data value
            actual: Actual data value
            
        Returns:
            True if match, False otherwise
            
        Raises:
            MismatchError: If data doesn't match
        """
        try:
            if expected != actual:
                error = MismatchError(expected, actual, address)
                logger.error(f"{self.name}: {error}")
                self.errors.append(error)
                self.results.append(VerificationResult.FAIL)
                raise error
            else:
                logger.debug(f"{self.name}: Match at address 0x{address:X}: 0x{expected:X}")
                self.results.append(VerificationResult.PASS)
                return True
        except MismatchError:
            raise
        except Exception as e:
            logger.exception(f"{self.name}: Unexpected error in check_data")
            self.errors.append(e)
            self.results.append(VerificationResult.ERROR)
            raise
    
    def check_with_retry(self, operation, max_retries: int = 3) -> bool:
        """
        Check operation with retry logic.
        
        Args:
            operation: Function to execute
            max_retries: Maximum number of retries
            
        Returns:
            True if operation succeeds
        """
        for attempt in range(max_retries):
            try:
                result = operation()
                logger.info(f"{self.name}: Operation succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                logger.warning(f"{self.name}: Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"{self.name}: Operation failed after {max_retries} attempts")
                    self.errors.append(e)
                    self.results.append(VerificationResult.ERROR)
                    raise
        return False
    
    def get_statistics(self) -> dict:
        """Get verification statistics."""
        stats = {
            'total': len(self.results),
            'pass': sum(1 for r in self.results if r == VerificationResult.PASS),
            'fail': sum(1 for r in self.results if r == VerificationResult.FAIL),
            'error': sum(1 for r in self.results if r == VerificationResult.ERROR),
            'errors': len(self.errors)
        }
        return stats


def example_basic_error_handling() -> None:
    """Demonstrate basic error handling."""
    print("1. Basic Error Handling:")
    
    checker = VerificationChecker("BasicChecker")
    
    # Successful check
    try:
        checker.check_data(address=0x1000, expected=0x1234, actual=0x1234)
        print("   ✓ Successful check passed")
    except MismatchError:
        print("   ✗ Unexpected mismatch")
    
    # Failed check
    try:
        checker.check_data(address=0x2000, expected=0x5678, actual=0x9ABC)
        print("   ✗ Should have raised MismatchError")
    except MismatchError as e:
        print(f"   ✓ Caught expected error: {e}")
    
    stats = checker.get_statistics()
    print(f"   Statistics: {stats}")
    print()


def example_exception_chaining() -> None:
    """Demonstrate exception chaining."""
    print("2. Exception Chaining:")
    
    try:
        try:
            # Simulate an operation that fails
            raise ValueError("Original error")
        except ValueError as e:
            # Chain the exception
            raise VerificationError("Verification failed") from e
    except VerificationError as e:
        logger.error(f"Caught chained exception: {e}")
        logger.error(f"Original exception: {e.__cause__}")
        print(f"   ✓ Exception chaining demonstrated")
    print()


def example_retry_logic() -> None:
    """Demonstrate retry logic."""
    print("3. Retry Logic:")
    
    checker = VerificationChecker("RetryChecker")
    
    attempt_count = 0
    
    def flaky_operation() -> bool:
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise TimeoutError("flaky_operation", 100)
        return True
    
    try:
        result = checker.check_with_retry(flaky_operation, max_retries=3)
        print(f"   ✓ Operation succeeded after {attempt_count} attempts")
    except Exception as e:
        print(f"   ✗ Operation failed: {e}")
    print()


def example_logging_levels() -> None:
    """Demonstrate different logging levels."""
    print("4. Logging Levels:")
    
    logger.debug("This is a DEBUG message (detailed information)")
    logger.info("This is an INFO message (general information)")
    logger.warning("This is a WARNING message (potential issues)")
    logger.error("This is an ERROR message (errors occurred)")
    logger.critical("This is a CRITICAL message (serious errors)")
    
    print("   ✓ Logging levels demonstrated (check verification.log)")
    print()


def main() -> None:
    """Run error handling and logging examples."""
    print("=" * 60)
    print("Module 1: Error Handling and Logging")
    print("=" * 60)
    print()
    
    example_basic_error_handling()
    example_exception_chaining()
    example_retry_logic()
    example_logging_levels()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print("Check 'verification.log' for detailed logs")


if __name__ == "__main__":
    main()

