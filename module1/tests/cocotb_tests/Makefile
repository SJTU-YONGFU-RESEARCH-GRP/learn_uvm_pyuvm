# Makefile for Module 1 cocotb tests
# Usage: make SIM=verilator test_and_gate

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_and_gate.py test_counter.py

# Verilog files
VERILOG_SOURCES = ../../dut/simple_gates/and_gate.v ../../dut/simple_gates/counter.v

# Test to run
TEST ?= test_and_gate

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = $(shell echo $(TEST) | sed 's/test_//')
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

# Helper targets
.PHONY: test_all
test_all:
	$(MAKE) TEST=test_and_gate
	$(MAKE) TEST=test_counter

# Note: clean target is provided by included Makefile.sim

