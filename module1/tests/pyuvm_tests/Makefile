# Makefile for Module 1 pyuvm tests
# Usage: make SIM=verilator test_and_gate_uvm

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_and_gate_uvm.py

# Verilog files
VERILOG_SOURCES = ../../dut/simple_gates/and_gate.v

# Test to run
TEST ?= test_and_gate_uvm

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = and_gate
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

# Note: clean target is provided by included Makefile.sim
