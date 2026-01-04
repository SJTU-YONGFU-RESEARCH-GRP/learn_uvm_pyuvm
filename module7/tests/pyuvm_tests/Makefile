# Makefile for Module 7 pyuvm tests
# Usage: make SIM=verilator TEST=test_real_world

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_real_world.py

# Verilog files
VERILOG_FILES = ../../dut/dma/simple_dma.v

# Test to run
TEST ?= test_real_world

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = simple_dma
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

