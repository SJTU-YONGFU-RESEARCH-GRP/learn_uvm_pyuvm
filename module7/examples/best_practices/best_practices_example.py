"""
Module 7 Example: Best Practices
Demonstrates code organization, documentation, and best practices.
"""

from pyuvm import *


class BestPracticesTransaction(uvm_sequence_item):
    """
    Transaction class demonstrating best practices.
    
    Best Practices:
    - Clear class name
    - Comprehensive docstring
    - Type hints (in real code)
    - Clear field names
    - __str__ method for debugging
    """
    
    def __init__(self, name="BestPracticesTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}"


class BestPracticesComponent(uvm_component):
    """
    Component demonstrating best practices.
    
    Best Practices:
    - Clear component name
    - Comprehensive docstring
    - Organized methods
    - Clear logging
    - Error handling
    """
    
    def build_phase(self):
        """
        Build phase with clear documentation.
        
        Best Practices:
        - Document what is built
        - Use clear variable names
        - Organize code logically
        """
        self.logger.info(f"[{self.get_name()}] Building component (best practices)")
        self.ap = uvm_analysis_port("ap", self)
    
    def connect_phase(self):
        """
        Connect phase with clear documentation.
        
        Best Practices:
        - Document connections
        - Verify connections
        - Handle errors
        """
        self.logger.info(f"[{self.get_name()}] Connecting component (best practices)")
    
    async def run_phase(self):
        """
        Run phase with clear documentation.
        
        Best Practices:
        - Document run phase behavior
        - Use clear control flow
        - Handle exceptions
        """
        self.logger.info(f"[{self.get_name()}] Running component (best practices)")
        await Timer(10, units="ns")
    
    def check_phase(self):
        """
        Check phase with clear documentation.
        
        Best Practices:
        - Document what is checked
        - Report results clearly
        - Handle errors gracefully
        """
        self.logger.info(f"[{self.get_name()}] Checking component (best practices)")
    
    def report_phase(self):
        """
        Report phase with clear documentation.
        
        Best Practices:
        - Generate clear reports
        - Include statistics
        - Format output clearly
        """
        self.logger.info(f"[{self.get_name()}] Reporting component (best practices)")


class ReusableComponent(uvm_component):
    """
    Reusable component demonstrating reusability patterns.
    
    Best Practices for Reusability:
    - Parameterization
    - Configuration support
    - Clear interfaces
    - Documentation
    - Example usage
    """
    
    def __init__(self, name="ReusableComponent", parent=None, config=None):
        """
        Initialize reusable component.
        
        Args:
            name: Component name
            parent: Parent component
            config: Configuration dictionary
        """
        super().__init__(name, parent)
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.mode = self.config.get('mode', 'normal')
    
    def build_phase(self):
        """Build phase - use configuration."""
        self.logger.info(f"[{self.get_name()}] Building reusable component")
        self.logger.info(f"  Configuration: enabled={self.enabled}, mode={self.mode}")
        self.ap = uvm_analysis_port("ap", self)
    
    async def run_phase(self):
        """Run phase - component operation."""
        if self.enabled:
            self.logger.info(f"[{self.get_name()}] Running in {self.mode} mode")
            await Timer(10, units="ns")


class WellOrganizedEnv(uvm_env):
    """
    Environment demonstrating code organization.
    
    Best Practices for Organization:
    - Clear structure
    - Logical grouping
    - Clear naming
    - Documentation
    """
    
    def build_phase(self):
        """
        Build phase - demonstrate organization.
        
        Organization:
        1. Create agents
        2. Create scoreboards
        3. Create coverage
        4. Create other components
        """
        self.logger.info("=" * 60)
        self.logger.info("Building Well-Organized Environment")
        self.logger.info("=" * 60)
        
        # Group 1: Agents
        self.agent = BestPracticesComponent.create("agent", self)
        
        # Group 2: Analysis components
        self.reusable_comp = ReusableComponent.create(
            "reusable_comp", 
            self, 
            config={'enabled': True, 'mode': 'normal'}
        )
    
    def connect_phase(self):
        """
        Connect phase - demonstrate organization.
        
        Organization:
        1. Connect agents
        2. Connect analysis ports
        3. Connect other connections
        """
        self.logger.info("Connecting Well-Organized Environment")
        # Connections here


@uvm_test()
class BestPracticesTest(uvm_test):
    """
    Test demonstrating best practices.
    
    Best Practices:
    - Clear test name
    - Comprehensive docstring
    - Organized test flow
    - Clear reporting
    """
    
    async def build_phase(self):
        """
        Build phase - demonstrate best practices.
        
        Best Practices:
        - Clear phase documentation
        - Organized component creation
        - Clear logging
        """
        self.logger.info("=" * 60)
        self.logger.info("Best Practices Example Test")
        self.logger.info("=" * 60)
        self.env = WellOrganizedEnv.create("env", self)
    
    async def run_phase(self):
        """
        Run phase - demonstrate best practices.
        
        Best Practices:
        - Clear test flow
        - Proper objection handling
        - Clear logging
        """
        self.raise_objection()
        self.logger.info("Running best practices test")
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        """
        Report phase - demonstrate best practices.
        
        Best Practices:
        - Clear reporting
        - Summary statistics
        - Clear formatting
        """
        self.logger.info("=" * 60)
        self.logger.info("Best practices test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm best practices example.")
    print("To run with cocotb, use the Makefile in the test directory.")

