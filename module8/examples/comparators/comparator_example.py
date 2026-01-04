"""
Module 8 Example 8.2: UVM Comparators
Demonstrates using comparators for transaction comparison in scoreboards.
"""

from pyuvm import *


class ComparatorTransaction(uvm_sequence_item):
    """Transaction for comparator example."""
    
    def __init__(self, name="ComparatorTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.timestamp = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}, addr=0x{self.address:04X}, ts={self.timestamp}"
    
    def __eq__(self, other):
        """Equality comparison for transactions."""
        if not isinstance(other, ComparatorTransaction):
            return False
        return (self.data == other.data and 
                self.address == other.address)
    
    def __hash__(self):
        """Hash for use in sets/dicts."""
        return hash((self.data, self.address))


class InOrderComparator(uvm_component):
    """
    In-order comparator for transactions.
    
    Compares transactions in the order they arrive.
    """
    
    def __init__(self, name="InOrderComparator", parent=None):
        super().__init__(name, parent)
        self.expected_ap = uvm_analysis_export("expected_ap", self)
        self.actual_ap = uvm_analysis_export("actual_ap", self)
        self.expected_imp = uvm_analysis_imp("expected_imp", self)
        self.actual_imp = uvm_analysis_imp("actual_imp", self)
        self.expected_ap.connect(self.expected_imp)
        self.actual_ap.connect(self.actual_imp)
        
        self.expected_queue = []
        self.actual_queue = []
        self.matches = 0
        self.mismatches = 0
    
    def write_expected(self, txn):
        """Receive expected transaction."""
        self.expected_queue.append(txn)
        self.logger.debug(f"[{self.get_name()}] Expected: {txn}")
        self.compare()
    
    def write_actual(self, txn):
        """Receive actual transaction."""
        self.actual_queue.append(txn)
        self.logger.debug(f"[{self.get_name()}] Actual: {txn}")
        self.compare()
    
    def compare(self):
        """Compare expected and actual transactions."""
        while len(self.expected_queue) > 0 and len(self.actual_queue) > 0:
            expected = self.expected_queue.pop(0)
            actual = self.actual_queue.pop(0)
            
            if expected == actual:
                self.matches += 1
                self.logger.info(f"[{self.get_name()}] Match: {expected}")
            else:
                self.mismatches += 1
                self.logger.error(f"[{self.get_name()}] Mismatch: expected={expected}, actual={actual}")
    
    def check_phase(self):
        """Check phase - report comparison results."""
        if len(self.expected_queue) > 0:
            self.logger.warning(f"[{self.get_name()}] {len(self.expected_queue)} expected transactions not matched")
        if len(self.actual_queue) > 0:
            self.logger.warning(f"[{self.get_name()}] {len(self.actual_queue)} actual transactions not matched")
        
        self.logger.info(f"[{self.get_name()}] Comparison results: matches={self.matches}, mismatches={self.mismatches}")


class AlgorithmicComparator(uvm_component):
    """
    Algorithmic comparator with custom comparison function.
    
    Allows flexible comparison algorithms.
    """
    
    def __init__(self, name="AlgorithmicComparator", parent=None, compare_func=None):
        super().__init__(name, parent)
        self.expected_ap = uvm_analysis_export("expected_ap", self)
        self.actual_ap = uvm_analysis_export("actual_ap", self)
        self.expected_imp = uvm_analysis_imp("expected_imp", self)
        self.actual_imp = uvm_analysis_imp("actual_imp", self)
        self.expected_ap.connect(self.expected_imp)
        self.actual_ap.connect(self.actual_imp)
        
        self.compare_func = compare_func or self.default_compare
        self.expected_dict = {}
        self.matches = 0
        self.mismatches = 0
    
    def default_compare(self, expected, actual):
        """Default comparison function."""
        return expected == actual
    
    def write_expected(self, txn):
        """Receive expected transaction."""
        key = (txn.data, txn.address)
        self.expected_dict[key] = txn
        self.logger.debug(f"[{self.get_name()}] Expected: {txn}")
    
    def write_actual(self, txn):
        """Receive actual transaction."""
        key = (txn.data, txn.address)
        if key in self.expected_dict:
            expected = self.expected_dict.pop(key)
            if self.compare_func(expected, txn):
                self.matches += 1
                self.logger.info(f"[{self.get_name()}] Match: {txn}")
            else:
                self.mismatches += 1
                self.logger.error(f"[{self.get_name()}] Mismatch: expected={expected}, actual={txn}")
        else:
            self.mismatches += 1
            self.logger.error(f"[{self.get_name()}] Unexpected transaction: {txn}")
    
    def check_phase(self):
        """Check phase - report comparison results."""
        if len(self.expected_dict) > 0:
            self.logger.warning(f"[{self.get_name()}] {len(self.expected_dict)} expected transactions not matched")
        
        self.logger.info(f"[{self.get_name()}] Comparison results: matches={self.matches}, mismatches={self.mismatches}")


class ComparatorScoreboard(uvm_scoreboard):
    """Scoreboard using comparator."""
    
    def build_phase(self):
        self.logger.info("Building Comparator Scoreboard")
        # Choose comparator type
        self.use_algorithmic = ConfigDB().get(None, "", "use_algorithmic_comparator", False)
        
        if self.use_algorithmic:
            self.comparator = AlgorithmicComparator.create("comparator", self)
        else:
            self.comparator = InOrderComparator.create("comparator", self)
        
        self.expected_ap = uvm_analysis_port("expected_ap", self)
        self.actual_ap = uvm_analysis_port("actual_ap", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Comparator Scoreboard")
        self.expected_ap.connect(self.comparator.expected_ap)
        self.actual_ap.connect(self.comparator.actual_ap)
    
    def write_expected(self, txn):
        """Write expected transaction."""
        self.expected_ap.write(txn)
    
    def write_actual(self, txn):
        """Write actual transaction."""
        self.actual_ap.write(txn)


class ComparatorEnv(uvm_env):
    """Environment demonstrating comparator usage."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Comparator Environment")
        self.logger.info("=" * 60)
        self.scoreboard = ComparatorScoreboard.create("scoreboard", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Comparator Environment")


@uvm_test()
class ComparatorTest(uvm_test):
    """Test demonstrating comparator usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Comparator Example Test")
        self.logger.info("=" * 60)
        self.env = ComparatorEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running comparator test")
        
        # Generate expected transactions
        for i in range(5):
            txn = ComparatorTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            self.env.scoreboard.write_expected(txn)
        
        # Generate actual transactions (matching)
        for i in range(5):
            txn = ComparatorTransaction()
            txn.data = i * 0x10
            txn.address = i * 0x100
            self.env.scoreboard.write_actual(txn)
        
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Comparator test completed")
        self.logger.info("=" * 60)


if __name__ == "__main__":
    print("This is a pyuvm comparator example.")
    print("To run with cocotb, use the Makefile in the test directory.")

