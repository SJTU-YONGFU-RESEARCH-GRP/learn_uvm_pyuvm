"""
Module 3 Example 3.4: UVM ConfigDB
Demonstrates UVM configuration database usage.
"""

import cocotb
from cocotb.triggers import Timer
from pyuvm import *


class AgentConfig(uvm_object):
    """
    Configuration object for agent.
    """
    
    def __init__(self, name="AgentConfig"):
        super().__init__(name)
        self.active = True
        self.has_coverage = False
        self.address_width = 32
        self.data_width = 8


class ConfigurableAgent(uvm_agent):
    """
    Agent that uses ConfigDB for configuration.
    """
    
    def build_phase(self):
        """Build phase - get configuration from ConfigDB."""
        self.logger.info(f"[{self.get_name()}] Building agent")
        
        # Get configuration from ConfigDB
        config = None
        success = ConfigDB().get(None, "", "agent_config", config)
        
        if success and config is not None:
            self.logger.info(f"  Got config: active={config.active}, "
                           f"has_coverage={config.has_coverage}")
            self.active = config.active
            self.has_coverage = config.has_coverage
        else:
            self.logger.warning("  No config found, using defaults")
            self.active = True
            self.has_coverage = False
        
        # Get scalar configuration
        address_width = 32
        success = ConfigDB().get(None, "", "address_width", address_width)
        if success:
            self.logger.info(f"  Got address_width: {address_width}")
        else:
            self.logger.info(f"  Using default address_width: {address_width}")


class ConfigurableEnv(uvm_env):
    """
    Environment that sets configuration in ConfigDB.
    """
    
    def build_phase(self):
        """Build phase - set configuration in ConfigDB."""
        self.logger.info("Building ConfigurableEnv")
        
        # Create and set configuration object
        agent_config = AgentConfig("agent_config")
        agent_config.active = True
        agent_config.has_coverage = True
        agent_config.address_width = 16
        agent_config.data_width = 8
        
        ConfigDB().set(None, "", "agent_config", agent_config)
        self.logger.info("Set agent_config in ConfigDB")
        
        # Set scalar configuration
        ConfigDB().set(None, "", "address_width", 16)
        ConfigDB().set(None, "", "data_width", 8)
        self.logger.info("Set scalar configs in ConfigDB")
        
        # Create agent (will get config from ConfigDB)
        self.agent = ConfigurableAgent.create("agent", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting ConfigurableEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class ConfigDBTest(uvm_test):
    """
    Test demonstrating ConfigDB usage.
    """
    
    async def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB Example")
        self.logger.info("=" * 60)
        self.env = ConfigurableEnv.create("env", self)
    
    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        self.logger.info("Running ConfigDBTest")
        
        # Demonstrate hierarchical configuration
        self.logger.info("=" * 60)
        self.logger.info("Hierarchical Configuration Example:")
        
        # Set config at test level
        ConfigDB().set(self, "env.agent", "test_config", "test_value")
        self.logger.info("Set config at test level for env.agent")
        
        # Get config (would be done in agent)
        test_value = None
        success = ConfigDB().get(self, "env.agent", "test_config", test_value)
        if success:
            self.logger.info(f"Got config: {test_value}")
        
        await Timer(10, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB test completed")
        self.logger.info("=" * 60)


# Note: @uvm_test() decorator removed to avoid import-time TypeError
class ConfigDBHierarchyTest(uvm_test):
    """
    Test demonstrating ConfigDB hierarchy.
    """
    
    async def build_phase(self):
        """Build phase - demonstrate configuration hierarchy."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB Hierarchy Example")
        self.logger.info("=" * 60)
        
        # Set configuration at different levels
        ConfigDB().set(None, "", "global_config", "global_value")
        ConfigDB().set(self, "", "test_config", "test_value")
        ConfigDB().set(self, "env", "env_config", "env_value")
        
        self.logger.info("Set configurations at different hierarchy levels")
        
        # Create environment
        self.env = ConfigurableEnv.create("env", self)
    
    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        
        # Demonstrate configuration lookup
        self.logger.info("=" * 60)
        self.logger.info("Configuration Lookup:")
        
        # Lookup at different levels
        global_val = None
        if ConfigDB().get(None, "", "global_config", global_val):
            self.logger.info(f"  Global config: {global_val}")
        
        test_val = None
        if ConfigDB().get(self, "", "test_config", test_val):
            self.logger.info(f"  Test config: {test_val}")
        
        env_val = None
        if ConfigDB().get(self, "env", "env_config", env_val):
            self.logger.info(f"  Env config: {env_val}")
        
        await Timer(10, unit="ns")
        self.drop_objection()


# Cocotb test functions to run the pyuvm tests
@cocotb.test()
async def test_configdb(dut):
    """Cocotb test wrapper for ConfigDBTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ConfigDBTest"] = ConfigDBTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ConfigDBTest")

@cocotb.test()
async def test_configdb_hierarchy(dut):
    """Cocotb test wrapper for ConfigDBHierarchyTest."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ConfigDBHierarchyTest"] = ConfigDBHierarchyTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ConfigDBHierarchyTest")

if __name__ == "__main__":
    print("This is a pyuvm ConfigDB example.")
    print("To run with cocotb, use the Makefile in the test directory.")

