"""
Module 8 Example 8.7: Math Utilities
Demonstrates mathematical utilities for UVM.
"""

from pyuvm import *
import random
import statistics


class MathUtilsExample(uvm_component):
    """Component demonstrating math utilities."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Math Utilities Example")
        self.logger.info("=" * 60)
    
    async def run_phase(self):
        """Demonstrate math utilities."""
        self.raise_objection()
        
        # Random number generation
        self.logger.info("Random Number Generation:")
        random.seed(42)
        rand_int = random.randint(0, 100)
        rand_float = random.random()
        self.logger.info(f"  Random int (0-100): {rand_int}")
        self.logger.info(f"  Random float (0-1): {rand_float:.4f}")
        
        # Statistical functions
        self.logger.info("Statistical Functions:")
        data = [random.randint(0, 100) for _ in range(10)]
        mean_val = statistics.mean(data)
        median_val = statistics.median(data)
        stdev_val = statistics.stdev(data) if len(data) > 1 else 0
        self.logger.info(f"  Data: {data}")
        self.logger.info(f"  Mean: {mean_val:.2f}")
        self.logger.info(f"  Median: {median_val:.2f}")
        self.logger.info(f"  Std Dev: {stdev_val:.2f}")
        
        # Mathematical operations
        self.logger.info("Mathematical Operations:")
        value1 = 0x1234
        value2 = 0x5678
        self.logger.info(f"  Value1: 0x{value1:04X} ({value1})")
        self.logger.info(f"  Value2: 0x{value2:04X} ({value2})")
        self.logger.info(f"  Sum: 0x{value1 + value2:04X} ({value1 + value2})")
        self.logger.info(f"  Product: 0x{value1 * value2:04X} ({value1 * value2})")
        self.logger.info(f"  Bitwise AND: 0x{value1 & value2:04X}")
        self.logger.info(f"  Bitwise OR: 0x{value1 | value2:04X}")
        self.logger.info(f"  Bitwise XOR: 0x{value1 ^ value2:04X}")
        
        # Bit manipulation
        self.logger.info("Bit Manipulation:")
        value = 0xABCD
        self.logger.info(f"  Value: 0x{value:04X} ({bin(value)})")
        self.logger.info(f"  Bit 0: {(value >> 0) & 1}")
        self.logger.info(f"  Bit 8: {(value >> 8) & 1}")
        self.logger.info(f"  Set bit 4: 0x{value | (1 << 4):04X}")
        self.logger.info(f"  Clear bit 4: 0x{value & ~(1 << 4):04X}")
        
        # Range operations
        self.logger.info("Range Operations:")
        min_val = min(data)
        max_val = max(data)
        self.logger.info(f"  Min: {min_val}")
        self.logger.info(f"  Max: {max_val}")
        self.logger.info(f"  Range: {max_val - min_val}")
        
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Math utilities example completed")
        self.logger.info("=" * 60)


@uvm_test()
class MathUtilsTest(uvm_test):
    """Test demonstrating math utilities."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Math Utilities Test")
        self.logger.info("=" * 60)
        self.example = MathUtilsExample.create("example", self)
    
    async def run_phase(self):
        self.raise_objection()
        await Timer(10, units="ns")
        self.drop_objection()


if __name__ == "__main__":
    print("This is a pyuvm math utilities example.")
    print("Python provides rich mathematical capabilities.")
    print("Use random, statistics, and standard math operations.")

