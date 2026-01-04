"""
Module 8 Example 8.9: Utility Integration
Demonstrates integrating multiple utilities in a testbench.
"""

from pyuvm import *
import sys
import random
from collections import deque


class IntegrationTransaction(uvm_sequence_item):
    """Transaction for integration example."""
    
    def __init__(self, name="IntegrationTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.transaction_id = 0
    
    def __str__(self):
        return f"id={self.transaction_id}, data=0x{self.data:02X}, addr=0x{self.address:04X}"
    
    def reset(self):
        """Reset for reuse."""
        self.data = 0
        self.address = 0
        self.transaction_id = 0


class TransactionPool(uvm_component):
    """Object pool for transaction reuse."""
    
    def __init__(self, name="TransactionPool", parent=None, pool_size=10):
        super().__init__(name, parent)
        self.pool_size = pool_size
        self.pool = deque()
        self.allocated = []
    
    def build_phase(self):
        for _ in range(self.pool_size):
            self.pool.append(IntegrationTransaction())
    
    def get(self):
        """Get transaction from pool."""
        if len(self.pool) > 0:
            return self.pool.popleft()
        return IntegrationTransaction()
    
    def put(self, txn):
        """Return transaction to pool."""
        txn.reset()
        if len(self.pool) < self.pool_size:
            self.pool.append(txn)


class IntegrationComparator(uvm_component):
    """Comparator for transaction comparison."""
    
    def __init__(self, name="IntegrationComparator", parent=None):
        super().__init__(name, parent)
        self.expected_ap = uvm_analysis_export("expected_ap", self)
        self.actual_ap = uvm_analysis_export("actual_ap", self)
        self.expected_imp = uvm_analysis_imp("expected_imp", self)
        self.actual_imp = uvm_analysis_imp("actual_imp", self)
        self.expected_ap.connect(self.expected_imp)
        self.actual_ap.connect(self.actual_imp)
        self.expected_queue = deque()
        self.matches = 0
        self.mismatches = 0
    
    def write_expected(self, txn):
        """Receive expected transaction."""
        self.expected_queue.append(txn)
        self.compare()
    
    def write_actual(self, txn):
        """Receive actual transaction."""
        if len(self.expected_queue) > 0:
            expected = self.expected_queue.popleft()
            if expected.data == txn.data and expected.address == txn.address:
                self.matches += 1
            else:
                self.mismatches += 1
        self.compare()
    
    def compare(self):
        """Compare transactions."""
        pass


class IntegrationRecorder(uvm_component):
    """Recorder for transaction recording."""
    
    def __init__(self, name="IntegrationRecorder", parent=None):
        super().__init__(name, parent)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.recorded = []
    
    def write(self, txn):
        """Record transaction."""
        self.recorded.append(str(txn))
        self.logger.debug(f"[{self.get_name()}] Recorded: {txn}")


class IntegrationScoreboard(uvm_scoreboard):
    """Scoreboard using multiple utilities."""
    
    def build_phase(self):
        self.logger.info("Building Integration Scoreboard")
        self.comparator = IntegrationComparator.create("comparator", self)
        self.recorder = IntegrationRecorder.create("recorder", self)
        self.expected_ap = uvm_analysis_port("expected_ap", self)
        self.actual_ap = uvm_analysis_port("actual_ap", self)
        self.ap = uvm_analysis_port("ap", self)
    
    def connect_phase(self):
        self.expected_ap.connect(self.comparator.expected_ap)
        self.actual_ap.connect(self.comparator.actual_ap)
        self.ap.connect(self.recorder.ap)
    
    def write_expected(self, txn):
        """Write expected transaction."""
        self.expected_ap.write(txn)
        self.ap.write(txn)
    
    def write_actual(self, txn):
        """Write actual transaction."""
        self.actual_ap.write(txn)
        self.ap.write(txn)


class IntegrationSequence(uvm_sequence):
    """Sequence using pool and random utilities."""
    
    async def body(self):
        """Generate transactions using pool and random."""
        # Get pool from environment
        env = self.get_env()
        pool = env.pool if hasattr(env, 'pool') else None
        
        # Get number of transactions from CLP
        num_txns = env.num_transactions if hasattr(env, 'num_transactions') else 10
        
        # Get seed from CLP
        seed = env.seed if hasattr(env, 'seed') else None
        if seed is not None:
            random.seed(seed)
        
        for i in range(num_txns):
            # Get transaction from pool
            if pool:
                txn = pool.get()
            else:
                txn = IntegrationTransaction()
            
            # Randomize transaction
            txn.transaction_id = i
            txn.data = random.randint(0, 0xFF)
            txn.address = random.randint(0x1000, 0x2000)
            
            await self.start_item(txn)
            await self.finish_item(txn)
            
            # Return to pool
            if pool:
                pool.put(txn)
            
            await Timer(10, units="ns")


class IntegrationAgent(uvm_agent):
    """Agent for integration example."""
    
    def build_phase(self):
        self.logger.info("Building Integration Agent")
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Integration Agent")


class IntegrationEnv(uvm_env):
    """Environment demonstrating utility integration."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Integration Environment")
        self.logger.info("=" * 60)
        
        # Get CLP arguments
        self.num_transactions = int(self.get_clp_arg("+num_transactions", "10"))
        self.seed = int(self.get_clp_arg("+seed", "0"))
        self.use_pool = self.get_clp_arg("+use_pool", "true").lower() == "true"
        
        self.logger.info(f"CLP Configuration:")
        self.logger.info(f"  num_transactions: {self.num_transactions}")
        self.logger.info(f"  seed: {self.seed}")
        self.logger.info(f"  use_pool: {self.use_pool}")
        
        # Create components
        self.agent = IntegrationAgent.create("agent", self)
        self.scoreboard = IntegrationScoreboard.create("scoreboard", self)
        
        # Create pool if enabled
        if self.use_pool:
            self.pool = TransactionPool.create("pool", self, pool_size=5)
    
    def get_clp_arg(self, arg_name, default_value):
        """Get command-line argument."""
        clean_name = arg_name.lstrip('+')
        for i, arg in enumerate(sys.argv):
            if arg.startswith(f"+{clean_name}="):
                return arg.split('=')[1]
            elif arg == f"+{clean_name}":
                if i + 1 < len(sys.argv):
                    return sys.argv[i + 1]
                return "1"
        return default_value
    
    def connect_phase(self):
        self.logger.info("Connecting Integration Environment")


@uvm_test()
class IntegrationTest(uvm_test):
    """Test demonstrating utility integration."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Utility Integration Example Test")
        self.logger.info("=" * 60)
        self.env = IntegrationEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running integration test")
        
        # Start sequence
        seq = IntegrationSequence.create("seq")
        await seq.start(self.env.agent.seqr)
        
        # Generate expected transactions
        for i in range(self.env.num_transactions):
            txn = IntegrationTransaction()
            txn.transaction_id = i
            txn.data = random.randint(0, 0xFF)
            txn.address = random.randint(0x1000, 0x2000)
            self.env.scoreboard.write_expected(txn)
        
        await Timer(200, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Integration test completed")
        self.logger.info("=" * 60)
        self.logger.info("Utilities used:")
        self.logger.info("  - Command Line Processor (CLP)")
        self.logger.info("  - Transaction Pool")
        self.logger.info("  - Comparator")
        self.logger.info("  - Recorder")
        self.logger.info("  - Random utilities")


if __name__ == "__main__":
    print("Utility Integration Example")
    print("=" * 60)
    print("This example demonstrates integrating multiple utilities.")
    print("")
    print("Usage:")
    print("  python integration_example.py +num_transactions=20 +seed=42 +use_pool=true")
    print("")

