"""
Module 8 Example 8.6: String Utilities
Demonstrates string manipulation utilities for UVM.
"""

from pyuvm import *


class StringUtilsExample(uvm_component):
    """Component demonstrating string utilities."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("String Utilities Example")
        self.logger.info("=" * 60)
    
    async def run_phase(self):
        """Demonstrate string utilities."""
        self.raise_objection()
        
        # String formatting
        self.logger.info("String Formatting:")
        data = 0x1234
        addr = 0xABCD
        formatted = f"data=0x{data:04X}, addr=0x{addr:04X}"
        self.logger.info(f"  Formatted: {formatted}")
        
        # String conversion
        self.logger.info("String Conversion:")
        hex_str = hex(data)
        bin_str = bin(data)
        self.logger.info(f"  Hex: {hex_str}")
        self.logger.info(f"  Bin: {bin_str}")
        
        # String manipulation
        self.logger.info("String Manipulation:")
        path = "module8/examples/string_utils/string_utils_example.py"
        basename = path.split('/')[-1]
        dirname = '/'.join(path.split('/')[:-1])
        self.logger.info(f"  Path: {path}")
        self.logger.info(f"  Basename: {basename}")
        self.logger.info(f"  Dirname: {dirname}")
        
        # String comparison
        self.logger.info("String Comparison:")
        str1 = "test_mode"
        str2 = "TEST_MODE"
        self.logger.info(f"  Case-sensitive: {str1 == str2}")
        self.logger.info(f"  Case-insensitive: {str1.lower() == str2.lower()}")
        
        # String utilities for UVM
        self.logger.info("UVM String Utilities:")
        component_name = "my_agent.driver"
        self.logger.info(f"  Component name: {component_name}")
        self.logger.info(f"  Split by '.': {component_name.split('.')}")
        self.logger.info(f"  Last part: {component_name.split('.')[-1]}")
        
        # Transaction string representation
        self.logger.info("Transaction String Representation:")
        txn_data = {
            'data': 0xAA,
            'address': 0x1000,
            'timestamp': 100
        }
        txn_str = ", ".join([f"{k}=0x{v:04X}" if isinstance(v, int) else f"{k}={v}" 
                            for k, v in txn_data.items()])
        self.logger.info(f"  Transaction: {txn_str}")
        
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("String utilities example completed")
        self.logger.info("=" * 60)


@uvm_test()
class StringUtilsTest(uvm_test):
    """Test demonstrating string utilities."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("String Utilities Test")
        self.logger.info("=" * 60)
        self.example = StringUtilsExample.create("example", self)
    
    async def run_phase(self):
        self.raise_objection()
        await Timer(10, units="ns")
        self.drop_objection()


if __name__ == "__main__":
    print("This is a pyuvm string utilities example.")
    print("Python provides rich string manipulation capabilities.")
    print("Use f-strings, format(), and standard string methods.")

