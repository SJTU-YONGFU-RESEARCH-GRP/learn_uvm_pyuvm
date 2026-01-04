# Makefile for callbacks example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = callback_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/advanced/multi_channel.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = callback_example
TOPLEVEL = multi_channel
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

