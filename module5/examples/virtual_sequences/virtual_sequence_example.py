"""
Module 5 Example 5.1: Virtual Sequences
Demonstrates virtual sequencer and virtual sequence coordination.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer

# Try to import uvm_seq_item_pull_port explicitly if not available from pyuvm import *
try:
    # Check if already available
    _ = uvm_seq_item_pull_port
except NameError:
    # Try importing from TLM modules
    try:
        from pyuvm.s15_uvm_tlm_1 import uvm_seq_item_pull_port
    except (ImportError, AttributeError):
        try:
            from pyuvm.s15_uvm_tlm import uvm_seq_item_pull_port
        except (ImportError, AttributeError):
            try:
                from pyuvm.s16_uvm_tlm_1 import uvm_seq_item_pull_port
            except (ImportError, AttributeError):
                try:
                    from pyuvm.s16_uvm_tlm import uvm_seq_item_pull_port
                except (ImportError, AttributeError):
                    # Try to get from pyuvm module
                    import pyuvm
                    if hasattr(pyuvm, 'uvm_seq_item_pull_port'):
                        uvm_seq_item_pull_port = getattr(pyuvm, 'uvm_seq_item_pull_port')
                    else:
                        # Last resort: try to get from globals (might be available from pyuvm import *)
                        try:
                            uvm_seq_item_pull_port = globals()['uvm_seq_item_pull_port']
                        except KeyError:
                            # If all else fails, raise an error with helpful message
                            raise ImportError(
                                "Could not import uvm_seq_item_pull_port from pyuvm. "
                                "Tried: pyuvm.s15_uvm_tlm_1, pyuvm.s15_uvm_tlm, "
                                "pyuvm.s16_uvm_tlm_1, pyuvm.s16_uvm_tlm, pyuvm module, and globals()"
                            )


class VirtualTransaction(uvm_sequence_item):
    """Transaction for virtual sequence example."""
    
    def __init__(self, name="VirtualTransaction"):
        super().__init__(name)
        self.data = 0
        self.channel = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, channel={self.channel}"


class ChannelSequence(uvm_sequence):
    """Sequence for a single channel."""
    
    def __init__(self, name="ChannelSequence", channel=0, num_items=5):
        super().__init__(name)
        self.channel = channel
        self.num_items = num_items
    
    async def body(self):
        """Generate transactions for this channel."""
        # Sequences don't have logger by default
        print(f"[{self.get_name()}] Starting channel {self.channel} sequence")
        
        for i in range(self.num_items):
            txn = VirtualTransaction()
            txn.data = i * 0x10
            txn.channel = self.channel
            
            await self.start_item(txn)
            await self.finish_item(txn)
            
            print(f"[{self.get_name()}] Generated transaction {i} for channel {self.channel}: {txn}")


class VirtualSequence(uvm_sequence):
    """
    Virtual sequence coordinating multiple sequencers.
    
    Shows:
    - Virtual sequence structure
    - Multiple sequencer coordination
    - Parallel sequence execution
    - Sequence synchronization
    """
    
    def __init__(self, name="VirtualSequence"):
        super().__init__(name)
        # Virtual sequencer references (set by test)
        self.master_seqr = None
        self.slave_seqr = None
    
    async def body(self):
        """Body method - coordinate multiple sequences."""
        # Sequences don't have logger by default, use print or get logger from sequencer
        print("=" * 60)
        print(f"[{self.get_name()}] Starting virtual sequence")
        print("=" * 60)
        
        # Start sequences on different sequencers in parallel
        if self.master_seqr and self.slave_seqr:
            print("[VirtualSequence] Starting parallel sequences")
            
            # Start master sequence
            master_seq = ChannelSequence.create("master_seq")
            master_seq.channel = 0
            master_seq.num_items = 3
            master_task = cocotb.start_soon(master_seq.start(self.master_seqr))
            
            # Start slave sequence
            slave_seq = ChannelSequence.create("slave_seq")
            slave_seq.channel = 1
            slave_seq.num_items = 3
            slave_task = cocotb.start_soon(slave_seq.start(self.slave_seqr))
            
            # Wait for both to complete
            await master_task
            await slave_task
            
            print("[VirtualSequence] Parallel sequences completed")
        
        # Sequential execution example
        print("=" * 60)
        print("[VirtualSequence] Starting sequential sequences")
        
        if self.master_seqr:
            seq1 = ChannelSequence.create("seq1")
            seq1.channel = 0
            seq1.num_items = 2
            await seq1.start(self.master_seqr)
        
        if self.slave_seqr:
            seq2 = ChannelSequence.create("seq2")
            seq2.channel = 1
            seq2.num_items = 2
            await seq2.start(self.slave_seqr)
        
        print("[VirtualSequence] Sequential sequences completed")
        print("=" * 60)


class VirtualSequencer(uvm_sequencer):
    """
    Virtual sequencer containing references to multiple sequencers.
    
    Shows:
    - Virtual sequencer structure
    - Multiple sequencer references
    - Virtual sequencer implementation
    """
    
    def build_phase(self):
        """Build phase - virtual sequencer doesn't create sub-sequencers."""
        self.logger.info(f"[{self.get_name()}] Building virtual sequencer")
        # References to actual sequencers (set in connect_phase)
        self.master_seqr = None
        self.slave_seqr = None
    
    def connect_phase(self):
        """Connect phase - get references to actual sequencers."""
        self.logger.info(f"[{self.get_name()}] Connecting virtual sequencer")
        # In real implementation, get sequencer references from environment
        # self.master_seqr = self.env.master_agent.seqr
        # self.slave_seqr = self.env.slave_agent.seqr


class VirtualDriver(uvm_driver):
    """Simple driver for virtual sequence test."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building driver")
        # uvm_seq_item_pull_port should be available from pyuvm import *
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    def connect_phase(self):
        """Connect phase - connection is done by parent agent."""
        self.logger.info(f"[{self.get_name()}] Connecting driver")
        # Connection to sequencer is done by parent agent in its connect_phase
    
    async def run_phase(self):
        """Driver run phase - consume transactions."""
        self.logger.info(f"[{self.get_name()}] Starting driver run_phase")
        try:
            while True:
                txn = await self.seq_item_port.get_next_item()
                self.logger.info(f"[{self.get_name()}] Received transaction: {txn}")
                # Simulate some processing
                await Timer(1, unit="ns")
                self.seq_item_port.item_done()
        except Exception as e:
            self.logger.warning(f"[{self.get_name()}] Driver run_phase ended: {e}")


class MasterAgent(uvm_agent):
    """Master agent."""
    
    def build_phase(self):
        self.logger.info("Building MasterAgent")
        self.seqr = uvm_sequencer("sequencer", self)
        self.driver = VirtualDriver.create("driver", self)
    
    def connect_phase(self):
        self.logger.info("Connecting MasterAgent")
        if hasattr(self.driver, 'seq_item_port') and self.driver.seq_item_port:
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class SlaveAgent(uvm_agent):
    """Slave agent."""
    
    def build_phase(self):
        self.logger.info("Building SlaveAgent")
        self.seqr = uvm_sequencer("sequencer", self)
        self.driver = VirtualDriver.create("driver", self)
    
    def connect_phase(self):
        self.logger.info("Connecting SlaveAgent")
        if hasattr(self.driver, 'seq_item_port') and self.driver.seq_item_port:
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class VirtualEnv(uvm_env):
    """Environment with multiple agents and virtual sequencer."""
    
    def build_phase(self):
        self.logger.info("Building VirtualEnv")
        self.master_agent = MasterAgent.create("master_agent", self)
        self.slave_agent = SlaveAgent.create("slave_agent", self)
        self.virtual_seqr = VirtualSequencer.create("virtual_seqr", self)
    
    def connect_phase(self):
        self.logger.info("Connecting VirtualEnv")
        # Connect virtual sequencer to actual sequencers
        self.virtual_seqr.master_seqr = self.master_agent.seqr
        self.virtual_seqr.slave_seqr = self.slave_agent.seqr


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class VirtualSequenceTest(uvm_test):
    """Test demonstrating virtual sequences."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Virtual Sequence Example Test")
        self.logger.info("=" * 60)
        self.env = VirtualEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running virtual sequence test")
        
        try:
            # Create and start virtual sequence
            virtual_seq = VirtualSequence.create("virtual_seq")
            virtual_seq.master_seqr = self.env.virtual_seqr.master_seqr
            virtual_seq.slave_seqr = self.env.virtual_seqr.slave_seqr
            
            # Start the virtual sequence
            await virtual_seq.start(self.env.virtual_seqr)
            
            # Give some time for sequences to complete
            await Timer(50, unit="ns")
            
            self.logger.info("Virtual sequence test completed successfully")
        except Exception as e:
            self.logger.error(f"Virtual sequence test failed: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Virtual sequence test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_virtual_sequence(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["VirtualSequenceTest"] = VirtualSequenceTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("VirtualSequenceTest")


if __name__ == "__main__":
    print("This is a pyuvm virtual sequence example.")
    print("To run with cocotb, use the Makefile in the test directory.")

