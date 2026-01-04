"""
Module 8 Example 8.5: UVM Queues
Demonstrates queue data structures for transaction management.
"""

from pyuvm import *
from collections import deque


class QueueTransaction(uvm_sequence_item):
    """Transaction for queue example."""
    
    def __init__(self, name="QueueTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.priority = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, priority={self.priority}"


class TransactionQueue(uvm_component):
    """
    Queue for transaction management.
    
    Uses Python's deque for efficient queue operations.
    """
    
    def __init__(self, name="TransactionQueue", parent=None, max_size=None):
        super().__init__(name, parent)
        self.max_size = max_size
        self.queue = deque()
        self.added_count = 0
        self.removed_count = 0
        self.overflow_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Transaction Queue (max_size: {self.max_size or 'unlimited'})")
    
    def push(self, item):
        """Add item to queue."""
        if self.max_size and len(self.queue) >= self.max_size:
            self.overflow_count += 1
            self.logger.warning(f"[{self.get_name()}] Queue full, overflow: {item}")
            return False
        
        self.queue.append(item)
        self.added_count += 1
        self.logger.debug(f"[{self.get_name()}] Pushed: {item} (size: {len(self.queue)})")
        return True
    
    def pop(self):
        """Remove and return item from queue."""
        if len(self.queue) == 0:
            self.logger.warning(f"[{self.get_name()}] Queue empty")
            return None
        
        item = self.queue.popleft()
        self.removed_count += 1
        self.logger.debug(f"[{self.get_name()}] Popped: {item} (size: {len(self.queue)})")
        return item
    
    def peek(self):
        """Peek at front of queue without removing."""
        if len(self.queue) == 0:
            return None
        return self.queue[0]
    
    def size(self):
        """Get queue size."""
        return len(self.queue)
    
    def is_empty(self):
        """Check if queue is empty."""
        return len(self.queue) == 0
    
    def is_full(self):
        """Check if queue is full."""
        return self.max_size and len(self.queue) >= self.max_size
    
    def clear(self):
        """Clear queue."""
        self.queue.clear()
        self.logger.info(f"[{self.get_name()}] Queue cleared")
    
    def report_phase(self):
        """Report phase - show queue statistics."""
        self.logger.info(f"[{self.get_name()}] Queue Statistics:")
        self.logger.info(f"  Max size: {self.max_size or 'unlimited'}")
        self.logger.info(f"  Current size: {len(self.queue)}")
        self.logger.info(f"  Items added: {self.added_count}")
        self.logger.info(f"  Items removed: {self.removed_count}")
        self.logger.info(f"  Overflows: {self.overflow_count}")


class PriorityQueue(uvm_component):
    """
    Priority queue for transactions.
    
    Orders transactions by priority.
    """
    
    def __init__(self, name="PriorityQueue", parent=None):
        super().__init__(name, parent)
        self.queue = []
        self.added_count = 0
        self.removed_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Priority Queue")
    
    def push(self, item):
        """Add item to priority queue."""
        # Use priority for ordering (higher priority first)
        priority = item.priority if hasattr(item, 'priority') else 0
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0], reverse=True)  # Sort by priority (descending)
        self.added_count += 1
        self.logger.debug(f"[{self.get_name()}] Pushed (priority={priority}): {item}")
    
    def pop(self):
        """Remove and return highest priority item."""
        if len(self.queue) == 0:
            return None
        
        priority, item = self.queue.pop(0)
        self.removed_count += 1
        self.logger.debug(f"[{self.get_name()}] Popped (priority={priority}): {item}")
        return item
    
    def size(self):
        """Get queue size."""
        return len(self.queue)
    
    def report_phase(self):
        """Report phase - show queue statistics."""
        self.logger.info(f"[{self.get_name()}] Priority Queue Statistics:")
        self.logger.info(f"  Current size: {len(self.queue)}")
        self.logger.info(f"  Items added: {self.added_count}")
        self.logger.info(f"  Items removed: {self.removed_count}")


class QueueScoreboard(uvm_scoreboard):
    """Scoreboard using queue for transaction buffering."""
    
    def build_phase(self):
        self.logger.info("Building Queue Scoreboard")
        self.queue = TransactionQueue.create("queue", self, max_size=100)
        self.ap = uvm_analysis_port("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
    
    def write(self, txn):
        """Receive transaction and add to queue."""
        if not self.queue.push(txn):
            self.logger.error(f"[{self.get_name()}] Failed to add transaction to queue: {txn}")
    
    async def run_phase(self):
        """Process queue."""
        while True:
            if not self.queue.is_empty():
                txn = self.queue.pop()
                self.logger.info(f"[{self.get_name()}] Processing: {txn}")
            await Timer(10, units="ns")


class QueueEnv(uvm_env):
    """Environment demonstrating queue usage."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Queue Environment")
        self.logger.info("=" * 60)
        self.scoreboard = QueueScoreboard.create("scoreboard", self)
        self.priority_queue = PriorityQueue.create("priority_queue", self)
        self.ap = uvm_analysis_port("ap", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Queue Environment")
        self.ap.connect(self.scoreboard.ap)


@uvm_test()
class QueueTest(uvm_test):
    """Test demonstrating queue usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Queue Example Test")
        self.logger.info("=" * 60)
        self.env = QueueEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running queue test")
        
        # Test regular queue
        for i in range(10):
            txn = QueueTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            txn.priority = i % 3
            self.env.ap.write(txn)
            await Timer(10, units="ns")
        
        # Test priority queue
        for i in range(5):
            txn = QueueTransaction()
            txn.data = i * 0x20
            txn.address = i * 0x200
            txn.priority = 5 - i  # Higher priority first
            self.env.priority_queue.push(txn)
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Queue test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm queue example.")
    print("To run with cocotb, use the Makefile in the test directory.")

