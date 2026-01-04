# Makefile for signal_access example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = signal_access_example.py

# Verilog files
VERILOG_SOURCES = ../../dut/registers/simple_register.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = signal_access_example
TOPLEVEL = simple_register
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

