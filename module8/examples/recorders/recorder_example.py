"""
Module 8 Example 8.3: UVM Recorders
Demonstrates transaction recording for analysis.
"""

from pyuvm import *
import json
from datetime import datetime


class RecorderTransaction(uvm_sequence_item):
    """Transaction for recorder example."""
    
    def __init__(self, name="RecorderTransaction"):
        super().__init__(name)
        self.data = 0
        self.address = 0
        self.timestamp = 0
        self.transaction_id = 0
    
    def __str__(self):
        return f"id={self.transaction_id}, data=0x{self.data:02X}, addr=0x{self.address:04X}, ts={self.timestamp}"
    
    def to_dict(self):
        """Convert transaction to dictionary for recording."""
        return {
            'transaction_id': self.transaction_id,
            'data': hex(self.data),
            'address': hex(self.address),
            'timestamp': self.timestamp
        }


class TextRecorder(uvm_component):
    """
    Text recorder for transactions.
    
    Records transactions to a text file.
    """
    
    def __init__(self, name="TextRecorder", parent=None, filename="transactions.txt"):
        super().__init__(name, parent)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.filename = filename
        self.recorded_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Text Recorder (file: {self.filename})")
        # Open file for writing
        self.file = open(self.filename, 'w')
        self.file.write(f"Transaction Recording Started: {datetime.now()}\n")
        self.file.write("=" * 60 + "\n")
    
    def write(self, txn):
        """Record transaction."""
        self.recorded_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.file.write(f"[{timestamp}] {txn}\n")
        self.logger.debug(f"[{self.get_name()}] Recorded: {txn}")
    
    def report_phase(self):
        """Report phase - close file."""
        self.file.write("=" * 60 + "\n")
        self.file.write(f"Transaction Recording Ended: {datetime.now()}\n")
        self.file.write(f"Total transactions recorded: {self.recorded_count}\n")
        self.file.close()
        self.logger.info(f"[{self.get_name()}] Recorded {self.recorded_count} transactions to {self.filename}")


class JSONRecorder(uvm_component):
    """
    JSON recorder for transactions.
    
    Records transactions to a JSON file.
    """
    
    def __init__(self, name="JSONRecorder", parent=None, filename="transactions.json"):
        super().__init__(name, parent)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.filename = filename
        self.transactions = []
        self.recorded_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building JSON Recorder (file: {self.filename})")
        self.start_time = datetime.now()
    
    def write(self, txn):
        """Record transaction."""
        self.recorded_count += 1
        record = txn.to_dict() if hasattr(txn, 'to_dict') else {'transaction': str(txn)}
        record['record_time'] = datetime.now().isoformat()
        self.transactions.append(record)
        self.logger.debug(f"[{self.get_name()}] Recorded: {txn}")
    
    def report_phase(self):
        """Report phase - write JSON file."""
        end_time = datetime.now()
        recording_data = {
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_transactions': self.recorded_count,
            'transactions': self.transactions
        }
        
        with open(self.filename, 'w') as f:
            json.dump(recording_data, f, indent=2)
        
        self.logger.info(f"[{self.get_name()}] Recorded {self.recorded_count} transactions to {self.filename}")


class TransactionDatabase(uvm_component):
    """
    Transaction database for storing and querying transactions.
    
    In-memory database for transaction analysis.
    """
    
    def __init__(self, name="TransactionDatabase", parent=None):
        super().__init__(name, parent)
        self.ap = uvm_analysis_export("ap", self)
        self.imp = uvm_analysis_imp("imp", self)
        self.ap.connect(self.imp)
        self.database = []
        self.recorded_count = 0
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building Transaction Database")
    
    def write(self, txn):
        """Store transaction in database."""
        self.recorded_count += 1
        record = {
            'id': self.recorded_count,
            'transaction': txn.to_dict() if hasattr(txn, 'to_dict') else {'data': str(txn)},
            'timestamp': datetime.now().isoformat()
        }
        self.database.append(record)
        self.logger.debug(f"[{self.get_name()}] Stored: {txn}")
    
    def query(self, filter_func=None):
        """Query database with optional filter."""
        if filter_func:
            return [r for r in self.database if filter_func(r)]
        return self.database
    
    def report_phase(self):
        """Report phase - show database statistics."""
        self.logger.info(f"[{self.get_name()}] Database contains {len(self.database)} transactions")
        if len(self.database) > 0:
            self.logger.info(f"  First transaction: {self.database[0]['transaction']}")
            self.logger.info(f"  Last transaction: {self.database[-1]['transaction']}")


class RecorderEnv(uvm_env):
    """Environment demonstrating recorder usage."""
    
    def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Building Recorder Environment")
        self.logger.info("=" * 60)
        
        # Create multiple recorders
        self.text_recorder = TextRecorder.create("text_recorder", self, "transactions.txt")
        self.json_recorder = JSONRecorder.create("json_recorder", self, "transactions.json")
        self.database = TransactionDatabase.create("database", self)
        
        self.ap = uvm_analysis_port("ap", self)
    
    def connect_phase(self):
        self.logger.info("Connecting Recorder Environment")
        # Connect to all recorders
        self.ap.connect(self.text_recorder.ap)
        self.ap.connect(self.json_recorder.ap)
        self.ap.connect(self.database.ap)


@uvm_test()
class RecorderTest(uvm_test):
    """Test demonstrating recorder usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Recorder Example Test")
        self.logger.info("=" * 60)
        self.env = RecorderEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running recorder test")
        
        # Generate and record transactions
        for i in range(10):
            txn = RecorderTransaction()
            txn.transaction_id = i
            txn.data = i * 0x10
            txn.address = i * 0x100
            txn.timestamp = i * 10
            
            self.env.ap.write(txn)
            await Timer(10, units="ns")
        
        await Timer(50, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("Recorder test completed")
        self.logger.info("=" * 60)
        self.logger.info("Check generated files:")
        self.logger.info("  - transactions.txt (text format)")
        self.logger.info("  - transactions.json (JSON format)")


if __name__ == "__main__":
    print("This is a pyuvm recorder example.")
    print("To run with cocotb, use the Makefile in the test directory.")

