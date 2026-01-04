"""
Module 1 Example 1.1: Python Class Basics
Demonstrates classes, inheritance, and special methods for verification.
"""

from typing import Any, Optional
from dataclasses import dataclass
import random


class Transaction:
    """
    Base transaction class for verification.
    
    This class demonstrates:
    - Class definition
    - Instance variables
    - Methods
    - Special methods (__str__, __repr__, __eq__)
    """
    
    _id_counter = 0  # Class variable
    
    def __init__(self, data: Optional[Any] = None) -> None:
        """
        Initialize a transaction.
        
        Args:
            data: Optional data payload
        """
        Transaction._id_counter += 1
        self.id = Transaction._id_counter
        self.data = data
        self.timestamp = 0
    
    def __str__(self) -> str:
        """String representation for user display."""
        return f"Transaction(id={self.id}, data={self.data}, timestamp={self.timestamp})"
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Transaction(id={self.id}, data={self.data!r}, timestamp={self.timestamp})"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Transaction):
            return False
        return self.id == other.id and self.data == other.data
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries."""
        return hash((self.id, self.data))
    
    def set_timestamp(self, timestamp: int) -> None:
        """Set transaction timestamp."""
        self.timestamp = timestamp
    
    def get_id(self) -> int:
        """Get transaction ID."""
        return self.id


class ReadTransaction(Transaction):
    """
    Read transaction class.
    
    Demonstrates inheritance and method overriding.
    """
    
    def __init__(self, address: int, data: Optional[int] = None) -> None:
        """
        Initialize a read transaction.
        
        Args:
            address: Memory address to read from
            data: Optional expected data value
        """
        super().__init__(data)
        self.address = address
        self.transaction_type = "READ"
    
    def __str__(self) -> str:
        """Override string representation."""
        return f"ReadTransaction(id={self.id}, address=0x{self.address:X}, data={self.data})"
    
    def get_address(self) -> int:
        """Get read address."""
        return self.address


class WriteTransaction(Transaction):
    """
    Write transaction class.
    
    Demonstrates inheritance and method overriding.
    """
    
    def __init__(self, address: int, data: int) -> None:
        """
        Initialize a write transaction.
        
        Args:
            address: Memory address to write to
            data: Data value to write
        """
        super().__init__(data)
        self.address = address
        self.transaction_type = "WRITE"
    
    def __str__(self) -> str:
        """Override string representation."""
        return f"WriteTransaction(id={self.id}, address=0x{self.address:X}, data=0x{self.data:X})"
    
    def get_address(self) -> int:
        """Get write address."""
        return self.address


def main() -> None:
    """Run example demonstrating transaction classes."""
    print("=" * 60)
    print("Module 1 Example 1.1: Python Class Basics")
    print("=" * 60)
    print()
    
    # Create base transaction
    print("1. Creating base transaction:")
    txn1 = Transaction(data=0x1234)
    print(f"   {txn1}")
    print(f"   Transaction ID: {txn1.get_id()}")
    print()
    
    # Create read transaction
    print("2. Creating read transaction (inheritance):")
    read_txn = ReadTransaction(address=0x1000, data=0xDEAD)
    print(f"   {read_txn}")
    print(f"   Address: 0x{read_txn.get_address():X}")
    print()
    
    # Create write transaction
    print("3. Creating write transaction (inheritance):")
    write_txn = WriteTransaction(address=0x2000, data=0xBEEF)
    print(f"   {write_txn}")
    print(f"   Address: 0x{write_txn.get_address():X}")
    print()
    
    # Demonstrate equality
    print("4. Testing equality:")
    txn2 = Transaction(data=0x1234)
    txn2.id = txn1.id  # Same ID
    print(f"   txn1 == txn2: {txn1 == txn2}")
    print(f"   txn1 == read_txn: {txn1 == read_txn}")
    print()
    
    # Demonstrate hash (for sets/dicts)
    print("5. Using transactions in a set (requires __hash__):")
    transaction_set = {txn1, txn2, read_txn, write_txn}
    print(f"   Set size: {len(transaction_set)}")
    for txn in transaction_set:
        print(f"   - {txn}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

