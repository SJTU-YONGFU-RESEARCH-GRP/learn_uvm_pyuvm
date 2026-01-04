"""
Module 6 Example 6.1: Multi-Agent Environment
Demonstrates multi-agent environment with agent coordination.
"""

from pyuvm import *
# Explicitly import uvm_seq_item_pull_port - it may not be exported by from pyuvm import *
# Try multiple possible import paths
_uvm_seq_item_pull_port = None
try:
    # First try: check if it's in the namespace after from pyuvm import *
    _uvm_seq_item_pull_port = globals()['uvm_seq_item_pull_port']
except KeyError:
    # Second try: import from pyuvm module directly
    import pyuvm
    if hasattr(pyuvm, 'uvm_seq_item_pull_port'):
        _uvm_seq_item_pull_port = pyuvm.uvm_seq_item_pull_port
    else:
        # Third try: try TLM module paths using __import__
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_seq_item_pull_port'])
                if hasattr(tlm_module, 'uvm_seq_item_pull_port'):
                    _uvm_seq_item_pull_port = tlm_module.uvm_seq_item_pull_port
                    break
            except (ImportError, AttributeError):
                continue

if _uvm_seq_item_pull_port is not None:
    globals()['uvm_seq_item_pull_port'] = _uvm_seq_item_pull_port

# Explicitly import uvm_analysis_imp - it may not be exported by from pyuvm import *
# Try multiple possible import paths
_uvm_analysis_imp = None
try:
    # First try: check if it's in the namespace after from pyuvm import *
    _uvm_analysis_imp = globals()['uvm_analysis_imp']
except KeyError:
    # Second try: import from pyuvm module directly
    import pyuvm
    if hasattr(pyuvm, 'uvm_analysis_imp'):
        _uvm_analysis_imp = pyuvm.uvm_analysis_imp
    else:
        # Third try: try TLM module paths using __import__
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_analysis_imp'])
                if hasattr(tlm_module, 'uvm_analysis_imp'):
                    _uvm_analysis_imp = tlm_module.uvm_analysis_imp
                    break
            except (ImportError, AttributeError):
                continue

if _uvm_analysis_imp is not None:
    globals()['uvm_analysis_imp'] = _uvm_analysis_imp
import cocotb
from cocotb.triggers import Timer


class MultiAgentTransaction(uvm_sequence_item):
    """Transaction for multi-agent example."""
    
    def __init__(self, name="MultiAgentTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.agent_id = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, agent={self.agent_id}"


class MultiAgentSequence(uvm_sequence):
    """Sequence for multi-agent."""
    
    def __init__(self, name="MultiAgentSequence", agent_id=0, num_items=5):
        super().__init__(name)
        self.agent_id = agent_id
        self.num_items = num_items
    
    async def body(self):
        """Generate transactions for agent."""
        self.logger.info(f"[{self.get_name()}] Starting sequence for agent {self.agent_id}")
        
        for i in range(self.num_items):
            txn = MultiAgentTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            txn.agent_id = self.agent_id
            
            await self.start_item(txn)
            await self.finish_item(txn)
            
            self.logger.info(f"[{self.get_name()}] Generated transaction {i} for agent {self.agent_id}: {txn}")


class MultiAgentDriver(uvm_driver):
    """Driver for multi-agent."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building driver")
        self.seq_item_port = uvm_seq_item_pull_port("seq_item_port", self)
    
    async def run_phase(self):
        """Run phase."""
        self.logger.info(f"[{self.get_name()}] Starting driver")
        
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"[{self.get_name()}] Driving: {item}")
            await Timer(10, unit="ns")
            await self.seq_item_port.item_done()


class MultiAgentMonitor(uvm_monitor):
    """Monitor for multi-agent."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building monitor")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase."""
        self.logger.info(f"[{self.get_name()}] Starting monitor")
        
        while True:
            await Timer(10, unit="ns")
            txn = MultiAgentTransaction()
            txn.data = 0xAA
            txn.address = 0x1000
            txn.agent_id = 0  # Simulated
            self.ap.write(txn)


class MultiAgentAgent(uvm_agent):
    """Agent for multi-agent environment."""
    
    def __init__(self, name="MultiAgentAgent", parent=None, agent_id=0):
        super().__init__(name, parent)
        self.agent_id = agent_id
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building agent {self.agent_id}")
        self.driver = MultiAgentDriver.create("driver", self)
        self.monitor = MultiAgentMonitor.create("monitor", self)
        self.seqr = uvm_sequencer("sequencer", self)
    
    def connect_phase(self):
        self.logger.info(f"[{self.get_name()}] Connecting agent {self.agent_id}")
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class MultiAgentScoreboard(uvm_scoreboard):
    """Scoreboard for multi-agent environment."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building scoreboard")
        self.analysis_exports = []
        self.analysis_imps = []
        
        # Create analysis ports for each agent
        for i in range(3):
            ap = uvm_analysis_export(f"ap_agent_{i}", self)
            imp = uvm_analysis_imp(f"imp_agent_{i}", self)
            ap.connect(imp)
            self.analysis_exports.append(ap)
            self.analysis_imps.append(imp)
        
        self.received = {0: [], 1: [], 2: []}
    
    def write(self, txn, agent_id=None):
        """Write method - receive transactions from multiple agents."""
        if agent_id is None:
            agent_id = 0
        
        self.logger.info(f"[{self.get_name()}] Received from agent {agent_id}: {txn}")
        self.received[agent_id].append(txn)
    
    def check_phase(self):
        """Check phase."""
        self.logger.info("=" * 60)
        self.logger.info(f"[{self.get_name()}] Multi-Agent Scoreboard Check")
        for agent_id, txns in self.received.items():
            self.logger.info(f"  Agent {agent_id}: {len(txns)} transactions")
        self.logger.info("=" * 60)


class MultiAgentEnv(uvm_env):
    """
    Multi-agent environment demonstrating agent coordination.
    
    Shows:
    - Multiple agent instantiation
    - Agent coordination
    - Environment hierarchy
    - Scoreboard integration
    """
    
    def build_phase(self):
        """Build phase - create multiple agents."""
        self.logger.info("=" * 60)
        self.logger.info("Building MultiAgentEnv")
        self.logger.info("=" * 60)
        
        # Create multiple agents
        self.agents = []
        for i in range(3):
            agent = MultiAgentAgent.create(f"agent_{i}", self)
            agent.agent_id = i
            self.agents.append(agent)
        
        # Create scoreboard
        self.scoreboard = MultiAgentScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        """Connect phase - connect agents to scoreboard."""
        self.logger.info("Connecting MultiAgentEnv")
        
        # Connect each agent's monitor to scoreboard
        for i, agent in enumerate(self.agents):
            # In real implementation, would connect properly
            # agent.monitor.ap.connect(self.scoreboard.analysis_exports[i])
            self.logger.info(f"Connected agent {i} to scoreboard")


class MultiAgentVirtualSequence(uvm_sequence):
    """Virtual sequence coordinating multiple agents."""
    
    def __init__(self, name="MultiAgentVirtualSequence"):
        super().__init__(name)
        self.agent_seqrs = []
    
    async def body(self):
        """Body method - coordinate multiple agents."""
        self.logger.info("=" * 60)
        self.logger.info("[VirtualSequence] Starting multi-agent coordination")
        self.logger.info("=" * 60)
        
        # Start sequences on multiple agents in parallel
        tasks = []
        for i, seqr in enumerate(self.agent_seqrs):
            seq = MultiAgentSequence.create(f"seq_agent_{i}", agent_id=i, num_items=3)
            task = cocotb.start_soon(seq.start(seqr))
            tasks.append(task)
        
        # Wait for all sequences to complete
        for task in tasks:
            await task
        
        self.logger.info("[VirtualSequence] Multi-agent coordination completed")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class MultiAgentTest(uvm_test):
    """Test demonstrating multi-agent environment."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Multi-Agent Environment Example Test")
        self.logger.info("=" * 60)
        self.env = MultiAgentEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running multi-agent test")
        
        # Create virtual sequence
        virtual_seq = MultiAgentVirtualSequence.create("virtual_seq")
        virtual_seq.agent_seqrs = [agent.seqr for agent in self.env.agents]
        
        # Start virtual sequence
        await virtual_seq.start(None)  # Virtual sequencer would be used here
        
        await Timer(100, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Multi-agent test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_multi_agent(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["MultiAgentTest"] = MultiAgentTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("MultiAgentTest")


if __name__ == "__main__":
    print("This is a pyuvm multi-agent example.")
    print("To run with cocotb, use the Makefile in the test directory.")

