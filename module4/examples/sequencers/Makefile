# Makefile for sequencers example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = sequencer_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/interfaces/simple_interface.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = sequencer_example
TOPLEVEL = simple_interface
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

