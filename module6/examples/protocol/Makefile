# Makefile for protocol example
# Usage: make SIM=verilator

# Default simulator
SIM ?= icarus

# Python test file
PYTHON_FILES = protocol_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/protocols/axi4_lite_slave.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables
MODULE = protocol_example
TOPLEVEL = axi4_lite_slave
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

