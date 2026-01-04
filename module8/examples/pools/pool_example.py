"""
Module 8 Example 8.4: UVM Pools
Demonstrates object pooling for performance optimization.
"""

from pyuvm import *


class PoolTransaction(uvm_sequence_item):
    """Transaction for pool example."""
    
    def __init__(self, name="PoolTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"
    
    def reset(self):
        """Reset transaction for reuse."""
        self.data = 0
        self.address = 0


class TransactionPool(uvm_component):
    """
    Object pool for transaction reuse.
    
    Reduces memory allocation overhead by reusing objects.
    """
    
    def __init__(self, name="TransactionPool", parent=None, pool_size=10):
        super().__init__(name, parent)
        self.pool_size = pool_size
        self.pool = []
        self.allocated = []
        self.allocated_count = 0
        self.reused_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Transaction Pool (size: {self.pool_size})")
        # Pre-allocate pool
        for _ in range(self.pool_size):
            txn = PoolTransaction()
            self.pool.append(txn)
    
    def get(self):
        """Get transaction from pool."""
        if len(self.pool) > 0:
            txn = self.pool.pop()
            self.reused_count += 1
        else:
            # Pool empty, create new transaction
            txn = PoolTransaction()
            self.allocated_count += 1
        
        self.allocated.append(txn)
        self.logger.debug(f"[{self.get_name()}] Allocated transaction: {txn}")
        return txn
    
    def put(self, txn):
        """Return transaction to pool."""
        if txn in self.allocated:
            self.allocated.remove(txn)
        
        # Reset transaction for reuse
        if hasattr(txn, 'reset'):
            txn.reset()
        
        # Return to pool if not full
        if len(self.pool) < self.pool_size:
            self.pool.append(txn)
            self.logger.debug(f"[{self.get_name()}] Returned transaction to pool")
        else:
            # Pool full, discard transaction
            self.logger.debug(f"[{self.get_name()}] Pool full, discarding transaction")
    
    def report_phase(self):
        """Report phase - show pool statistics."""
        self.logger.info(f"[{self.get_name()}] Pool Statistics:")
        self.logger.info(f"  Pool size: {self.pool_size}")
        self.logger.info(f"  Currently in pool: {len(self.pool)}")
        self.logger.info(f"  Currently allocated: {len(self.allocated)}")
        self.logger.info(f"  Reused transactions: {self.reused_count}")
        self.logger.info(f"  New allocations: {self.allocated_count}")
        self.logger.info(f"  Reuse rate: {self.reused_count / (self.reused_count + self.allocated_count) * 100:.1f}%" if (self.reused_count + self.allocated_count) > 0 else "  Reuse rate: N/A")


class PoolAgent(uvm_agent):
    """Agent using transaction pool."""
    
    def build_phase(self):
        self.logger.info("Building Pool Agent")
        self.pool = TransactionPool.create("pool", self, pool_size=5)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Pool Agent")


class PoolSequence(uvm_sequence):
    """Sequence using transaction pool."""
    
    async def body(self):
        """Generate transactions using pool."""
        # Get pool from parent
        agent = self.get_parent()
        pool = agent.pool if hasattr(agent, 'pool') else None
        
        for i in range(20):
            # Get transaction from pool
            if pool:
                txn = pool.get()
            else:
                txn = PoolTransaction()
            
            # Configure transaction
            txn.data = i * 0x10
            txn.address = i * 0x100
            
            await self.start_item(txn)
            await self.finish_item(txn)
            
            # Return transaction to pool
            if pool:
                pool.put(txn)
            
            await Timer(10, units="ns")


class PoolEnv(uvm_env):
    """Environment demonstrating pool usage."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Pool Environment")
        self.logger.info("=" * 60)
        self.agent = PoolAgent.create("agent", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Pool Environment")


@uvm_test()
class PoolTest(uvm_test):
    """Test demonstrating pool usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Pool Example Test")
        self.logger.info("=" * 60)
        self.env = PoolEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running pool test")
        
        # Start sequence
        seq = PoolSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Pool test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm pool example.")
    print("To run with cocotb, use the Makefile in the test directory.")

