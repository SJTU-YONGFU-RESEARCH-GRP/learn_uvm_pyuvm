# Makefile for Module 6 pyuvm tests
# Usage: make SIM=verilator TEST=test_complex_testbench

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_complex_testbench.py

# Verilog files
VERILOG_FILES = ../../dut/protocols/axi4_lite_slave.v

# Test to run
TEST ?= test_complex_testbench

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = axi4_lite_slave
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf sim_build
	rm -rf results.xml
	rm -rf *.vcd
	rm -rf *.log

