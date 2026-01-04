# Makefile for objections example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = objections_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/simple_blocks/adder.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = objections_example
TOPLEVEL = adder
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

