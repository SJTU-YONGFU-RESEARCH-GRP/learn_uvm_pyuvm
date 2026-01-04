# Makefile for Module 6 pyuvm tests
# Usage: make SIM=verilator TEST=test_complex_testbench

# Default simulator
SIM ?= icarus

# Python files
PYTHON_FILES = test_complex_testbench.py

# Verilog files
VERILOG_SOURCES = ../../dut/protocols/axi4_lite_slave.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Test to run
TEST ?= test_complex_testbench

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = axi4_lite_slave
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

