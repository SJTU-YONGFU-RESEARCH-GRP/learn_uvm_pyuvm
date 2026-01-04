# Makefile for Module 3 pyuvm tests
# Usage: make SIM=verilator test_simple_uvm

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_simple_uvm.py

# Verilog files
VERILOG_SOURCES = ../../dut/simple_blocks/adder.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Test to run
TEST ?= test_simple_uvm

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = adder
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

