# Makefile for Module 4 pyuvm tests
# Usage: make SIM=verilator TEST=test_complete_agent

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_complete_agent.py

# Verilog files
VERILOG_SOURCES = ../../dut/interfaces/simple_interface.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Test to run
TEST ?= test_complete_agent

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = simple_interface
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

