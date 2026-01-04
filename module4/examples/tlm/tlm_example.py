"""
Module 4 Example: TLM (Transaction-Level Modeling)
Demonstrates TLM interfaces, ports, exports, and implementations.
"""

from pyuvm import *
# Explicitly import TLM classes - they may not be exported by from pyuvm import *
# Try multiple possible import paths

# Import uvm_put_imp
_uvm_put_imp = None
try:
    _uvm_put_imp = globals()['uvm_put_imp']
except KeyError:
    import pyuvm
    if hasattr(pyuvm, 'uvm_put_imp'):
        _uvm_put_imp = pyuvm.uvm_put_imp
    else:
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_put_imp'])
                if hasattr(tlm_module, 'uvm_put_imp'):
                    _uvm_put_imp = tlm_module.uvm_put_imp
                    break
            except (ImportError, AttributeError):
                continue
if _uvm_put_imp is not None:
    globals()['uvm_put_imp'] = _uvm_put_imp

# Import uvm_get_imp
_uvm_get_imp = None
try:
    _uvm_get_imp = globals()['uvm_get_imp']
except KeyError:
    import pyuvm
    if hasattr(pyuvm, 'uvm_get_imp'):
        _uvm_get_imp = pyuvm.uvm_get_imp
    else:
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_get_imp'])
                if hasattr(tlm_module, 'uvm_get_imp'):
                    _uvm_get_imp = tlm_module.uvm_get_imp
                    break
            except (ImportError, AttributeError):
                continue
if _uvm_get_imp is not None:
    globals()['uvm_get_imp'] = _uvm_get_imp

# Import uvm_peek_imp
_uvm_peek_imp = None
try:
    _uvm_peek_imp = globals()['uvm_peek_imp']
except KeyError:
    import pyuvm
    if hasattr(pyuvm, 'uvm_peek_imp'):
        _uvm_peek_imp = pyuvm.uvm_peek_imp
    else:
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_peek_imp'])
                if hasattr(tlm_module, 'uvm_peek_imp'):
                    _uvm_peek_imp = tlm_module.uvm_peek_imp
                    break
            except (ImportError, AttributeError):
                continue
if _uvm_peek_imp is not None:
    globals()['uvm_peek_imp'] = _uvm_peek_imp

# Import uvm_transport_imp
_uvm_transport_imp = None
try:
    _uvm_transport_imp = globals()['uvm_transport_imp']
except KeyError:
    import pyuvm
    if hasattr(pyuvm, 'uvm_transport_imp'):
        _uvm_transport_imp = pyuvm.uvm_transport_imp
    else:
        for module_name in ['s15_uvm_tlm_1', 's15_uvm_tlm', 's16_uvm_tlm_1', 's16_uvm_tlm']:
            try:
                tlm_module = __import__(f'pyuvm.{module_name}', fromlist=['uvm_transport_imp'])
                if hasattr(tlm_module, 'uvm_transport_imp'):
                    _uvm_transport_imp = tlm_module.uvm_transport_imp
                    break
            except (ImportError, AttributeError):
                continue
if _uvm_transport_imp is not None:
    globals()['uvm_transport_imp'] = _uvm_transport_imp

import cocotb
from cocotb.triggers import Timer


class TLMTransaction(uvm_sequence_item):
    """Transaction for TLM examples."""
    
    def __init__(self, name="TLMTransaction"):
        super().__init__(name)
        self.data = 0
    
    def __str__(self):
        return f"data=0x{self.data:02X}"


# TLM Put Interface Example
class PutProducer(uvm_component):
    """Component using put port to send transactions."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building PutProducer")
        self.put_port = uvm_put_port("put_port", self)
    
    async def run_phase(self):
        """Run phase - produce transactions."""
        self.raise_objection()
        self.logger.info(f"[{self.get_name()}] Starting producer")
        
        for i in range(5):
            txn = TLMTransaction()
            txn.data = i * 0x10
            self.logger.info(f"[{self.get_name()}] Producing: {txn}")
            await self.put_port.put(txn)
            self.logger.info(f"[{self.get_name()}] Put transaction: {txn}")
        
        self.drop_objection()


class PutConsumer(uvm_put_export):
    """Component using put export to receive transactions."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building PutConsumer")
    
    async def put(self, txn):
        """Put implementation method."""
        self.logger.info(f"[{self.get_name()}] Received via put: {txn}")
        await Timer(5, units="ns")

    async def try_put(self, txn):
        """Try put implementation method."""
        await self.put(txn)
        return True

    def can_put(self):
        """Can put implementation method."""
        return True


# TLM Get Interface Example
class GetProducer(uvm_get_export):
    """Component using get export to provide transactions."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building GetProducer")
        self.transactions = []
        for i in range(5):
            txn = TLMTransaction()
            txn.data = i * 0x20
            self.transactions.append(txn)
        self.index = 0
    
    async def get(self):
        """Get implementation method."""
        if self.index < len(self.transactions):
            txn = self.transactions[self.index]
            self.index += 1
            self.logger.info(f"[{self.get_name()}] Providing via get: {txn}")
            await Timer(5, units="ns")
            return txn
        return None

    async def try_get(self):
        """Try get implementation method."""
        return await self.get()

    def can_get(self):
        """Can get implementation method."""
        return self.index < len(self.transactions)


class GetConsumer(uvm_component):
    """Component using get port to receive transactions."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building GetConsumer")
        self.get_port = uvm_get_port("get_port", self)
    
    async def run_phase(self):
        """Run phase - consume transactions."""
        self.raise_objection()
        self.logger.info(f"[{self.get_name()}] Starting consumer")
        
        for i in range(5):
            txn = await self.get_port.get()
            if txn:
                self.logger.info(f"[{self.get_name()}] Got transaction: {txn}")
        
        self.drop_objection()


# TLM Transport Interface Example
class TransportComponent(uvm_transport_export):
    """Component using transport interface."""

    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building TransportComponent")
        # Create transport port and connect it to ourselves (since we inherit from export)
        self.transport_port = uvm_transport_port("transport_port", self)
        self.transport_port.connect(self)
    
    async def transport(self, req):
        """Transport implementation - request/response."""
        self.logger.info(f"[{self.get_name()}] Received request: {req}")
        # Create response
        resp = TLMTransaction()
        resp.data = req.data + 1
        await Timer(10, units="ns")
        self.logger.info(f"[{self.get_name()}] Sending response: {resp}")
        return resp

    async def nb_transport(self, req):
        """Non-blocking transport implementation."""
        return await self.transport(req)


# TLM FIFO Example
class FIFOProducer(uvm_component):
    """Component producing to TLM FIFO."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building FIFOProducer")
        self.put_port = uvm_put_port("put_port", self)
    
    async def run_phase(self):
        self.raise_objection()
        for i in range(5):
            txn = TLMTransaction()
            txn.data = i * 0x30
            self.logger.info(f"[{self.get_name()}] Producing to FIFO: {txn}")
            await self.put_port.put(txn)
        self.drop_objection()


class FIFOConsumer(uvm_component):
    """Component consuming from TLM FIFO."""
    
    def build_phase(self):
        self.logger.info(f"[{self.get_name()}] Building FIFOConsumer")
        self.get_port = uvm_get_port("get_port", self)
    
    async def run_phase(self):
        self.raise_objection()
        for i in range(5):
            txn = await self.get_port.get()
            if txn:
                self.logger.info(f"[{self.get_name()}] Consuming from FIFO: {txn}")
        self.drop_objection()


class TLMEnv(uvm_env):
    """Environment demonstrating TLM connections."""
    
    def build_phase(self):
        self.logger.info("Building TLMEnv")
        # Put interface components
        self.put_producer = PutProducer.create("put_producer", self)
        self.put_consumer = PutConsumer.create("put_consumer", self)
        
        # Get interface components
        self.get_producer = GetProducer.create("get_producer", self)
        self.get_consumer = GetConsumer.create("get_consumer", self)
        
        # Transport interface components
        self.transport_comp = TransportComponent.create("transport_comp", self)
        
        # FIFO components
        self.fifo = uvm_tlm_fifo("fifo", self)
        self.fifo_producer = FIFOProducer.create("fifo_producer", self)
        self.fifo_consumer = FIFOConsumer.create("fifo_consumer", self)
    
    def connect_phase(self):
        self.logger.info("Connecting TLMEnv")
        # Connect put interface
        self.put_producer.put_port.connect(self.put_consumer)
        
        # Connect get interface
        self.get_consumer.get_port.connect(self.get_producer)
        
        # Connect FIFO
        self.fifo_producer.put_port.connect(self.fifo.put_export)
        self.fifo_consumer.get_port.connect(self.fifo.get_export)


class TLMTest(uvm_test):
    """Test demonstrating TLM usage."""
    
    async def build_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("TLM Example Test")
        self.logger.info("=" * 60)
        self.env = TLMEnv.create("env", self)
    
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Running TLM test")
        
        # Demonstrate transport
        self.logger.info("=" * 60)
        self.logger.info("Transport Interface Example:")
        req = TLMTransaction()
        req.data = 0xAA
        resp = await self.env.transport_comp.transport_port.transport(req)
        self.logger.info(f"Request: {req}, Response: {resp}")
        
        await Timer(100, units="ns")
        self.drop_objection()
    
    def report_phase(self):
        self.logger.info("=" * 60)
        self.logger.info("TLM test completed")
        self.logger.info("=" * 60)


# Helper function to recursively call build_phase on all children
async def build_all_children(comp):
    """Recursively call build_phase on component and all its children."""
    import inspect
    # Call build_phase on this component if it hasn't been called
    if hasattr(comp, 'build_phase'):
        if inspect.iscoroutinefunction(comp.build_phase):
            await comp.build_phase()
        else:
            comp.build_phase()
    
    # Get all children and call build_phase on them
    # Try different ways to access children
    children = []
    if hasattr(comp, '_children'):
        children = list(comp._children.values())
    elif hasattr(comp, 'get_children'):
        children = comp.get_children()
    else:
        # Try to find child components by checking attributes
        for attr_name in dir(comp):
            if not attr_name.startswith('_'):
                attr = getattr(comp, attr_name, None)
                if attr is not None and isinstance(attr, uvm_component):
                    children.append(attr)
    
    for child in children:
        await build_all_children(child)


# Cocotb test function to run the pyuvm test
@cocotb.test()
async def test_tlm(dut):
    """Cocotb test wrapper for pyuvm TLM test."""
    import inspect
    test = TLMTest.create("test")
    await test.build_phase()
    # Recursively build all children
    if hasattr(test, 'env') and test.env:
        await build_all_children(test.env)
    if hasattr(test, 'connect_phase') and inspect.iscoroutinefunction(test.connect_phase):
        await test.connect_phase()
    # Ensure env's connect_phase is called
    if hasattr(test, 'env') and test.env and hasattr(test.env, 'connect_phase'):
        if inspect.iscoroutinefunction(test.env.connect_phase):
            await test.env.connect_phase()
        else:
            test.env.connect_phase()
    await test.run_phase()
    if hasattr(test, 'check_phase'):
        test.check_phase()
    test.report_phase()


if __name__ == "__main__":
    print("This is a pyuvm TLM example.")
    print("To run with cocotb, use the Makefile in the test directory.")

