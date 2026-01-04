"""
Module 4 Example: Transaction-Level Modeling
Demonstrates transaction design, operations, and methods.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer
import copy


class BaseTransaction(uvm_sequence_item):
    """Base transaction class."""
    
    def __init__(self, name="BaseTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"{self.get_name()}: data=0x{self.data:02X}, addr=0x{self.address:04X}"
    
    def __eq__(self, other):
        """Equality comparison."""
        if not isinstance(other, BaseTransaction):
            return False
        return self.data == other.data and self.address == other.address
    
    def copy(self):
        """Create a copy of the transaction."""
        txn = BaseTransaction()
        txn.data = self.data
        txn.address = self.address
        return txn


class ExtendedTransaction(BaseTransaction):
    """Extended transaction with additional fields."""
    
    def __init__(self, name="ExtendedTransaction"):
        super().__init__(name)
        self.control = 0
        self.status = 0
    
    def __str__(self):
        return (f"{self.get_name()}: data=0x{self.data:02X}, "
                f"addr=0x{self.address:04X}, ctrl=0x{self.control:02X}, "
                f"status=0x{self.status:02X}")
    
    def __eq__(self, other):
        """Equality comparison."""
        if not isinstance(other, ExtendedTransaction):
            return False
        return (super().__eq__(other) and 
                self.control == other.control and 
                self.status == other.status)


class ConstrainedTransaction(uvm_sequence_item):
    """Transaction with constraints."""
    
    def __init__(self, name="ConstrainedTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def randomize(self):
        """Randomize transaction fields with constraints."""
        import random
        # Constraint: address must be aligned to 4-byte boundary
        self.address = random.randint(0, 0xFFFF) & ~0x3
        # Constraint: data must be non-zero
        self.data = random.randint(1, 255)
        return True
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class TransactionWithMethods(uvm_sequence_item):
    """Transaction demonstrating useful methods."""
    
    def __init__(self, name="TransactionWithMethods"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def pack(self):
        """Pack transaction into bytes."""
        return bytes([self.data, self.address & 0xFF, (self.address >> 8) & 0xFF])
    
    def unpack(self, data):
        """Unpack bytes into transaction."""
        if len(data) >= 3:
            self.data = data[0]
            self.address = data[1] | (data[2] << 8)
    
    def convert2string(self):
        """Convert to string representation."""
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"
    
    def do_copy(self, rhs):
        """Copy method for UVM."""
        self.data = rhs.data
        self.address = rhs.address
    
    def do_compare(self, rhs, comparer):
        """Compare method for UVM."""
        return self.data == rhs.data and self.address == rhs.address


class TransactionTest(uvm_test):
    """Test demonstrating transaction usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Transaction Example Test")
        self.logger.info("=" * 60)
    
    async def run_phase(self):
        self.raise_objection()
        
        # Base transaction
        self.logger.info("=" * 60)
        self.logger.info("Base Transaction:")
        txn1 = BaseTransaction("txn1")
        txn1.data = 0xAB
        txn1.address = 0x1000
        self.logger.info(f"Created: {txn1}")
        
        # Transaction copy
        txn2 = txn1.copy()
        self.logger.info(f"Copied: {txn2}")
        
        # Transaction comparison
        self.logger.info(f"txn1 == txn2: {txn1 == txn2}")
        
        # Extended transaction
        self.logger.info("=" * 60)
        self.logger.info("Extended Transaction:")
        ext_txn = ExtendedTransaction("ext_txn")
        ext_txn.data = 0xCD
        ext_txn.address = 0x2000
        ext_txn.control = 0x01
        ext_txn.status = 0x80
        self.logger.info(f"Created: {ext_txn}")
        
        # Constrained transaction
        self.logger.info("=" * 60)
        self.logger.info("Constrained Transaction:")
        const_txn = ConstrainedTransaction("const_txn")
        const_txn.randomize()
        self.logger.info(f"Randomized: {const_txn}")
        self.logger.info(f"Address aligned: {const_txn.address % 4 == 0}")
        
        # Transaction with methods
        self.logger.info("=" * 60)
        self.logger.info("Transaction with Methods:")
        method_txn = TransactionWithMethods("method_txn")
        method_txn.data = 0xEF
        method_txn.address = 0x3000
        self.logger.info(f"Created: {method_txn}")
        
        # Pack/unpack
        packed = method_txn.pack()
        self.logger.info(f"Packed: {packed.hex()}")
        
        unpacked = TransactionWithMethods("unpacked_txn")
        unpacked.unpack(packed)
        self.logger.info(f"Unpacked: {unpacked}")
        
        await Timer(10, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Transaction test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_transaction(dut):
    """Cocotb test wrapper for pyuvm transaction test."""
    import inspect
    test = TransactionTest.create("test")
    await test.build_phase()
    if hasattr(test, 'connect_phase') and inspect.iscoroutinefunction(test.connect_phase):
        await test.connect_phase()
    await test.run_phase()
    if hasattr(test, 'check_phase'):
        test.check_phase()
    test.report_phase()


if __name__ == "__main__":
    print("This is a pyuvm transaction example.")
    print("To run with cocotb, use the Makefile in the test directory.")

