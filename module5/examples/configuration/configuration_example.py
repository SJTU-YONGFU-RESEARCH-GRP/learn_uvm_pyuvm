"""
Module 5 Example 5.3: Complex Configuration Objects
Demonstrates configuration object design and hierarchy.
"""

from pyuvm import *
import cocotb
from cocotb.triggers import Timer


class AgentConfig(uvm_object):
    """
    Configuration object for agent.
    
    Shows:
    - Configuration class design
    - Configuration fields
    - Configuration methods
    - Configuration validation
    """
    
    def __init__(self, name="AgentConfig"):
        super().__init__(name)
        self.active = True
        self.has_coverage = False
        self.address_width = 32
        self.data_width = 8
        self.max_outstanding = 4
    
    def __str__(self):
        return (f"active={self.active}, has_coverage={self.has_coverage}, "
                f"addr_width={self.address_width}, data_width={self.data_width}, "
                f"max_outstanding={self.max_outstanding}")
    
    def validate(self):
        """Validate configuration."""
        if self.address_width not in [16, 32, 64]:
            self.logger.error(f"Invalid address_width: {self.address_width}")
            return False
        if self.data_width not in [8, 16, 32, 64]:
            self.logger.error(f"Invalid data_width: {self.data_width}")
            return False
        if self.max_outstanding < 1:
            self.logger.error(f"Invalid max_outstanding: {self.max_outstanding}")
            return False
        return True


class EnvConfig(uvm_object):
    """
    Environment configuration object.
    
    Shows:
    - Hierarchical configuration
    - Configuration composition
    - Configuration inheritance
    """
    
    def __init__(self, name="EnvConfig"):
        super().__init__(name)
        self.num_agents = 2
        self.master_config = AgentConfig("master_config")
        self.slave_config = AgentConfig("slave_config")
        self.enable_scoreboard = True
        self.enable_coverage = True
    
    def __str__(self):
        return (f"num_agents={self.num_agents}, "
                f"master_config={self.master_config}, "
                f"slave_config={self.slave_config}, "
                f"enable_scoreboard={self.enable_scoreboard}, "
                f"enable_coverage={self.enable_coverage}")
    
    def validate(self):
        """Validate environment configuration."""
        if not self.master_config.validate():
            return False
        if not self.slave_config.validate():
            return False
        if self.num_agents < 1:
            self.logger.error(f"Invalid num_agents: {self.num_agents}")
            return False
        return True


class ConfigurableAgent(uvm_agent):
    """Agent that uses configuration object."""
    
    def build_phase(self):
        """Build phase - get configuration."""
        self.logger.info(f"[{self.get_name()}] Building configurable agent")
        
        # Get configuration from ConfigDB
        config = None
        success = ConfigDB().get(None, "", f"{self.get_full_name()}.config", config)
        
        if success and config is not None:
            self.logger.info(f"[{self.get_name()}] Got config: {config}")
            self.config = config
        else:
            self.logger.warning(f"[{self.get_name()}] No config found, using defaults")
            self.config = AgentConfig()
        
        # Validate configuration
        if not self.config.validate():
            self.logger.error(f"[{self.get_name()}] Configuration validation failed")
        
        # Use configuration
        if self.config.active:
            self.logger.info(f"[{self.get_name()}] Agent is ACTIVE")
        else:
            self.logger.info(f"[{self.get_name()}] Agent is PASSIVE")


class ConfigurableEnv(uvm_env):
    """Environment using configuration objects."""
    
    def build_phase(self):
        """Build phase - set and use configuration."""
        self.logger.info("Building ConfigurableEnv")
        
        # Create environment configuration
        env_config = EnvConfig("env_config")
        env_config.num_agents = 2
        env_config.master_config.active = True
        env_config.master_config.has_coverage = True
        env_config.slave_config.active = False
        env_config.slave_config.has_coverage = False
        
        # Validate configuration
        if not env_config.validate():
            self.logger.error("Environment configuration validation failed")
        
        # Set configuration in ConfigDB
        ConfigDB().set(None, "", "env.config", env_config)
        ConfigDB().set(None, "", "env.master_agent.config", env_config.master_config)
        ConfigDB().set(None, "", "env.slave_agent.config", env_config.slave_config)
        
        self.logger.info(f"Set environment configuration: {env_config}")
        
        # Create agents (will get config from ConfigDB)
        self.master_agent = ConfigurableAgent.create("master_agent", self)
        self.slave_agent = ConfigurableAgent.create("slave_agent", self)
    
    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting ConfigurableEnv")


# Note: @uvm_test() decorator removed to avoid import-time TypeError
# Using cocotb test wrapper instead for compatibility with cocotb test discovery
class ConfigurationTest(uvm_test):
    """Test demonstrating configuration objects."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Configuration Example Test")
        self.logger.info("=" * 60)
        self.env = ConfigurableEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running configuration test")
        
        # Demonstrate configuration hierarchy
        self.logger.info("=" * 60)
        self.logger.info("Configuration Hierarchy:")
        self.logger.info(f"  Environment config: {self.env.config if hasattr(self.env, 'config') else 'N/A'}")
        self.logger.info(f"  Master agent config: {self.env.master_agent.config}")
        self.logger.info(f"  Slave agent config: {self.env.slave_agent.config}")
        
        await Timer(10, unit="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Configuration test completed")
        self.logger.info("=" * 60)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_configuration(dut):
    """Cocotb test wrapper for pyuvm test."""
    # Register the test class with uvm_root so run_test can find it
    if not hasattr(uvm_root(), 'm_uvm_test_classes'):
        uvm_root().m_uvm_test_classes = {}
    uvm_root().m_uvm_test_classes["ConfigurationTest"] = ConfigurationTest
    # Use uvm_root to run the test properly (executes all phases in hierarchy)
    await uvm_root().run_test("ConfigurationTest")


if __name__ == "__main__":
    print("This is a pyuvm configuration example.")
    print("To run with cocotb, use the Makefile in the test directory.")

