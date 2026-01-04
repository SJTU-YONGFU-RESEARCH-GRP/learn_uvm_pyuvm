"""
Module 8 Example 8.8: Random Utilities
Demonstrates random number generation and constrained randomization.
"""

from pyuvm import *
import random


class RandomTransaction(uvm_sequence_item):
    """Transaction with random fields."""
    
    def __init__(self, name="RandomTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.length = 0
    
    def randomize(self, seed=None):
        """Randomize transaction fields."""
        if seed is not None:
            random.seed(seed)
        
        self.data = random.randint(0, 0xFF)
        self.address = random.randint(0, 0xFFFF)
        self.length = random.randint(1, 256)
    
    def randomize_constrained(self, data_min=0, data_max=0xFF, 
                              addr_min=0, addr_max=0xFFFF,
                              length_min=1, length_max=256, seed=None):
        """Randomize with constraints."""
        if seed is not None:
            random.seed(seed)
        
        self.data = random.randint(data_min, data_max)
        self.address = random.randint(addr_min, addr_max)
        self.length = random.randint(length_min, length_max)
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, len={self.length}"


class RandomSequence(uvm_sequence):
    """Sequence generating random transactions."""
    
    def __init__(self, name="RandomSequence", seed=None):
        super().__init__(name)
        self.seed = seed
    
    async def body(self):
        """Generate random transactions."""
        if self.seed is not None:
            random.seed(self.seed)
            self.logger.info(f"[{self.get_name()}] Using seed: {self.seed}")
        
        for i in range(10):
            txn = RandomTransaction()
            txn.randomize()
            await self.start_item(txn)
            await self.finish_item(txn)
            await Timer(10, units="ns")


class ConstrainedRandomSequence(uvm_sequence):
    """Sequence with constrained randomization."""
    
    def __init__(self, name="ConstrainedRandomSequence", seed=None):
        super().__init__(name)
        self.seed = seed
    
    async def body(self):
        """Generate constrained random transactions."""
        if self.seed is not None:
            random.seed(self.seed)
            self.logger.info(f"[{self.get_name()}] Using seed: {self.seed}")
        
        for i in range(10):
            txn = RandomTransaction()
            # Constrain: data in range 0x10-0xF0, address aligned to 4-byte boundary
            txn.randomize_constrained(
                data_min=0x10,
                data_max=0xF0,
                addr_min=0x1000,
                addr_max=0x2000,
                length_min=16,
                length_max=64,
                seed=self.seed
            )
            # Align address to 4-byte boundary
            txn.address = (txn.address // 4) * 4
            
            await self.start_item(txn)
            await self.finish_item(txn)
            await Timer(10, units="ns")


class RandomUtilsExample(uvm_component):
    """Component demonstrating random utilities."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Random Utilities Example")
        self.logger.info("=" * 60)
    
    async def run_phase(self):
        """Demonstrate random utilities."""
        self.raise_objection()
        
        # Random seed management
        self.logger.info("Random Seed Management:")
        seed = 12345
        random.seed(seed)
        self.logger.info(f"  Seed: {seed}")
        
        # Generate random values
        self.logger.info("Random Value Generation:")
        for i in range(5):
            rand_val = random.randint(0, 100)
            self.logger.info(f"  Random {i+1}: {rand_val}")
        
        # Random state
        self.logger.info("Random State:")
        state = random.getstate()
        self.logger.info(f"  State type: {type(state)}")
        
        # Constrained random
        self.logger.info("Constrained Random:")
        for i in range(5):
            rand_val = random.randint(10, 90)  # Constrained range
            self.logger.info(f"  Constrained {i+1}: {rand_val}")
        
        # Random choice
        self.logger.info("Random Choice:")
        choices = ['READ', 'WRITE', 'IDLE']
        for i in range(5):
            choice = random.choice(choices)
            self.logger.info(f"  Choice {i+1}: {choice}")
        
        # Random shuffle
        self.logger.info("Random Shuffle:")
        items = list(range(10))
        random.shuffle(items)
        self.logger.info(f"  Shuffled: {items}")
        
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Random utilities example completed")
        self.logger.info("=" * 60)


class RandomAgent(uvm_agent):
    """Agent for random utilities example."""
    
    def build_phase(self):
        self.logger.info("Building Random Agent")
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Random Agent")


class RandomEnv(uvm_env):
    """Environment demonstrating random utilities."""
    
    def build_phase(self):
        self.logger.info("Building Random Environment")
        self.agent = RandomAgent.create("agent", self)
        self.example = RandomUtilsExample.create("example", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Random Environment")


@uvm_test()
class RandomUtilsTest(uvm_test):
    """Test demonstrating random utilities."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Random Utilities Test")
        self.logger.info("=" * 60)
        self.env = RandomEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running random utilities test")
        
        # Test random sequence
        seq = RandomSequence.create("seq", seed=42)
        await seq.start(self.env.agent.seqr)
        
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Random utilities test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm random utilities example.")
    print("Python's random module provides randomization capabilities.")
    print("Use random.seed() for reproducibility and random functions for generation.")

