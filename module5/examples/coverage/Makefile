# Makefile for coverage example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = coverage_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/advanced/multi_channel.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = coverage_example
TOPLEVEL = multi_channel
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

