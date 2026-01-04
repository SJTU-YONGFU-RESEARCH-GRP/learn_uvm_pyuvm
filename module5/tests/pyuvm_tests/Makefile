# Makefile for Module 5 pyuvm tests
# Usage: make SIM=verilator TEST=test_advanced_uvm

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_advanced_uvm.py

# Verilog files
VERILOG_SOURCES = ../../dut/advanced/multi_channel.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Test to run
TEST ?= test_advanced_uvm

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = multi_channel
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

